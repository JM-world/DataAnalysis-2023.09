import os   # 이미지 파일 열기
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')     # localhost:5000/ 을 서비스하기 위한 코드
def index():
    return '<h1>Static Resource</h2>'

@app.route('/static')
def static_resource():
    print(app.root_path)        # D:/WorkSpace/02.DataAnalysis/07.FlaskWeb
    # static resource가 cache로 인하여 즉시 변경이 안되는 경우도 있음
    img_file = os.path.join(app.root_path, 'static/img/고양이1.jpg')
    mtime = int(os.stat(img_file).st_mtime)      # 마지막으로 변경된 시간
    return render_template('04.static.html')

if __name__ == '__main__':
    app.run(debug=True)