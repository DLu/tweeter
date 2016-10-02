from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('tweet.html')

@app.route('/interact')
def interact():
    try:
        return jsonify(id='779659915510046720')
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run()