import redis
import pymysql

def db_connect():
    conn = pymysql.connect(host='',
                           user='', password='', db='', charset='utf8')
    cursor = conn.cursor()

    return conn, cursor

def db_close(conn):
    conn.commit()
    conn.close()
    
if __name__ == "__main__":
    r = redis.Redis("localhost")
    print(r.ping())
    conn, cursor = db_connect()
    u_email = ''
    sql = "select * from User order by reward DESC limit 10"       
    #sql = "select * from dummy_gps2 where id = %s and timestep = %s"
    cursor.execute(sql)
    
    records = cursor.fetchall()
    db_close(conn)
    i = 1
    if len(records) > 0:
        for row in records:
            user_email = row[1]
            user_point = row[2]
            user_payment_method = row[3]
            user_account_no = row[4]
            user_rank = row[5]
            print(f'{user_email}, {user_point}, {user_payment_method}, {user_account_no}, {user_rank}')
            r.set('email_' + str(i),user_email)
            r.set('point_' + str(i),user_point)
            if i > 6:
                break
            i += 1