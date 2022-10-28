import psycopg2 as pg2

conn = pg2.connect(host="local_pgdb",
                   port=5432,
                   database="postgres",
                   user="user",
                   password="admin")

command = """CREATE TABLE xxx (
        xxx VARCHAR(50),
        xxx VARCHAR(50),
        xxx INTEGER,
        xxx DATE,
        xxx INTEGER,
        xxx VARCHAR(50),
        xxx KEY (user_id) );"""

cursor = conn.cursor()
cursor.execute(command)
conn.commit()
conn.close()