import flask
import os
import json
import hashlib
import time
import threading
from flask import request, jsonify


app = flask.Flask("图床")

bighash = set()
# f = open("data.txt", "a")
lock = threading.Lock()

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        byte = file.read()
        md5 = hashlib.md5(byte).hexdigest()
        with lock:
            if md5 not in bighash:
                open(f"upload/{md5}.jpg", "wb").write(byte)
            bighash.add(md5)
        return jsonify({'msg': '上传成功', "url": f"http://{request.host}/upload/{md5}.jpg"})
    else:
        return jsonify({'msg': '上传失败'})

@app.route('/upload/<md5>', methods=['GET'])
@app.route('/upload/<md5>.jpg', methods=['GET'])
@app.route('/upload/<md5>.png', methods=['GET'])
def get(md5):
    if md5 in bighash:
        return flask.send_file(f"upload/{md5}.jpg")
    else:
        return jsonify({'msg': '获取失败'})
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)