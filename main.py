import numpy as np
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from PIL import Image
import imageio
import requests
from collections import Counter
import matplotlib

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

API_ENDPOINT = 'https://www.thecolorapi.com/id'

class ColorRow:
    def __init__(self, color, percent):
        self.color = color
        self.percent = percent


def convert_to_hex(image_path):
    img = imageio.imread(image_path)
    hex = []
    for dim in img:
        for row in dim:
            row = row/255
            new_hex = matplotlib.colors.to_hex(row, keep_alpha=False)
            hex.append(new_hex)
    return hex


def find_most_common(hex):
    occurence_count = Counter(hex)
    most_common = occurence_count.most_common(10)
    return most_common


class ImageForm(FlaskForm):
    image = StringField("Pathway to image file", validators=[DataRequired()])
    submit = SubmitField("Find Colors")


@app.route('/', methods=['GET', 'POST'])
def home():
    form = ImageForm()
    if request.method == 'POST':
        image_path = request.form.get("image")
        hex = convert_to_hex(image_path)
        pixel_count = len(hex)
        most_common = find_most_common(hex)
        colors = [color[0] for color in most_common]
        percents = [((color[1]/pixel_count)*100) for color in most_common]

        color_rows = []
        for item in range(10):
            color_row = ColorRow(colors[item], percents[item])
            color_rows.append(color_row)

        return render_template('index.html', form=form, image=image_path, color_rows=color_rows)

    return render_template('index.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)