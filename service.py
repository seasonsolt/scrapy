from flask import Flask, jsonify
from flask.ext.cors import CORS
import pymysql

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return "Hello, World!"


@app.route('/scrapy/get/curr', methods=['GET'])
def get_curr():
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='scrapy', charset="utf8")
    cursor = conn.cursor()

    sql = "select * from currency_rate where batch_no=(select max(batch_no) from currency_rate)"
    cursor.execute(sql)
    items = []
    currItem = {
        'currency': cursor._rows[0][2],
        'statisTime': cursor._rows[0][6].strftime("%Y-%m-%d:%H:%M:%S"),
        'refPrice': cursor._rows[0][3]
    }
    for r in cursor:
        print(r)
        if 'currency'  not in currItem or currItem['currency'] == '' or currItem['currency'] != r[2]:
            items.append(currItem)
            currItem = {
                'currency': r[2],
                'statisTime': r[6].strftime("%Y-%m-%d:%H:%M:%S"),
                'refPrice': r[3]
            }
        if r[5] == '中间价':
            currItem['midPrice'] = r[4]
        elif r[5] == '钞买价':
            currItem['cpBuyPrice'] = r[4]
        elif r[5] == '汇买价':
            currItem['excBuyPrice'] = r[4]
        elif r[5] == '钞/汇卖价':
            currItem['cpExcSalePrice'] = r[4]

    # 提交
    conn.commit()
    # 关闭游标
    cursor.close()
    # 关闭连接
    conn.close()
    return jsonify({"data":items})


if __name__ == '__main__':
#    app.run(debug=False)
    app.run(host='0.0.0.0', port=5000)
