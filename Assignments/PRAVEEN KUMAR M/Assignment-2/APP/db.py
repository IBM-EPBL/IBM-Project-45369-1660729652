import ibm_db
conn=ibm_db.connect("DATABASE=bludb;HOSTNAME=fbd88901-ebdb-4a4f-a32e-9822b9fb237b.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32731;SECURITY=SSL;SSLservercertiicate=DigiCertGlobalRootCA.crt;UID=vyq79202;PWD=sdL7FAq13svpnAm9",'','')
print(conn)
print("connection successful")



name = "praveen"
username = "praveen12"
email = "praveen@gmail.com"
password = "123456"


sql = "INSERT INTO SIGNUP VALUES (?,?,?,?)"
prep_stmt = ibm_db.prepare(conn, sql)
ibm_db.bind_param(prep_stmt, 1, name)
ibm_db.bind_param(prep_stmt, 2, username)
ibm_db.bind_param(prep_stmt, 3, email)
ibm_db.bind_param(prep_stmt, 4, password)
ibm_db.execute(prep_stmt)
print("Inserted Successfully")