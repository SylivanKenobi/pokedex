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
        image = PImage.open('image.png').convert('RGB')
        image = self.crop_height(np.asarray(image))
        image = self.crop_width(image)
        image = self.resize(image, image.size)
        return image.convert('RGB')

    def get_raw_data(self):
        return self.content.getdata()

    def resize(self, image, size):
        width, height = size
        max_width, max_height = (25, 22)

        factor_width = max_width/float(width)
        factor_height = max_height/float(height)

        crop_factor = factor_width if factor_width < factor_height else factor_height
        new_height,new_width = int(height*crop_factor),int(width*crop_factor)

        return image.resize((new_width, new_height))

    def crop_height(self, image):
        non_zero_list = []
        for index, stuff in enumerate(image):
            if len(np.unique(stuff)) > 1:
                non_zero_list.append(index)
        image = np.delete(image, range(0, non_zero_list[0] - 1),0)
        image = np.delete(image, range(non_zero_list[-1] - non_zero_list[0], len(image)),0)
        return PImage.fromarray(image, 'RGB')

    def crop_width(self, image):
        image = np.asarray(image)
        image = np.rot90(image, 3)
        non_zero_list = []
        for index, stuff in enumerate(image):
            unique = np.unique(stuff)
            if len(unique) == 1 and unique[0] == 0:
                bla = 'asdf'
            else:
                non_zero_list.append(index)
        image = np.delete(image, range(0, non_zero_list[0]),0)
        image = np.delete(image, range(non_zero_list[-1] - non_zero_list[0], len(image)),0)
        image = np.rot90(image, 1)
        return PImage.fromarray(image, 'RGB')
