from flask import Flask, jsonify
from flask import request
import json
import numpy as np
#import pandas as pd
from db_connect import *

total_count = 0
v0_count = 0
v1_count = 0
p0_count = 0
p1_count = 0
p2_count = 0

id_ts = '0'
id_data = 'vehicle_0'
value_x = '36.380727'
value_y = '127.365615'

conn = 0
cursor = 0
res = 0

x_value = []
y_value = []
# data_json = {'id': '0', 'x': '0', 'y': '0'}
# packet_json = {'0': '0', '1': '1', '2': '2', '3': '3', '4': '4'}
# packet_json['0'] = data_json
# packet_json['1'] = data_json
# packet_json['2'] = data_json
# packet_json['3'] = data_json
# packet_json['4'] = data_json
# df = pd.read_csv('./dataset/dataset_01.csv')


def get_x_value(i):
    return df.iloc[i, 2]


def get_y_value(i):
    return df.iloc[i, 3]


def get_id(i):
    return df.iloc[i, 1]


def get_timesep(i):
    return df.iloc[i, 0]


app = Flask(__name__)


def initialize_db():
    conn, cursor = db_connect()

    sql = "insert into gps(timestep, id, x,y) values(%s,%s,%s,%s)"

    init_df = pd.read_csv('./dataset/dataset_01.csv')
    for i in range(485):
        init_timestep = get_timesep(i)
        init_id = get_id(i)
        init_x = get_x_value(i)
        init_y = get_y_value(i)
        # print('{}:{}:{}:{}'.format(init_timestep, init_id, init_x, init_y))
        cursor.execute(sql, (init_timestep, init_id, init_x, init_y))

    db_close(conn)


@app.route('/')
def home():
    global total_count

    conn, cursor = db_connect()

    sql = "select * from gps where timestep = %s"
    cursor.execute(sql, (total_count))

    rows = cursor.fetchall()
    leng = len(rows)
    idx_packet = 0
    temp_packet = []
    for data in rows:
        data_json = {}
        # print(data[2] + ':' + data[3] + ':' + data[4])
        data_json['ts'] = data[1]
        data_json['id'] = data[2]
        data_json['x'] = data[3]
        data_json['y'] = data[4]
        # print(data_json)
        # print(str(idx_packet))
        temp_packet.append(data_json)
        # print(temp_packet[idx_packet])
        idx_packet += 1

    # data_json['id'] = rows[2]
    # data_json['x'] = rows[3]
    # data_json['y'] = rows[4]
    print(temp_packet)
    db_close(conn)

    total_count += 1
    if total_count >= 485:
        total_count = 0
    print('total_count : {}'.format(total_count))
    return jsonify(
        id_0=temp_packet[0],
        id_1=temp_packet[1],
        id_2=temp_packet[2],
        id_3=temp_packet[3],
        id_4=temp_packet[4]
    )
    # return json.dumps(packet_json)


@app.route('/v0')
def v0():
    global v0_count
    global id_ts
    global id_data
    global value_x
    global value_y

    conn, cursor = db_connect()

    sql = "select * from dummy_gps2 where id = %s and timestep = %s"
    cursor.execute(sql, ('vehicle_0', v0_count))

    rows = cursor.fetchall()
    leng = len(rows)
    db_close(conn)
    temp_packet = []
    print(rows)
    for data in rows:
        data_json = {}
        # print(data[2] + ':' + data[3] + ':' + data[4])
        if (data[2] == 'vehicle_0'):
            print('v0_count : {}'.format(v0_count))
            id_ts = data[1]
            id_data = data[2]
            value_x = data[3]
            value_y = data[4]
            v0_count += 1
            if v0_count > 80:
                v0_count = 0

            return jsonify(
                ts=id_ts,
                data_id=id_data,
                x_value=value_x,
                y_value=value_y
            )
    # v0_count += 5
    # if v0_count > 76:
    #     v0_count = 0

    # return jsonify(
    #     ts='0',
    #     data_id='0',
    #     x_value='10',
    #     y_value='120'
    # )


@app.route('/v1')
def v1():
    global v1_count

    conn, cursor = db_connect()

    sql = "select * from dummy_gps2 where id = %s and timestep = %s"
    cursor.execute(sql, ('person_0', p0_count))

    rows = cursor.fetchall()
    leng = len(rows)
    db_close(conn)
    temp_packet = []
    print(rows)
    for data in rows:
        data_json = {}
        # print(data[2] + ':' + data[3] + ':' + data[4])
        if (data[2] == 'person_0'):
            print('person_0 : {}'.format(person_0))
            id_ts = data[1]
            id_data = data[2]
            value_x = data[3]
            value_y = data[4]
            p0_count += 1
            if p0_count > 20:
                p0_count = 0

            return jsonify(
                ts=id_ts,
                data_id=id_data,
                x_value=value_x,
                y_value=value_y
            )


def get_counter(str):
    conn, cursor = db_connect()
    sql = 'select * from counter'
    cursor.execute(sql)
    rows = cursor.fetchall()

    print(rows)


@app.route('/p0')
def p0():
    global p0_count

    # get_counter('p0')
    conn, cursor = db_connect()

    sql = "select * from dummy_gps2 where timestep = %s"
    cursor.execute(sql, (p0_count))
    # print('p0_count : {}'.format(p0_count))
    rows = cursor.fetchall()
    leng = len(rows)
    db_close(conn)
    temp_packet = []
    for data in rows:
        data_json = {}
        # print(data[2] + ':' + data[3] + ':' + data[4])
        if (data[2] == 'person_0'):
            p0_count += 1
            if p0_count > 20:
                p0_count = 0
            # print('p0_count : {}'.format(p0_count))
                # db_close(conn)
            return jsonify(
                ts=data[1],
                data_id=data[2],
                x_value=data[3],
                y_value=data[4]
            )
    p0_count += 1
    if p0_count > 20:
        p0_count = 0
        # db_close(conn)
    return jsonify(
        ts='0',
        data_id='0',
        x_value='0',
        y_value='0'
    )


@app.route('/p1')
def p1():
    global p1_count

    conn, cursor = db_connect()

    sql = "select * from gps where timestep = %s"
    cursor.execute(sql, (p1_count))

    rows = cursor.fetchall()
    leng = len(rows)

    temp_packet = []
    for data in rows:
        data_json = {}
        # print(data[2] + ':' + data[3] + ':' + data[4])
        if (data[2] == 'person_1'):
            p1_count += 1
            if p1_count >= 485:
                p1_count = 0
            print('p1_count : {}'.format(p1_count))
            return jsonify(
                ts=data[1],
                data_id=data[2],
                x_value=data[3],
                y_value=data[4]
            )
    p1_count += leng
    if p1_count >= 485:
        p1_count = 0

    return jsonify(
        ts='0',
        data_id='0',
        x_value='0',
        y_value='0'
    )


@app.route('/p2')
def p2():
    global p2_count

    conn, cursor = db_connect()

    sql = "select * from gps where timestep = %s"
    cursor.execute(sql, (p2_count))

    rows = cursor.fetchall()
    leng = len(rows)

    temp_packet = []
    for data in rows:
        data_json = {}
        # print(data[2] + ':' + data[3] + ':' + data[4])
        if (data[2] == 'person_2'):
            p2_count += 1
            if p2_count >= 485:
                p2_count = 0
            print('p2_count : {}'.format(p2_count))
            return jsonify(
                ts=data[1],
                data_id=data[2],
                x_value=data[3],
                y_value=data[4]
            )
    p2_count += leng
    if p2_count >= 485:
        p2_count = 0

    return jsonify(
        ts='0',
        data_id='0',
        x_value='0',
        y_value='0'
    )


@app.route('/p2tx', methods=['GET'])
def p2tx():
    global p0_count

    tx_id = request.args.get('id', 'person_0')
    tx_x_value = request.args.get('x_value', '36.380727')
    tx_y_value = request.args.get('y_value', '127.365615')
    print("got data:")
    print(tx_id + ' : ' + tx_x_value + ' : ' + tx_y_value)

    conn, cursor = db_connect()

    sql = "INSERT INTO dummy_gps (timestep, id, x,y) values(%s,%s,%s,%s)"
    cursor.execute(sql, (p0_count, tx_id, tx_x_value, tx_y_value))
    db_close(conn)
    p0_count += 1

    return "success!"


if __name__ == '__main__':

    # conn, cursor = db_connect()

    # sql = "SELECT * FROM gps"
    # res = db_execute_quiry(cursor, sql)
    # for data in res:
    #     print(data)
    # print(type(data))

    # db_close(conn)

    app.run(host='0.0.0.0', port=8080)
