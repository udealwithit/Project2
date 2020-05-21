from flask import Flask, json, jsonify
from flask import request

api = Flask(__name__)

@api.route('/quality', methods=['GET'])
def get_companies():
	return "Hello World"

@api.route('/collect/quality', methods=['POST'])
def store_air_quality():
	print(request.get_json())
	return jsonify({"Hi":"Hello"})

if __name__ == "__main__":
	api.run(host="0.0.0.0", port="8443")