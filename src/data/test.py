import sqlite3
from sqlite3 import Error


def get_sql_string():
   
    sql = """select * from addresses a
join assosiation p
on p.address_id = a.id
where p.port_id in ports"""

    #print("hey", sql)
    return sql

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def execute_query(conn):
    cur = conn.cursor()
    cur.execute(get_sql_string())
    rows = cur.fetchall()

    for row in rows:
        print(row)

def main():
    db = "scan.sqlite333"
    conn = create_connection(db)
    print(1)
    print(get_sql_string())
    print(2)
    with conn:
        execute_query(conn)
main()
