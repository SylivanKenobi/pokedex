from PIL import Image as PImage
from PIL import ImageFilter
import requests
import json
import urllib.request
import numpy as np

class Image:

    def __init__(self, id, generation='none', game='none'):
        self.id = id
        self.generation = generation
        self.game = game
        self.content = self.fetch()

    def fetch(self):
        pokemon = requests.get(f'https://pokeapi.co/api/v2/pokemon/{self.id}').json()
        image_url = pokemon.get("sprites").get("front_default")
        urllib.request.urlretrieve(image_url, 'image.png')
        image = PImage.open('image.png')
        left = 18
        top, bottom = self.crop_height(np.asarray(image))
        right = 70
        image = image.crop((left, top, right, bottom))
        print(image.getbbox())
        image = self.resize(image, image.size)
        image = image.convert('RGB')
        return image

    def get_raw_data(self):
        return self.content.getdata()

    def resize(self, image, size):
        width = size[0]
        height = size[1]
        max_width = 25
        max_height = 22
        new_height = int((height / width) * max_width)
        return image.resize((max_width, new_height))

# WIP resize array
    def crop_height(self, image):
        non_zero_list = []
        for i in image:
            if len(set(i)) > 1:
                non_zero_list.append(i)
        # upper = ((non_zero_list[0] - height) / height) - 2
        # lower = (non_zero_list[-1] / height) + 10
        PImage.fromarray(image[non_zero_list[0]:non_zero_list[-1]], 'RGB').show()
        return upper, lower
