import sys
import heapq
import sqlite3
from ui import Ui_MainWindow
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow,QMessageBox,QAction
from PyQt5.QtGui import QIntValidator, QDoubleValidator,QBrush,QColor

class MyMainForm(QMainWindow,Ui_MainWindow):

    def __init__(self,parent = None):
        try:
            sql.create_db()
        except:
            pass
        super(MyMainForm,self).__init__(parent)
        self.setupUi(self)
        # 添加计算按钮信号和槽，注意display函数不加()
        self.pushButton.clicked.connect(self.main)   
        self.pushButton_2.clicked.connect(self.del_zzjg)     
        # 限制输入
        self.x.setValidator(QDoubleValidator())
        self.y.setValidator(QDoubleValidator())
        self.x_.setValidator(QDoubleValidator())
        self.y_.setValidator(QDoubleValidator())
        self.xiubian.setValidator(QIntValidator())
        self.yaokou.setValidator(QIntValidator())
        self.zdzzc.setValidator(QIntValidator())
        self.zdzzk.setValidator(QIntValidator())
        self.zxzzc.setValidator(QIntValidator())
        self.zxzzk.setValidator(QIntValidator())
        self.comboBox.setEditable(True)
        self.comboBox.activated.connect(self.on_comboBox_activated)
        menu = self.menuBar() 
        aboutmenu = menu.addMenu("帮助")

        Upgrade_log = QAction("升级日志",self)
        aboutmenu.triggered.connect(self.Upgrade_log)
        aboutmenu.addAction(Upgrade_log)

        # 重建复选框内容
        data_zzjg = sql.select_db()
        for item in data_zzjg:
            self.comboBox.addItem(item[1])
            
        select_zzjg = sql.select_db_by_zzjg(self.comboBox.currentText())
        if len(select_zzjg) != 0:
            self.paper.setText(select_zzjg[0][2])    
    def Upgrade_log(self):
        msgbox = QMessageBox().about(None,"升级内容",
        '''
2020-07-29
 1.修复155碗盖1000计算问题

2020-07-26
 1.新增推荐指数
 2.新增颜色标记
 3.新增横切规格
 4.分纸张类型
 5.调整最优解算法
        '''
        )

    def on_comboBox_activated(self):    
        select_zzjg = sql.select_db_by_zzjg(self.comboBox.currentText())
        if len(select_zzjg) != 0:
            self.paper.setText(select_zzjg[0][2])            

    def input_text(self):
        # 定义全局变量：输入数值
        global yaokou,xiubian,yswc,cut_max_k,cut_max_c,cut_min_k,cut_min_c,max_cut_num
        # 定义行列
        global len_i,len_j
        x              = float(self.x.text())
        y              = float(self.y.text())
        x_             = float(self.x_.text())
        y_             = float(self.y_.text())
        yaokou         = float(self.yaokou.text())
        xiubian        = float(self.xiubian.text()) 
        yswc           = float(self.yswc.text())
        paper_str      = self.paper.text()
        cut_max_k      = float(self.zdzzk.text()) 
        cut_max_c      = float(self.zdzzc.text())
        cut_min_k      = float(self.zxzzk.text())
        cut_min_c      = float(self.zxzzc.text())

        # 判断是否为整数
        if cut_max_k == int(cut_max_k):
            cut_max_k = int(cut_max_k)
        
        if cut_max_c == int(cut_max_c):
            cut_max_c = int(cut_max_c)

        if cut_min_c == int(cut_min_c):
            cut_min_c = int(cut_min_c)

        if cut_min_k == int(cut_min_k):
            cut_min_k = int(cut_min_k)


        # 定义状态指针
        global ztzz
        ztzz = 0

        # 纸张宽度数组
        p_list_temp = paper_str.split('|')
        p_list = []
        for item in p_list_temp:
            try:
                item = float(item)
                if item == int(item):
                    item = int(item)
                p_list.append(item)

            except:
                QMessageBox.information(self,"错误","原纸宽度输入有误！")
                ztzz = 1

        # 定义表格行数,列数
        len_i = len(p_list)
        len_j = 14

        # 碗盖长宽合理性
        if x == 0 :
            QMessageBox.information(self,"错误","碗盖“长”不能为0！")
            ztzz = 1
        elif x == int(x):
            x = int(x)
            
        
        if y == 0 :
            QMessageBox.information(self,"错误","碗盖“宽”不能为0！")
            ztzz = 1
        elif y == int(y):
            y = int(y)
            

        if x_ == 0 :
            QMessageBox.information(self,"错误","碗盖“横出血”不能为0！")
            ztzz = 1
        elif x_ == int(x_):
            x_ = int(x_)
            

        if y_ == 0 :
            QMessageBox.information(self,"错误","碗盖“纵出血”不能为0！")
            ztzz = 1
        elif y_ == int(y_):
            y_ = int(y_)
            

        if yaokou == 0 :
            QMessageBox.information(self,"错误","碗盖“咬口”不能为0！")
            ztzz = 1
        elif yaokou == int(yaokou):
            yaokou = int(yaokou)
            

        if xiubian == 0 :
            QMessageBox.information(self,"错误","碗盖“修边”不能为0！")
            ztzz = 1
        elif xiubian == int(xiubian):
            xiubian = int(xiubian)
            

        if yswc == 0 :
            QMessageBox.information(self,"错误","碗盖“印刷误差”不能为0！")
            ztzz = 1
        elif yswc == int(yswc):
            yswc = int(yswc)        

        # 判断碗盖长+横出血是否合适
        w_x = x + x_
        if w_x == int(w_x):
            w_x = int(w_x)
        else:
            QMessageBox.information(self,"错误","碗盖长+横出血必须为整数")    
            ztzz = 1

        # 判断碗盖宽+纵出血是否合适
        w_y = y + y_
        if w_y == int(w_y):
            w_y = int(w_y)
        else:
            QMessageBox.information(self,"错误","碗盖宽+纵出血必须为整数")   
            ztzz = 1      

        # 最大生产个数
        max_cut_num_1               = int(cut_max_c / w_x) * int(cut_max_k / w_y)
        max_cut_num_2               = int(cut_max_k / w_x) * int(cut_max_c / w_y)
        max_cut_num                 = max(max_cut_num_1,max_cut_num_2)

        display_data = []
        Bowllid = {}
        Bowllid['x'] = x
        Bowllid['y'] = y
        Bowllid['x_'] = x_
        Bowllid['y_'] = y_
        Bowllid['w_x'] = w_x
        Bowllid['w_y'] = w_y
        for p in p_list:
            if ztzz == 0:
                display_data.append(jscqgg.jisuan(Bowllid,p))
        return display_data

    def display(self):
        # 显示表格
        display_data = self.input_text()
        
        lyl_temp = []
        if len(display_data) > 0:
            for i in range(0,len_i):
                lyl_temp.append(display_data[i]['tjzs'])
            if len(display_data) >= 3:
                lyl_lagest = heapq.nlargest(3,lyl_temp)
            else:
                lyl_lagest = heapq.nlargest(len(display_data),lyl_temp)
        else:
            lyl_lagest = []
        # 显示定义
        str0 = ['碗盖长\n(mm)','碗盖宽\n(mm)','横出血\n(mm)','纵出血\n(mm)','横切规格\n(mm)','裁切规格1\n(mm)','裁切规格2\n(mm)','拼数1\n(拼)','拼数2\n(拼)','飞边\n(mm)','原纸宽\n(mm)','利用率\n(%)','生产效率\n(%)','推荐指数\n(%)']
        str1 = ['x','y','x_','y_','w_y_0','cut_1','cut_2','cut_1_num','cut_2_num','w_x_0','p','lyl','scxl','tjzs']
        str2 = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14']
        
        # 设置表头
        # 设置行
        self.outview.setRowCount(len_i)
        # 设置列
        self.outview.setColumnCount(len_j)        
        self.outview.setHorizontalHeaderLabels(str0)
        self.outview.setVerticalHeaderLabels(str2)
        self.outview.setColumnWidth(4,80)
        self.outview.setColumnWidth(5,80)
        self.outview.setColumnWidth(6,80)
        self.outview.setColumnWidth(12,60)
        self.outview.setColumnWidth(13,60)

        if ztzz == 0:
            for i in range(0,len_i):
                for j in range(0,len_j):
                    st1 = str(display_data[i][str1[j]])
                    item = QtWidgets.QTableWidgetItem(st1)
                    if display_data[i]['tjzs'] in lyl_lagest:
                        display_data[i]['ztm'] = 1
                        if display_data[i]['ztm'] == 1:
                            item.setBackground(QBrush(QColor(106,247,91)))
                        if display_data[i]['tjzs'] < 90:
                            item.setBackground(QBrush(QColor(253,255,94)))
                    elif display_data[i]['ztm'] == 2:
                        item.setBackground(QBrush(QColor(253,255,94)))
                    self.outview.setItem(i,j,item)
        else:
            for i in range(0,len_i):
                for j in range(0,len_j):
                    item = QtWidgets.QTableWidgetItem("")
                    self.outview.setItem(i,j,item)

    def main(self):
        self.display()
        self.zzjg_chuli()

    def zzjg_chuli(self): 
        zzjg_temp = self.comboBox.currentText()
        paper_width_temp = self.paper.text()

        zzjg_zhuangtai = sql.select_db_by_zzjg(zzjg_temp)

        # 新的纸张规格及原纸宽
        if len(zzjg_zhuangtai) == 0:
            msg_xin = '是否新增纸张规格：“' + zzjg_temp + "”及纸张宽度：“" + paper_width_temp + "”？"
            msgbox_relay_xin = QMessageBox.question(self,"新增",msg_xin,QMessageBox.Yes|QMessageBox.No)
            if msgbox_relay_xin == 16384:
                msg_insert = sql.insert_db(zzjg_temp,paper_width_temp)
                msgbox = QMessageBox.about(None,"通知",msg_insert)
                self.comboBox.addItem(zzjg_temp)
        # 更新纸张宽度
        elif len(zzjg_zhuangtai) > 0:
            if sql.select_db_by_zzjg(zzjg_temp)[0][2] != paper_width_temp:
                msg_xiu = '是否修改纸张规格：“' + zzjg_temp + "“的纸张宽度" + paper_width_temp + "”？"
                msgbox_relay_xiu = QMessageBox.question(self,"修改",msg_xiu,QMessageBox.Yes|QMessageBox.No)
                if msgbox_relay_xiu == 16384:
                    sql.update_db(zzjg_temp,paper_width_temp)
                    msg_update = "已更新" + zzjg_temp
                    msgbox = QMessageBox.about(None,"通知",msg_update)

    def del_zzjg(self):
        zzjg_temp = self.comboBox.currentText()
        paper_width_temp = self.paper.text()
        msg_del = '是否删除纸张规格：“' + zzjg_temp + "“及纸张宽度" + paper_width_temp + "”？"
        msgbox_relay_del = QMessageBox.question(self,"删除",msg_del,QMessageBox.Yes|QMessageBox.No)
        if msgbox_relay_del == 16384:
            sql.delete_db_by_zzjg(zzjg_temp)
            msg_delete = "已删除" + zzjg_temp
            msgbox = QMessageBox.about(None,"通知",msg_delete)
            for i in range(0,self.comboBox.count()):
                if self.comboBox.itemText(i) == zzjg_temp:
                    self.comboBox.removeItem(i)

class sql(object):
    def create_db():
        conn = sqlite3.connect('test.db')
        c = conn.cursor()
        c.execute('''
        CREATE TABLE ZZJG(
        ID INTEGER PRIMARY KEY,
        zzjg TEXT NOT NULL,
        paper_width TEXT NOT NULL
        );
        ''')
        conn.commit()
        conn.close()

    def select_db():
        conn = sqlite3.connect('test.db')
        c = conn.cursor()
        sql = 'SELECT ID,zzjg,paper_width from ZZJG'
        data = c.execute(sql).fetchall()
        conn.close()
        return data

    def select_db_by_zzjg(zzjg):
        conn = sqlite3.connect('test.db')
        c = conn.cursor()
        sql_select = 'SELECT ID,zzjg,paper_width from ZZJG where zzjg = \'' + str(zzjg) + '\''
        select_data = c.execute(sql_select).fetchall()
        return select_data

    def delete_db_by_zzjg(zzjg):
        conn = sqlite3.connect('test.db')
        c = conn.cursor()
        sql_delete = 'DELETE FROM ZZJG WHERE zzjg = \'' + str(zzjg) + '\''
        c.execute(sql_delete)  
        conn.commit()
        conn.close()    

    def insert_db(zzjg,paper_width):
        conn = sqlite3.connect('test.db')
        c = conn.cursor()
        sql_select = 'SELECT ID,zzjg,paper_width from ZZJG where zzjg = \'' + str(zzjg) + '\''
        select_data = c.execute(sql_select).fetchall()
        if len(select_data) == 0:
            sql_insert = 'INSERT INTO ZZJG (zzjg,paper_width) values(\'' + str(zzjg) + '\' ,\'' + str(paper_width) + '\')'
            c.execute(sql_insert)
            conn.commit()
            conn.close()
            msg = "已添加" + zzjg
        else:
            msg = "已存在" + zzjg
        return msg

    def update_db(zzjg,paper_width):
        conn = sqlite3.connect('test.db')
        c = conn.cursor()
        sql_update = 'UPDATE ZZJG SET paper_width = \'' + str(paper_width) + '\' where zzjg = \'' + str(zzjg) + '\''
        c.execute(sql_update)
        conn.commit()
        conn.close()

class jscqgg(object):
    def js_Bowllid_list_temp(Bowllid,p):
        Bowllid_list_temp = []        
        x = Bowllid['y']
        y = Bowllid['x']
        x_ = Bowllid['y_']
        y_ = Bowllid['x_']
        w_x = Bowllid['w_y']
        w_y = Bowllid['w_x']
        # y_max 用长可增加生产效率和纸张利用率
        y_min = int(cut_min_k / w_y) + 1
        y_max = int(cut_max_c / w_y)
        x_1 = int((p-16) / w_x) - int(int((p-16) / w_x) /2)
        x_2 = int((p-16) / w_x) - x_1
        Bowllid_list_temp_temp = {}
        y_list = []
        for i in range(y_min , y_max + 1):
            y_list.append(i)
        Bowllid_list_temp_temp['x'] = x
        Bowllid_list_temp_temp['y'] = y
        Bowllid_list_temp_temp['x_'] = x_
        Bowllid_list_temp_temp['y_'] = y_
        Bowllid_list_temp_temp['w_x'] = w_x
        Bowllid_list_temp_temp['w_y'] = w_y
        Bowllid_list_temp_temp['x_1'] = x_1
        Bowllid_list_temp_temp['x_2'] = x_2
        Bowllid_list_temp_temp['y_list'] = y_list
        Bowllid_list_temp_temp['p'] = p
        Bowllid_list_temp.append(Bowllid_list_temp_temp)
        if Bowllid['x'] != Bowllid['y']:
            # 第1种，共2种
            x = Bowllid['x']
            y = Bowllid['y']
            x_ = Bowllid['x_']
            y_ = Bowllid['y_']
            w_x = Bowllid['w_x']
            w_y = Bowllid['w_y']            
            # y_max 用长可增加生产效率和纸张利用率
            y_min = int(cut_min_k / w_y) + 1
            y_max = int(cut_max_c / w_y)
            x_1 = int((p-16) / w_x) - int(int((p-16) / w_x) /2)
            x_2 = int((p-16) / w_x) - x_1
            Bowllid_list_temp_temp = {}
            y_list = []
            for i in range(y_min , y_max + 1):
                y_list.append(i)
            Bowllid_list_temp_temp['x'] = x
            Bowllid_list_temp_temp['y'] = y
            Bowllid_list_temp_temp['x_'] = x_
            Bowllid_list_temp_temp['y_'] = y_
            Bowllid_list_temp_temp['w_x'] = w_x
            Bowllid_list_temp_temp['w_y'] = w_y
            Bowllid_list_temp_temp['x_1'] = x_1
            Bowllid_list_temp_temp['x_2'] = x_2
            Bowllid_list_temp_temp['y_list'] = y_list
            Bowllid_list_temp_temp['p'] = p
            Bowllid_list_temp.append(Bowllid_list_temp_temp)
        return Bowllid_list_temp

    def js_Bowllid_build_list_temp(Bowllid_list_temp):
        # 计算所有开料规格的可能性
        temp_Bowllid_build_list = []
        for Bowllid_list_temp_temp in Bowllid_list_temp:
            x = Bowllid_list_temp_temp['x']
            y = Bowllid_list_temp_temp['y']
            x_ = Bowllid_list_temp_temp['x_']
            y_ = Bowllid_list_temp_temp['y_']
            w_x = Bowllid_list_temp_temp['w_x']
            w_y = Bowllid_list_temp_temp['w_y']
            x_1 = Bowllid_list_temp_temp['x_1']
            x_2 = Bowllid_list_temp_temp['x_2']
            y_list = Bowllid_list_temp_temp['y_list']
            p = Bowllid_list_temp_temp['p']

            w_y_ = 10000
            w_x_1 = 0
            w_x_2 = 0
            w_x_0 = 0
            lyl = 0
            try:
                y_list.remove(x_1)
                y_list.remove(x_2)
            except:
                pass
            if len(y_list) != 0:
                for i in y_list:
                    Bowllid_build = []
                    if i < x_1:
                        temp_x = (x_1 + x_2) * w_x + yswc * 2
                        if temp_x + 10 <= p:
                            w_y_ = i * w_y + yaokou
                            w_x_1 = x_1 * w_x + yswc
                            w_x_2 = x_2 * w_x + yswc
                            w_x_0 = p - temp_x
                    else:
                        temp_x = (x_1 + x_2) * w_x + yaokou * 2
                        if temp_x + 10<= p:
                            w_y_ = i * w_y + yswc
                            w_x_1 = x_1 * w_x + yaokou
                            w_x_2 = x_2 * w_x + yaokou
                            w_x_0 = p - temp_x
                        else:
                            if x_1 == x_2:
                                x_2 = x_2 - 1
                                temp_x = (x_1 + x_2) * w_x + yaokou * 2
                                if temp_x + 10 <= p:
                                    w_y_ = i * w_y + yswc
                                    w_x_1 = x_1 * w_x + yaokou
                                    w_x_2 = x_2 * w_x + yaokou
                                    w_x_0 = p - temp_x
                            else:
                                x_1 = x_1 - 1
                                temp_x = (x_1 + x_2) * w_x + yaokou * 2
                                if temp_x + 10 <=p:
                                    w_y_ = i * w_y + yswc
                                    w_x_1 = x_1 * w_x + yaokou
                                    w_x_2 = x_2 * w_x + yaokou
                                    w_x_0 = p - temp_x
                    temp_area_1 = (x_1 + x_2) * i * w_x * w_y
                    temp_area_2 = (w_y_ + xiubian) * p
                    # 利用率
                    lyl = round(temp_area_1 / temp_area_2,4)
                    # 生产效率
                    cut_1 = str(w_x_1) + "*" + str(w_y_)
                    cut_2 = str(w_x_2) + "*" + str(w_y_)
                    cut_1_num = int(w_x_1 / w_x) * int(w_y_ / w_y)
                    cut_2_num = int(w_x_2 / w_x) * int(w_y_ / w_y)   
                    scxl      = (cut_1_num + cut_2_num) / max_cut_num / 2   
                    # 推荐指数
                    tjzs = lyl * scxl              
                    Bowllid_build = {}
                    Bowllid_build['x'] = x
                    Bowllid_build['y'] = y
                    Bowllid_build['x_'] = x_
                    Bowllid_build['y_'] = y_
                    Bowllid_build['w_x'] = w_x
                    Bowllid_build['w_y'] = w_y
                    Bowllid_build['w_x_1'] = w_x_1
                    Bowllid_build['w_x_2'] = w_x_2
                    Bowllid_build['w_x_0'] = w_x_0
                    Bowllid_build['w_y_'] = w_y_
                    Bowllid_build['w_y_0'] = str(w_y_ + xiubian) + "*" + str(p)
                    Bowllid_build['p'] = p
                    Bowllid_build['lyl'] = lyl
                    Bowllid_build['scxl'] = scxl
                    Bowllid_build['tjzs'] = tjzs
                    temp_Bowllid_build_list.append(Bowllid_build)
            else:
                Bowllid_build = {}
                Bowllid_build['x'] = x
                Bowllid_build['y'] = y
                Bowllid_build['x_'] = x_
                Bowllid_build['y_'] = y_
                Bowllid_build['w_x'] = w_x
                Bowllid_build['w_y'] = w_y
                Bowllid_build['w_x_1'] = w_x_1
                Bowllid_build['w_x_2'] = w_x_2
                Bowllid_build['w_x_0'] = w_x_0
                Bowllid_build['w_y_'] = 0
                Bowllid_build['w_y_0'] = 0
                Bowllid_build['p'] = p
                Bowllid_build['lyl'] = 0
                Bowllid_build['scxl'] = 0
                Bowllid_build['tjzs'] = 0
                temp_Bowllid_build_list.append(Bowllid_build)
            for i in (x_1,x_2):
                if len(y_list) != 0 and y >= min(y_list):
                    temp_x = (x_1 + x_2) * w_x
                    Bowllid_build = {}    
                    if temp_x + 2 * yaokou + 10 <= p:
                        w_y_ = i * w_y + yswc
                        w_x_1 = x_1 * w_x + yaokou
                        w_x_2 = x_2 * w_x + yaokou
                        w_x_0 = p - temp_x - 2*yaokou
                    elif temp_x + 2 * yswc + 10 <= p:
                        w_y_ = i * w_y + yaokou
                        w_x_1 = x_1 * w_x + yswc
                        w_x_2 = x_2 * w_x + yswc
                        w_x_0 = p - 2 * yswc - temp_x
                    temp_area_1 = (x_1 + x_2) * i * w_x * w_y
                    temp_area_2 = (w_y_ + xiubian) * p
                    lyl = round(temp_area_1 / temp_area_2,4)
                    # 生产效率
                    cut_1 = str(w_x_1) + "*" + str(w_y_)
                    cut_2 = str(w_x_2) + "*" + str(w_y_)
                    cut_1_num = int(w_x_1 / w_x) * int(w_y_ / w_y)
                    cut_2_num = int(w_x_2 / w_x) * int(w_y_ / w_y)   
                    scxl      = (cut_1_num + cut_2_num) / max_cut_num / 2   
                    # 推荐指数
                    tjzs = lyl * scxl  
                    Bowllid_build['x'] = x
                    Bowllid_build['y'] = y
                    Bowllid_build['x_'] = x_
                    Bowllid_build['y_'] = y_
                    Bowllid_build['w_x'] = w_x
                    Bowllid_build['w_y'] = w_y
                    Bowllid_build['w_x_1'] = w_x_1
                    Bowllid_build['w_x_2'] = w_x_2
                    Bowllid_build['w_x_0'] = w_x_0
                    Bowllid_build['w_y_'] = w_y_
                    Bowllid_build['w_y_0'] = str(w_y_ + xiubian) + "*" + str(p)
                    Bowllid_build['p'] = p
                    Bowllid_build['lyl'] = lyl
                    Bowllid_build['scxl'] = scxl
                    Bowllid_build['tjzs'] = tjzs
                    temp_Bowllid_build_list.append(Bowllid_build)   
                elif len(y_list) == 0:
                    if i == x_1:
                        temp_x = (x_1 + x_2) * w_x
                        Bowllid_build = {} 
                        if temp_x + 2 * yaokou + 10 <= p:
                            w_y_ = i * w_y + yswc
                            w_y_ = i * w_y + yswc
                            w_x_1 = x_1 * w_x + yaokou
                            w_x_2 = x_2 * w_x + yaokou
                            w_x_0 = p - temp_x - 2 * yaokou  
                        elif temp_x + 2 * yswc + 10 <= p:
                            w_y_ = i * w_y + yaokou
                            w_x_1 = x_1 * w_x + yswc
                            w_x_2 = x_2 * w_x + yswc
                            w_x_0 = p - 2 * yswc - temp_x
                        temp_area_1 = (x_1 + x_2) * i * w_x * w_y
                        temp_area_2 = (w_y_ + xiubian) * p
                        lyl = round(temp_area_1 / temp_area_2,4)
                        # 生产效率
                        cut_1 = str(w_x_1) + "*" + str(w_y_)
                        cut_2 = str(w_x_2) + "*" + str(w_y_)
                        cut_1_num = int(w_x_1 / w_x) * int(w_y_ / w_y)
                        cut_2_num = int(w_x_2 / w_x) * int(w_y_ / w_y)   
                        scxl      = (cut_1_num + cut_2_num) / max_cut_num / 2   
                        # 推荐指数
                        tjzs = lyl * scxl  
                        Bowllid_build['x'] = x
                        Bowllid_build['y'] = y
                        Bowllid_build['x_'] = x_
                        Bowllid_build['y_'] = y_
                        Bowllid_build['w_x'] = w_x
                        Bowllid_build['w_y'] = w_y
                        Bowllid_build['w_x_1'] = w_x_1
                        Bowllid_build['w_x_2'] = w_x_2
                        Bowllid_build['w_x_0'] = w_x_0
                        Bowllid_build['w_y_'] = w_y_
                        Bowllid_build['w_y_0'] = str(w_y_ + xiubian) + "*" + str(p)
                        Bowllid_build['p'] = p
                        Bowllid_build['lyl'] = lyl
                        Bowllid_build['scxl'] = scxl
                        Bowllid_build['tjzs'] = tjzs
                        temp_Bowllid_build_list.append(Bowllid_build)                          
                    elif i == x_2:
                        temp_x = (x_1 + x_2) * w_x
                        Bowllid_build = {}    
                        if temp_x + 2 * yaokou + 10 <= p:
                            w_y_ = i * w_y + yswc
                            w_x_1 = x_1 * w_x + yaokou
                            w_x_2 = x_2 * w_x + yaokou
                            w_x_0 = p - temp_x - 2*yaokou
                        elif temp_x + 2 * yswc + 10 <= p:
                            w_y_ = i * w_y + yaokou
                            w_x_1 = x_1 * w_x + yswc
                            w_x_2 = x_2 * w_x + yswc
                            w_x_0 = p - 2 * yswc - temp_x
                        temp_area_1 = (x_1 + x_2) * i * w_x * w_y
                        temp_area_2 = (w_y_ + xiubian) * p
                        lyl = round(temp_area_1 / temp_area_2,4)
                        # 生产效率
                        cut_1 = str(w_x_1) + "*" + str(w_y_)
                        cut_2 = str(w_x_2) + "*" + str(w_y_)
                        cut_1_num = int(w_x_1 / w_x) * int(w_y_ / w_y)
                        cut_2_num = int(w_x_2 / w_x) * int(w_y_ / w_y)   
                        scxl      = (cut_1_num + cut_2_num) / max_cut_num / 2   
                        # 推荐指数
                        tjzs = lyl * scxl  
                        Bowllid_build['x'] = x
                        Bowllid_build['y'] = y
                        Bowllid_build['x_'] = x_
                        Bowllid_build['y_'] = y_
                        Bowllid_build['w_x'] = w_x
                        Bowllid_build['w_y'] = w_y
                        Bowllid_build['w_x_1'] = w_x_1
                        Bowllid_build['w_x_2'] = w_x_2
                        Bowllid_build['w_x_0'] = w_x_0
                        Bowllid_build['w_y_'] = w_y_
                        Bowllid_build['w_y_0'] = str(w_y_ + xiubian) + "*" + str(p)
                        Bowllid_build['p'] = p
                        Bowllid_build['lyl'] = lyl
                        Bowllid_build['scxl'] = scxl
                        Bowllid_build['tjzs'] = tjzs
                        temp_Bowllid_build_list.append(Bowllid_build)                          
                                                                  
        # 满足印刷纸张规格的解
        Bowllid_build_list = []
        for Bowllid_build_0 in temp_Bowllid_build_list:
            w_x_1 = Bowllid_build_0['w_x_1']
            w_x_2 = Bowllid_build_0['w_x_2']
            w_y_ = Bowllid_build_0['w_y_']
            temp_list = []
            temp_list.extend([w_x_1,w_x_2,w_y_])
            temp_max = max(temp_list)
            temp_min = min(temp_list)
            temp_list.remove(temp_max)
            temp_list.remove(temp_min)
            temp_0 = temp_list[0]
            if temp_max <= cut_max_c and temp_0 <= cut_max_k and temp_min >= cut_min_k:
                Bowllid_build_list.append(Bowllid_build_0)
        Bowllid_build = {}
        if len(Bowllid_build_list) == 0:
            Bowllid_build['x'] = x
            Bowllid_build['y'] = y
            Bowllid_build['x_'] = x_
            Bowllid_build['y_'] = y_
            Bowllid_build['w_x'] = w_x
            Bowllid_build['w_y'] = w_y
            Bowllid_build['w_x_1'] = 0
            Bowllid_build['w_x_2'] = 0
            Bowllid_build['w_x_0'] = 0
            Bowllid_build['w_y_'] = 0
            Bowllid_build['w_y_0'] = 0
            Bowllid_build['p'] = p
            Bowllid_build['lyl'] = 0      
            Bowllid_build['scxl'] = 0
            Bowllid_build['tjzs'] = 0
            Bowllid_build_list.append(Bowllid_build)    
        return Bowllid_build_list      

    def js_Bowl_specifications_list(Bowllid_build_list):
        tjzs_temp = []
        Bowl_specifications_list = []
        for i in range(0,len(Bowllid_build_list)):
            tjzs_temp.append(Bowllid_build_list[i]['tjzs'])
        for i in range(0,len(Bowllid_build_list)):
            w_x_1 = Bowllid_build_list[i]['w_x_1']
            w_x_2 = Bowllid_build_list[i]['w_x_2']
            w_y_  = Bowllid_build_list[i]['w_y_']
            tjzs  = Bowllid_build_list[i]['tjzs']
            if (w_x_1 - yaokou + yswc == w_y_) or (w_x_1 + yaokou - yswc == w_y_):
                if tjzs == max(tjzs_temp) and (max(tjzs_temp) > Bowllid_build_list[i]['tjzs'] + 0.1):
                    Bowl_specifications_list = Bowllid_build_list[i]
            elif tjzs == max(tjzs_temp):
                Bowl_specifications_list = Bowllid_build_list[i]    
        if len(Bowl_specifications_list) == 0:
            Bowl_specifications_list = Bowllid_build_list[i]
        return Bowl_specifications_list

    def js_Bowllid_list(Bowl_specifications_list):
        x     = Bowl_specifications_list['x']
        y     = Bowl_specifications_list['y']
        w_x   = Bowl_specifications_list['w_x']
        w_y   = Bowl_specifications_list['w_y']
        p     = Bowl_specifications_list['p']
        w_x_1 = Bowl_specifications_list['w_x_1']
        w_y_  = Bowl_specifications_list['w_y_']
        w_y_0 = Bowl_specifications_list['w_y_0']
        w_x_2 = Bowl_specifications_list['w_x_2'] 
        w_x_0 = Bowl_specifications_list['w_x_0']
        lyl   = Bowl_specifications_list['lyl']
        scxl  = Bowl_specifications_list['scxl']
        tjzs  = Bowl_specifications_list['tjzs']
        x_    = Bowl_specifications_list['x_']
        y_    = Bowl_specifications_list['y_']
        cut_1 = str(w_x_1) + "*" + str(w_y_)
        cut_2 = str(w_x_2) + "*" + str(w_y_)
        cut_1_num = int(w_x_1 / w_x) * int(w_y_ / w_y)
        cut_2_num = int(w_x_2 / w_x) * int(w_y_ / w_y)  
        
        Bowllid_list= {}
        if x >= y :
            Bowllid_list['x']       = y
            Bowllid_list['y']       = x
            Bowllid_list['x_']      = y_
            Bowllid_list['y_']      = x_
            Bowllid_list['w_x']     = w_y
            Bowllid_list['w_y']     = w_x
        else:
            Bowllid_list['x']       = x
            Bowllid_list['y']       = y
            Bowllid_list['x_']      = x_
            Bowllid_list['y_']      = y_ 
            Bowllid_list['w_x']     = w_x
            Bowllid_list['w_y']     = w_y                       
        Bowllid_list['cut_1']       = cut_1
        Bowllid_list['cut_2']       = cut_2
        Bowllid_list['cut_1_num']   = cut_1_num
        Bowllid_list['cut_2_num']   = cut_2_num
        Bowllid_list['w_y_0']       = w_y_0
        Bowllid_list['w_x_0']       = w_x_0
        Bowllid_list['p']           = p
        Bowllid_list['lyl']         = round(lyl * 100 , 1)
        Bowllid_list['scxl']        = round(scxl * 100 , 1)
        Bowllid_list['tjzs']        = round(tjzs * 100,1)
        # 状态码
        # 1,推荐指数大于90
        if Bowllid_list['tjzs'] >= 90:
            Bowllid_list['ztm'] = 1
        # 2,类似于正方形
        elif (w_x_1 + 10 == w_y_) or (w_x_2 + 10 == w_y_) or (w_x_1 - 10 == w_y_) or (w_x_2 - 10 == w_y_):
            Bowllid_list['ztm'] = 2
        else:
            Bowllid_list['ztm'] = 0
        return Bowllid_list

    def jisuan(Bowllid,p):
        Bowllid_list_temp = jscqgg.js_Bowllid_list_temp(Bowllid,p)
        Bowllid_build_list = jscqgg.js_Bowllid_build_list_temp(Bowllid_list_temp)
        # for item in Bowllid_build_list:
        #     print(item)
        Bowl_specifications_list = jscqgg.js_Bowl_specifications_list(Bowllid_build_list)
        Bowllid_list = jscqgg.js_Bowllid_list(Bowl_specifications_list)
        return Bowllid_list

if __name__ == "__main__":
    app = QApplication(sys.argv)              # 创建一个QApplication，也就是你要开发的软件app
    MainWindow = MyMainForm()                 # 创建一个QMainWindow，用来装载你需要的各种组件、控件
    MainWindow.show()                         # 执行QMainWindow的show()方法，显示这个QMainWindow
    sys.exit(app.exec_())                     # 使用exit()或者点击关闭按钮退出QApplication