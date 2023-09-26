from flask import Flask, render_template, request
import os

app = Flask(__name__)

@app.route('/')
def index():
    return '<h2>인터파크</h2>'

@app.route('/interpark', methods=['GET','POST'])
def interpark():
    if request.method == 'GET':
        return render_template('/98.interpark_form.html')
    else:
        file_image = request.files['image']
        fname = file_image.filename            # 업로드한 파일 이름
        filename = os.path.join(app.static_folder, f'interpark/{fname}')
        file_image.save(filename)
        return render_template('11.file_res.html', fname=f'interpark/{fname}')
        

if __name__ == '__main__':
    app.run(debug=True)