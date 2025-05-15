from flask import Flask, request, render_template
from Crypto.Cipher import AES
import base64
import hashlib

app = Flask(__name__)

def pad(text):
    while len(text) % 16 != 0:
        text += ' '
    return text

def encrypt(text, key):
    key = hashlib.sha256(key.encode()).digest()
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted = cipher.encrypt(pad(text).encode())
    return base64.b64encode(encrypted).decode()

def decrypt(encrypted_text, key):
    try:
        key = hashlib.sha256(key.encode()).digest()
        cipher = AES.new(key, AES.MODE_ECB)
        decrypted = cipher.decrypt(base64.b64decode(encrypted_text))
        return decrypted.decode().rstrip()
    except:
        return "Lỗi giải mã: kiểm tra lại khóa hoặc dữ liệu!"

@app.route("/")
def home():
    return render_template("index.html", result="")

@app.route("/encrypt", methods=["POST"])
def encrypt_route():
    text = request.form["text"]
    key = request.form["key"]
    result = encrypt(text, key)
    return render_template("index.html", result=result)

@app.route("/decrypt", methods=["POST"])
def decrypt_route():
    text = request.form["text"]
    key = request.form["key"]
    result = decrypt(text, key)
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
