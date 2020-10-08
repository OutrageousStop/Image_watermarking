import os
from flask import Flask, flash, request, redirect, url_for, send_file, render_template
from werkzeug.utils import secure_filename
import watermark_util
dirname = os.path.dirname(__file__)
print(os.path.join(dirname, '/result/hello'))
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)

@app.route('/embed_image', methods=['GET', 'POST'])
def embed_image():
    if request.method == 'POST':
        original_image = request.files['original_image']
        watermark_image = request.files['watermark_image']
        original_image.save('./temp/original_image')
        watermark_image.save('./temp/watermark_image')
        watermark_util.w2d()
        return send_file(os.path.join(dirname, 'result/image_with_watermark.jpg'))

@app.route('/embed', methods=['GET'])
def embed():
    return render_template('Embed_image.html')

@app.route('/', methods=['GET'])
def Landing_page():
    return render_template('Landing_page.html')

@app.route('/extract', methods=['GET'])
def extract():
    return render_template('Decode_image.html')

@app.route('/extract_image', methods=['GET', 'POST'])
def extract_image():
    if request.method == 'POST':
        image = request.files['image']
        image.save('./temp/toextractfrom')
        watermark_util.extractWM('toextractfrom')
        return send_file('./result/recovered_watermark.jpg')
    return "hello"


if __name__ == "__main__":
    app.run(debug=True)