import requests
import json
from PIL import Image
from PIL import ImageFilter
import urllib.request
import climage
import pokebase

charmander = pokebase.pokemon('4')

def create_canvas():
    canvas = []
    for height in range(20):
        line = []
        for width in range(80):
            if width >= 40:
                line.append(210)
            else:
                line.append(0)
        canvas.append(line)
    return canvas

def print_color(fg=0, bg=255, text=" "):
    return f'\033[48;5;{bg}m\033[38;5;{fg}m{text}\033[0;0m'

canvas = create_canvas()
text = ""
for line in canvas:
    for field in line:
        text += print_color(255, field, "a")
    text += "\n"
print(text)

response = requests.get("https://pokeapi.co/api/v2/pokemon/4")
print(response.json().keys())
# image_url_og = pokemon.get("sprites").get("front_default")
# # urllib.request.urlretrieve(image_url_og, 'img.png')
# # img = Image.open('img.png')

# # # print(pokemon.get("sprites").get("versions").get("generation-v").get("black-white").keys())
# # image_url_new = pokemon.get("sprites").get("versions").get("generation-v").get("black-white").get("front_default")
# # print(climage.convert(requests.get(image_url_new, stream=True).raw, is_unicode=True,palette="gruvboxdark"))
# print(pokemon.get("sprites").keys())
# for i in pokemon.get("sprites").get("versions").keys():
#     print(pokemon.get("sprites").get("versions").get(i).keys())
#     for blu in pokemon.get("sprites").get("versions").get(i).keys():
#         print(pokemon.get("sprites").get("versions").get(i).get(blu).get("front_default"))
#         if str(pokemon.get("sprites").get("versions").get(i).get(blu).get("front_default")) != "None":
#             image_url = pokemon.get("sprites").get("versions").get(i).get(blu).get("front_default")
#             urllib.request.urlretrieve(image_url, f'{blu}.png')
#             img = Image.open(f'{blu}.png')
#             print(img.format, img.size, img.mode)
            
#             # print(f'{i}  {blu} {image_url}')
#             # img = Image.open(requests.get(image_url, stream=True).raw)
#             # newsize = (160, 160)
            
            
#             if img.mode != "RGBA":
#                 img = img.convert('RGBA')
#             newImage = []
#             print(img.size)
#             the_set = set()
#             for item in img.getdata():
#                 the_set.add(item)
#                 if item[3] == 0:
#                     newImage.append((0, 0, 0, 0))
#                 else:
#                     newImage.append(item)
#             print(the_set)
#             img.putdata(newImage)
#             img = img.filter(ImageFilter.SMOOTH)
#             print(img.format, img.size, img.mode)
#             img.save(f'blu{blu}.png')
#             print(climage.convert(f'blu{blu}.png', is_unicode=True, width=60, is_256color=False, is_truecolor=True))


