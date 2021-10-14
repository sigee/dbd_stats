from flask import Flask, render_template, request
from PIL import Image
import os
import random
import string
import csv

from dbd.ImageRecogniser import DbdImageRecogniser

app = Flask(__name__)


@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')


@app.route("/", methods=['POST'])
def post_index():
    uploaded_files = request.files.getlist("screenshots[]")
    data = {'rows': []}
    image_recogniser = DbdImageRecogniser()

    for file in uploaded_files:
        file.save('uploaded.file')
        original_image = Image.open('uploaded.file')

        rank_text = get_rank_text(original_image, image_recogniser)
        perk1_text = get_perk1_text(original_image, image_recogniser)
        perk2_text = get_perk2_text(original_image, image_recogniser)
        perk3_text = get_perk3_text(original_image, image_recogniser)
        perk4_text = get_perk4_text(original_image, image_recogniser)
        killer_text = get_killer_text(original_image, image_recogniser)

        survivor_statuses = get_survivor_statuses(original_image, image_recogniser)

        escaped = survivor_statuses.count('escaped')
        died = survivor_statuses.count('died')
        killed = survivor_statuses.count('killed')
        disconnected = survivor_statuses.count('disconnected')

        row = {'killer': killer_text, 'rank': rank_text, 'perk1': perk1_text, 'perk2': perk2_text,
               'perk3': perk3_text, 'perk4': perk4_text, 'escaped': escaped, 'died': died, 'killed': killed,
               'disconnected': disconnected}

        with open(r'/data/stats.csv', 'a+', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(list(row.values()))

        data['rows'].append(row)
        os.remove('uploaded.file')


    return render_template('index.html', data=data)


def get_survivor_statuses(original_image, image_recogniser):
    survivor1_status = get_survivor1_text(original_image, image_recogniser)
    survivor2_status = get_survivor2_text(original_image, image_recogniser)
    survivor3_status = get_survivor3_text(original_image, image_recogniser)
    survivor4_status = get_survivor4_text(original_image, image_recogniser)
    survivor_statuses = [survivor1_status, survivor2_status, survivor3_status, survivor4_status]
    return survivor_statuses


def get_survivor1_text(original_image, image_recogniser):
    cropped_img = original_image.crop((810, 295, 870, 345))
    return image_to_text('survivor', cropped_img, image_recogniser)


def get_survivor2_text(original_image, image_recogniser):
    cropped_img = original_image.crop((810, 407, 870, 457))
    return image_to_text('survivor', cropped_img, image_recogniser)


def get_survivor3_text(original_image, image_recogniser):
    cropped_img = original_image.crop((810, 519, 870, 569))
    return image_to_text('survivor', cropped_img, image_recogniser)


def get_survivor4_text(original_image, image_recogniser):
    cropped_img = original_image.crop((810, 628, 870, 678))
    return image_to_text('survivor', cropped_img, image_recogniser)


def get_killer_text(original_image, image_recogniser):
    cropped_img = original_image.crop((480, 740, 530, 795))
    return image_to_text('killer', cropped_img, image_recogniser)


def get_perk4_text(original_image, image_recogniser):
    cropped_img = original_image.crop((345, 740, 405, 795))
    return image_to_text('perk', cropped_img, image_recogniser)


def get_perk3_text(original_image, image_recogniser):
    cropped_img = original_image.crop((290, 740, 355, 795))
    return image_to_text('perk', cropped_img, image_recogniser)


def get_perk2_text(original_image, image_recogniser):
    cropped_img = original_image.crop((235, 740, 295, 795))
    return image_to_text('perk', cropped_img, image_recogniser)


def get_perk1_text(original_image, image_recogniser):
    cropped_img = original_image.crop((180, 740, 240, 795))
    return image_to_text('perk', cropped_img, image_recogniser)


def get_rank_text(original_image, image_recogniser):
    cropped_img = original_image.crop((80, 700, 180, 810))
    return image_to_text('rank', cropped_img, image_recogniser)


def image_to_text(category, cropped_img, image_recogniser):
    cropped_img.save(category + ".png")
    text = image_recogniser.get_text(category + ".png")

    os.remove(category + ".png")
    if text == 'N/A':
        cropped_img = cropped_img.convert("RGB")
        cropped_img.save(category + '_issue/' + get_random_string(8) + '.jpg', quality=100)
    return text


def get_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))
