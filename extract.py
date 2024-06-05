import mysql.connector

# MySQL 데이터베이스에 연결
db_connection = mysql.connector.connect(
    host="13.125.156.170",
    user="mincoding",
    password="1234",
    database="minDB"
)

cursor = db_connection.cursor()

# 데이터베이스에서 데이터 추출
cursor.execute("SELECT * FROM minDB.sensing")
data = cursor.fetchall()

# 데이터베이스 연결 종료
cursor.close()
db_connection.close()

# 추출한 데이터 확인
for row in data:
    print(row)

