import psycopg2, sys
try:
    conn = psycopg2.connect(dbname='postgres', user='odoo', password='odoo', host='localhost', port=5431)
    cur = conn.cursor()
    cur.execute("SELECT datname FROM pg_database;")
    print('Databases:', cur.fetchall())
    conn.close()
except Exception as e:
    print('ERROR:', e)
    sys.exit(1)
