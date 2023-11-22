import json
import numpy as np
#import pandas as pd
from db_connect import *


def convert():
    conn, cursor = db_connect()

    sql = "select * from dummy_gps"
    cursor.execute(sql)

    rows = cursor.fetchall()
    leng = len(rows)
    db_close(conn)

    print(rows)
    for data in rows:
        id_ts = data[1]
        id_data = data[2]
        value_x = data[3]
        value_y = data[4]
        float_x = 36.380727 - \
            float(((float(value_x) - float(10)) * 1.34) / 1000000)
        #str_x = str(36.380727 + float_x)
        str_x = f'%2.6f' % (float_x)
        print("str_x : {}".format(str_x))
        float_y = 127.365615 - \
            float(((float(value_y) - float(120)) * 1.46) / 1000000)
        #str_y = str(127.365615 + float_y)
        str_y = f'%3.6f' % (float_y)
        print("str_y : {}".format(str_y))
        conn, cursor = db_connect()

        sql = "INSERT INTO dummy_gps2 (timestep, id, x, y) VALUES (%s,%s,%s,%s)"
        cursor.execute(sql, (id_ts, id_data, str_x, str_y))
        db_close(conn)


if __name__ == '__main__':
    convert()
