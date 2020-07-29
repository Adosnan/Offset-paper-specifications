import sqlite3

conn = sqlite3.connect('test.db')
def create_db():
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

def select_db_by_zzjg(zzjg):
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    sql_select = 'SELECT ID,zzjg,paper_width from ZZJG where zzjg = \'' + str(zzjg) + '\''
    select_data = c.execute(sql_select).fetchall()
    return select_data

def select_db():
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    sql = 'SELECT ID,zzjg,paper_width from ZZJG'
    data = c.execute(sql).fetchall()
    conn.close()
    return data
    
for item in select_db():
    print(item)
