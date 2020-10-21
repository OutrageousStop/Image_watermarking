import os
from flask import Flask, flash, request, redirect, url_for, send_file, render_template
from werkzeug.utils import secure_filename
import watermarking_color_util

dirname = os.path.dirname(__file__)
# print(os.path.join(dirname, '/result/hello'))

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)

@app.route('/embed_image', methods=['GET', 'POST'])
def embed_image():
    if request.method == 'POST':
        original_image = request.files['original_image']
        watermark_image = request.files['watermark_image']
        x_axis = int(request.form["x_axis"])
        y_axis = int(request.form["y_axis"])
        print(x_axis, y_axis)
        watermarking_color_util.x_axis = x_axis
        watermarking_color_util.y_axis = y_axis
        original_image.save('./temp/original_image')
        watermark_image.save('./temp/watermark_image')
        Type = int(request.form["type"])
        if Type == 0:
            watermarking_color_util.greywatermark('./temp/original_image', './temp/watermark_image')
        elif Type == 1:
            component = str(request.form["Component"])
            watermarking_color_util.singleComponentwatermark('./temp/original_image', './temp/watermark_image', component)
        else:
            watermarking_color_util.allComponentwatermark('./temp/original_image', './temp/watermark_image')

        return send_file(os.path.join(dirname, 'result/image_with_watermark.jpeg'), as_attachment=True)

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
        x_axis = int(request.form["x_axis"])
        y_axis = int(request.form["y_axis"])
        print(x_axis, y_axis)
        watermarking_color_util.x_axis = x_axis
        watermarking_color_util.y_axis = y_axis
        image.save('./temp/toextractfrom')
        Type = int(request.form["type"])

        if Type == 0:
            watermarking_color_util.extractFromgrey('./temp/toextractfrom')
        elif Type == 1:
            component = str(request.form["Component"])
            watermarking_color_util.extractFromSingleComponent('./temp/toextractfrom', component)
        else:
            watermarking_color_util.extractFromColorImage('./temp/toextractfrom')

        return send_file('./result/recovered_watermark.jpeg', as_attachment=True)
    return "hello"


if __name__ == "__main__":
    app.run(debug=True)