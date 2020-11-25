from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

client = MongoClient('localhost', 27017) # mongoDB의 27017 포트로 들어감
db = client.dbGongchaTest   # 'dbgongcha'라는 이름의 db 생성

db.orderCount.delete_many({})
db.orderCount.insert_one({'order_count': 1})

## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')

## API 역할을 하는 부분
@app.route('/order', methods=['GET', 'POST'])
def make_order():
    if request.method == 'POST':
        order_menu = request.form['menu_give']  # [menu_name, menu_options, menu_count, menu_price]
        order_price = request.form['price_give']  # total_price

        order_count = db.orderCount.find_one({}, {'_id': 0})
        order_number = order_count['order_count']  # 주문 번호

        order_date = str(datetime.today().date())
        order_time = datetime.today()  # 주문 날짜

        order_state = False  # 주문 처리 상태

        order = {'order_number': order_number, 'order_date': order_date, 'order_time': order_time, 'order_menu': order_menu,
                 'order_price': order_price, 'order_state': order_state}

        db.order.insert_one(order)

        return jsonify({'result': 'success'})

    elif request.method == 'GET':
        order_count = db.orderCount.find_one({}, {'_id': 0})
        order_number = order_count['order_count']
        order_date = str(datetime.today().date())

        result = db.order.find_one({'$and': [{'order_number': order_number},{'order_date': order_date}]},
            {'_id': 0, 'order_number': 0, 'order_date': 0, 'order_time': 0, 'order_menu': 0, 'order_state': 0})

        return jsonify({'result': 'success', 'order_price': result})

@app.route('/pay', methods=['GET', 'POST'])
def pay_order():
    if request.method == 'POST':
        order_count = db.orderCount.find_one({}, {'_id': 0})
        order_number = order_count['order_count']
        order_date = str(datetime.today().date())
        order_time = datetime.today()

        discount_cost = request.form['discount_give']  # 할인 금액
        pay_cost = request.form['pay_give']  # 결제 금액 (메뉴 가격 - 할인 금액)

        pay = {'order_number': order_number, 'order_date': order_date, 'order_time': order_time, 'discount_cost': discount_cost, 'pay_cost': pay_cost}

        db.pay.insert_one(pay)

        return jsonify({'result': 'success'})

    elif request.method == 'GET':
        order_count = db.orderCount.find_one({}, {'_id': 0})
        order_number = order_count['order_count']
        order_date = str(datetime.today().date())

        result = db.pay.find_one({'$and': [{'order_number': order_number}, {'order_date': order_date}]},
                                 {'_id': 0, 'order_number': 0, 'order_date': 0, 'order_time': 0, 'discount_cost': 0})

        return jsonify({'result': 'success', 'pay_cost': result})

@app.route('/finish', methods=['GET'])
def finish_order():
    # 1. orderCount DB에서 order_number 값 조회해오기(Read)
    order_count = db.orderCount.find_one({}, {'_id': 0})
    order_number = order_count['order_count']

    # 2. orderCount DB 1만큼 업데이트 해주기
    order_count_update = order_number + 1
    db.orderCount.update_one({}, {'$set': {'order_count': order_count_update}})

    return jsonify({'result': 'success', 'order_number': order_number})

@app.route('/payments', methods=['GET', 'POST'])
def manage_payments():
    if request.method == 'POST':
        order_date = request.form['date_give']

        # 1. order DB에서 order_date에 해당하는 값 가져오기
        order_db = list(db.order.find({'order_date': order_date}, {'_id': 0, 'order_state': 0}))

        for order in order_db:
            number = order['order_number']
            time = order['order_time']
            menu = order['order_menu']
            price = order['order_price']
            discount = 0
            pay = 0

            payments = {'order_number': number, 'order_time': time, 'order_menu': menu, 'order_price': price, 'discount_cost': discount,
                        'pay_cost': pay}
            db.payments.insert_one(payments)

        # 2. pay DB에서 order_date에 해당하는 값 가져오기
        pay_db = list(db.pay.find({'order_date': order_date}, {'_id': 0}))

        for pay in pay_db:
            number = pay['order_number']
            discount = pay['discount_cost']
            pay = pay['pay_cost']

            db.payments.update_one({'order_number': number}, {'$set': {'discount_cost': discount, 'pay_cost': pay}})

        return jsonify({'result': 'success'})

    elif request.method == 'GET':
        # 1. payments DB에서 결제내역 리스트 읽어오기
        result = list(db.payments.find({}, {'_id': 0}))

        # 2. payments라는 키 값으로 결제내역 리스트 보내주기
        return jsonify({'result': 'success', 'payments': result})

@app.route('/sales', methods=['GET', 'POST'])
def manage_sales():
    if request.method == 'POST':
        start_date = request.form['start_give']
        end_date = request.form['end_give']

        start_year = start_date[0]
        start_month = start_date[1]
        start_day = start_date[2]

        end_year = end_date[0]
        end_month = end_date[1]
        end_day = end_date[2]

        start = datetime(start_year, start_month, start_day)
        end = datetime(end_year, end_month, end_day)

        total_order = db.order.count_documents({'order_time': {'$gte': start, '$lt': end}})

        orders = list(db.order.find({'order_time': {'$gte' : start, '$lt' : end}}))
        total_price = 0
        for order in orders:
            order_price = order['order_price']
            total_price += order_price

        pays = list(db.pay.find({'order_time': {'$gte' : start, '$lt' : end}}))
        total_discount = 0
        total_pay = 0
        for pay in pays:
            discount_cost = pay['discount_cost']
            pay_cost = pay['pay_cost']
            total_discount += discount_cost
            total_pay += pay_cost

        sales = {'total_order': total_order, 'total_price': total_price, 'total_discount': total_discount, 'total_pay': total_pay}
        db.sales.insert_one(sales)

        return jsonify({'result': 'success'})

    elif request.method == 'GET':
        # 1. sales DB에서 매출내역 리스트 읽어오기
        result = db.sales.find_one({}, {'_id': 0})

        # 2. sales라는 키 값으로 결제내역 리스트 보내주기
        return jsonify({'result': 'success', 'sales': result})


@app.route('/check', methods=['GET', 'POST'])
def check_order():
    if request.method == 'POST':
        number_receive = request.form['number_give']
        db.order.update_one({'order_number': number_receive}, {'$set': {'order_state': True}})

        return jsonify({'result': 'success'})

    elif request.method == 'GET':
        result = list(db.order.find({'order_state': False}, {'_id': 0, 'order_date': 0, 'order_time': 0, 'order_price': 0, 'order_state': 0}))

        return jsonify({'result': 'success', 'order_list': result})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

