from process import MainProcess
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/college', methods=['POST'])
def get_college_input():
    college_input = request.form['college_input']
    a = MainProcess(college_input)
    output = a.get_number()
    result1 = output[0]
    result2 = output[1]
    acaTitles, acaPosts, nonAcaTitles, nonAcaPosts = a.get_posts()
    return render_template('main.html', result1=result1, result2=result2, acaTitles = acaTitles, acaPosts = acaPosts, nonAcaTitles = nonAcaTitles, nonAcaPosts = nonAcaPosts)

if __name__ == '__main__':
    app.run(debug=True)




