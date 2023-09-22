from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')     
def index():
    return '<h1>Template</h2>'

@app.route('/hello')
@app.route('/hello/<name>')
def hello(name=None):       # name값을 주면 그 값이 되고, 안주면 None
    dt = {'key1':'value1', 'key2':'value2', 'key3':'value3'}
    return render_template('05.template.html', name=name, dt=dt)

if __name__ == '__main__':
    app.run(debug=True)