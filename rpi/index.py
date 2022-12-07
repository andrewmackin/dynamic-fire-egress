from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/alert', methods=['POST'])
def webhook():
  print("Data received from Webhook for alerting is: ", request.json)
  return jsonify(
    { 'testResponse': 'alerted!', 'status': 200 }
  )

app.run(host='localhost', port=8101)