from flask import Flask,request,jsonify

app = Flask(__name__)

@app.route("/jsonExample",methods=['POST'])
def hello():
    message = request.get_json(force=True)
    name = message['name']
    response = {'getting':'hello ' +name+'!'}
    return jsonify(response)