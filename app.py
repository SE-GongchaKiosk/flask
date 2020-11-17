from flask import Flask, render_template, request
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('localhost', 27017) # mongoDB의 27017 포트로 들어감
db = client.dbgongcha   # 'dbgongcha'라는 이름의 db 생성


## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')

## API 역할을 하는 부분
@app.route('/urlexample', methods=['POST'])

@app.route('/urlexample', methods=['GET'])


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
