from flask import Flask, render_template, request
from pymongo import MongoClient


from flask import render_template, request, flash, redirect, url_for



app = Flask(__name__)

client = MongoClient('localhost', 27017) # mongoDB의 27017 포트로 들어감
client = client.dbgongcha   # 'dbgongcha'라는 이름의 db 생성
db = client['dbgongcha'] # 공처 db뭉치 가져오기
menu_collection = db['menu'] #menu collection 불러오기


## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')

## API 역할을 하는 부분
@app.route('/menu/login')
def manager_login():
    pass
    # return render_template('index.html', note=note)


@app.route('/menu', methods=['POST', 'GET'])
def show_menu():
    menu = db.menu_collection.find()
    return render_template('menu.html', menu = menu)

# 노트 생성
@app.route('/menu/add', methods=['POST', 'GET'])
def add_menu():
    if request.method == 'POST':
        db.menu_collection.insertOne({
            # "_id" : "gdhong",
            "카테고리" : request.form['category'],
            "상품명" : request.form['title'],
            "금액" : request.form['price']
            })
                    
        return redirect(url_for('show_menu'))

    return render_template('add.html')


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
