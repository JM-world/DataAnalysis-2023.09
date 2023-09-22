from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')     # localhost:5000/ 을 서비스하기 위한 코드
def index():
    return '<h1>파라메터 전달값 받기</h>'

# localhost:5000/area?pi=3.14&radius=10 <옛날식>
@app.route('/area')
def hello():
    pi = request.args.get('pi', '3.14159')      # default 값을 지정할 수 있음
    radius = request.values['radius']           # GET/POST 모두 사용할 수 있음
    result = float(pi) * float(radius) ** 2
    return f'<h1>pi={pi}, radius={radius}, area={result}</h1>'

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('/02.login.html')
    else:
        uid = request.form['uid']
        pwd = request.form['pwd']
        return f'<h1>uid={uid}, pwd={pwd} 환영합니다.</h1>'

@app.route('/sample', methods=['GET','POST'])
def sample():
    if request.method == 'GET':
        return render_template('/02.sample.html')
    else:
        a = request.form['a']
        b = request.form['b']
        result = int(a) * int(b)
        return f'<h1>a={a}, b={b}, a * b = {result}</h1>'

# localhost:5000/user/james, localhost:5000/user/maria
@app.route('/user/<uname>') # 꺽새 반드시 넣어야함
def user(uname):
    return f'<h1>uname={uname}</h1>'

# localhost:5000/square/12
@app.route('/square/<int:number>')      # int로 바로 변환
def square(number):
    return f'<h1>{number} ** 2 = {number ** 2}</h1>'

# localhost:5000/circle/3.14
@app.route('/circle/<float:pi>/and/<float:radius>')
def circle(pi, radius):
    result = pi * radius ** 2
    return f'<h1>pi={pi}, radius={radius}, area={result}</h1>'

if __name__ == '__main__':
    app.run(debug=True)