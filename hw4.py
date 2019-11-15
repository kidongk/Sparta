import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.mydb

## HTML을 주는 부분

@app.route('/')
def home():
   return render_template('hw4.html')


## API 역할을 하는 부분
@app.route('/shop', methods=['POST'])
def order():
    item_receive = request.form['item_give']  # 클라이언트로부터 comment를 받는 부분
    name_receive = request.form['name_give']  # 클라이언트로부터 url을 받는 부분
    count_receive = request.form['count_give']  # 클라이언트로부터 comment를 받는 부분
    address_receive = request.form['address_give']  # 클라이언트로부터 comment를 받는 부분
    phone_receive = request.form['phone_give']  # 클라이언트로부터 comment를 받는 부분
    order = {'name': name_receive, 'count': count_receive, 'address': address_receive, 'phone': phone_receive,
               'item': item_receive}
    db.orders.insert_one(order)
    return jsonify({'result': 'success'})

@app.route('/shop', methods=['GET'])
def call():
    item_receive = request.args.get('item_give')  # 클라이언트로부터 comment를 받는 부분
    order = list(db.orders.find({'item': item_receive}, {'_id': False}))
    return jsonify({'result': 'success', 'orders': order})

if __name__ == '__main__':
   app.run('127.0.0.1',port=5000,debug=True)
