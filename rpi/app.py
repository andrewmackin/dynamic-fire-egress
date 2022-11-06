from flask import Flask, request

app = Flask(__name__)

@app.route('/alert', methods=['POST'])
def webhook():
    if request.method == 'POST':
        print("Data received from Webhook for alerting is: ", request.json)
        return "Alert received"

app.run(host='0.0.0.0', port=8000)