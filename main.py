import requests
import json
import urllib.request
import climage
import climage
from canvas import Canvas
from image import Image

import os

def print_color(fg=(0,0,0), bg=(255,255,255), text=" "):
    if type(bg) == "str":
        print(fg, bg)
    return f'\x1b[48;2;{bg[0]};{bg[1]};{bg[2]}m\x1b[38;5;{fg}m{text}\x1b[0;0m'

def get_evolutions():
    # TODO: get evolution id dynamically
    response = requests.get("https://pokeapi.co/api/v2/evolution-chain/2").json()
    starter = response.get('chain').get('species').get('name')
    # TODO: is looping necessary? fix error handling for non level evolutions
    for i in response.get('chain').get('evolves_to'):
        evo_1 = { 
            'name': i.get('species').get('name'), 
            'level': i.get('evolution_details')[0].get('min_level'), 
            'trigger': i.get('evolution_details')[0].get('trigger').get('name'),
            'item': (i.get('evolution_details')[0].get('held_item') or {'name': 'nothing'}).get('name')
        }
        for j in i.get('evolves_to'):
            evo_2 = { 
                'name': j.get('species').get('name'), 
                'level': j.get('evolution_details')[0].get('min_level'), 
                'trigger': j.get('evolution_details')[0].get('trigger').get('name'),
                'item': (j.get('evolution_details')[0].get('held_item') or {'name': 'nothing'}).get('name')
            }
    return (starter, evo_1, evo_2)

def create_evolutions_string(evolutions):
    # TODO: more styling, not all evolutins are level based, not all pokemon have 3 evolutions, create spaces dynamically 
    return f"""
    {evolutions[0]}     >>      {evolutions[1].get('name')}     >>      {evolutions[2].get('name')}
                level {evolutions[1].get('level')}                level {evolutions[2].get('level')}
            """




canvas = Canvas(85, 20)
image = Image(4)


json = requests.get("https://pokeapi.co/api/v2/pokemon-species/4").json()
poke_desc = json.get('flavor_text_entries')[0].get('flavor_text').replace('\u000c', ' ')

canvas.add('description', poke_desc)
canvas.add('image', image.get_raw_data())
canvas.add('evo', create_evolutions_string(get_evolutions()))
canvas.add('name', json.get('name').title())

text = ""
for line in canvas.content:
    for field in line:
        text += print_color(255, field[0], field[1])
    text += "\n"
print(text)




############################################################
# working POC
############################################################
# canvas = create_canvas()

# response = requests.get("https://pokeapi.co/api/v2/pokemon-species/4")
# json = response.json()
# # TODO: get index of language dynamically
# poke_desc = json.get('flavor_text_entries')[0].get('flavor_text').replace('\u000c', ' ')
# evolutions = get_evolutions()
# evolutions = create_evolutions_string(evolutions)
# canvas = add_to_canvas(canvas, 'description', poke_desc)
# canvas = add_to_canvas(canvas, 'name', json.get('name').title())
# canvas = add_to_canvas(canvas, 'evo', evolutions)
# image = get_image()
# width, height = image.size
# left = 18
# top = height / 4
# right = 70
# bottom = 3 * height / 4
# image = image.crop((left, top, right, bottom))
# image = image.resize((26,20))
# image = image.convert('RGB')
# # Shows the image in image viewer
# canvas = add_image_to_canvas(canvas, image.getdata())

# text = ""
# for line in canvas:
#     for field in line:
#         text += print_color(255, field[0], field[1])
#     text += "\n"
# print(text)
############################################################


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


