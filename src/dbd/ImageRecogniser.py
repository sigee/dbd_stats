import base64
import os
import tensorflow as tf
import numpy
import random
import string

from io import BytesIO
from PIL import Image, ImageDraw


DEBUG = os.environ.get('DEBUG', 'false').lower() in ('true', '1', 't')


class DbdImageRecogniser:
    PERKS_IMAGE_SHAPE = (49, 49)
    KILLERS_IMAGE_SHAPE = (40, 40)
    ESCAPES_IMAGE_SHAPE = (60, 50)
    model = None
    class_names = []
    category = ''

    def __init__(self, category):
        self.category = category
        if category == 'killers':
            self.IMAGE_SHAPE = self.KILLERS_IMAGE_SHAPE
        elif category == 'perks':
            self.IMAGE_SHAPE = self.PERKS_IMAGE_SHAPE
        elif category == 'escapes':
            self.IMAGE_SHAPE = self.ESCAPES_IMAGE_SHAPE
        else:
            self.IMAGE_SHAPE = (1, 1)

        self.model = tf.keras.models.load_model('saved_model/dbd_' + category + '/')
        with open('saved_model/dbd_' + category + '/saved_labels.txt', 'r', encoding='utf-8') as txt_file:
            file_content = txt_file.read()
            self.class_names = file_content.splitlines()

    def get_text(self, image_path):
        img = tf.keras.utils.load_img(image_path, target_size=self.IMAGE_SHAPE)
        img_array = tf.keras.utils.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0)

        predictions = self.model.predict(img_array, verbose=0)
        score = tf.nn.softmax(predictions[0])

        return self.class_names[numpy.argmax(score)]

    def image_to_text(self, cropped_img):
        cropped_img.save(self.category + ".png")
        text = self.get_text(self.category + ".png")

        img = ''
        if DEBUG:
            if self.category != 'escapes':
                with Image.open(self.category + ".png") as image:
                    buffered = BytesIO()
                    image = image.convert("RGB")
                    image.save(buffered, format="JPEG")
                    base64encoded = base64.b64encode(buffered.getvalue()).decode('utf-8')
                    img = '<img src="data:image/jpg;base64,' + base64encoded + '" />'

        os.remove(self.category + ".png")
        if DEBUG:
            cropped_img = cropped_img.convert("RGB")
            path = '../debug/' + self.category + '/' + text
            os.makedirs(path, exist_ok=True)
            cropped_img.save('../debug/' + self.category + '/' + text + '/' + self._get_random_string(8) + '.jpg',
                             quality=100)

        return text, img

    @staticmethod
    def _get_random_string(length):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for _ in range(length))


class PerkRecogniser(DbdImageRecogniser):
    PERK_COORDINATES = [
        (192, 770, 241, 819),
        (247, 770, 296, 819),
        (302, 770, 351, 819),
        (357, 770, 406, 819)
    ]

    def __init__(self):
        super().__init__('perks')

    def get_perk_text(self, original_image, perk_id):
        perk_img = original_image.crop(self.PERK_COORDINATES[perk_id - 1])
        perk_img = self._clean_perk_background(perk_img)
        return self.image_to_text(perk_img)

    @staticmethod
    def _clean_perk_background(img):
        draw = ImageDraw.Draw(img)
        draw.polygon([(0, 0), (0, 25), (25, 0)], fill=(0, 0, 0))
        draw.polygon([(25, 0), (50, 0), (50, 25)], fill=(0, 0, 0))
        draw.polygon([(0, 25), (0, 50), (25, 50)], fill=(0, 0, 0))
        draw.polygon([(50, 25), (50, 50), (25, 50)], fill=(0, 0, 0))
        return img


class KillerRecogniser(DbdImageRecogniser):
    def __init__(self):
        super().__init__('killers')

    def get_killer_text(self, original_image):
        cropped_img = original_image.crop((489, 776, 529, 816))
        return self.image_to_text(cropped_img)


class EscapeRecogniser(DbdImageRecogniser):
    ESCAPE_COORDINATES = [
        (898, 310, 958, 360),
        (898, 427, 958, 477),
        (898, 543, 958, 593),
        (898, 661, 958, 711)
    ]

    def __init__(self):
        super().__init__('escapes')

    def get_survivor_statuses(self, original_image):
        survivor1_status_text, _ = self._get_escape_text(original_image, 1)
        survivor2_status_text, _ = self._get_escape_text(original_image, 2)
        survivor3_status_text, _ = self._get_escape_text(original_image, 3)
        survivor4_status_text, _ = self._get_escape_text(original_image, 4)
        survivor_statuses = [survivor1_status_text, survivor2_status_text, survivor3_status_text, survivor4_status_text]
        return survivor_statuses

    def _get_escape_text(self, original_image, escape_id):
        cropped_img = original_image.crop(self.ESCAPE_COORDINATES[escape_id - 1])
        return self.image_to_text(cropped_img)
