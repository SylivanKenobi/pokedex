from PIL import Image as PImage
from PIL import ImageFilter
import requests
import json
import urllib.request

class Image:

    def __init__(self, id, generation='none', game='none'):
        self.id = id
        self.generation = generation
        self.game = game
        self.content = self.fetch()

    def fetch(self):
        pokemon = requests.get('https://pokeapi.co/api/v2/pokemon/4').json()
        image_url = pokemon.get("sprites").get("front_default")
        urllib.request.urlretrieve(image_url, 'image.png')
        image = PImage.open('image.png')
        width, height = image.size
        left = 18
        top = height / 4
        right = 70
        bottom = 3 * height / 4
        image = image.crop((left, top, right, bottom))
        image = image.resize((26,20))
        image = image.convert('RGB')
        return image

    def get_raw_data(self):
        return self.content.getdata()

# image = get_image()
# width, height = image.size
# left = 18
# top = height / 4
# right = 70
# bottom = 3 * height / 4
# image = image.crop((left, top, right, bottom))
# image = image.resize((26,20))
# image = image.convert('RGB')        



# def get_image():
#     pokemon = requests.get('https://pokeapi.co/api/v2/pokemon/4').json()
#     image_url = pokemon.get("sprites").get("front_default")
#     urllib.request.urlretrieve(image_url, 'image.png')
#     return Image.open('image.png')