import requests
import json
from PIL import Image
from PIL import ImageFilter
import urllib.request
import climage
import climage

def create_canvas():
    canvas = []
    for height in range(20):
        line = []
        for width in range(80):
            line.append([(0,0,0), " "])
        canvas.append(line)
    return canvas

def print_color(fg=(0,0,0), bg=(255,255,255), text=" "):
    return f'\x1b[48;2;{bg[0]};{bg[1]};{bg[2]}m\x1b[38;5;{fg}m{text}\x1b[0;0m'

def add_to_canvas(canvas, placement, content):
    place = {
        'description': {'columns': 25, 'lines': 16, 'start_line': 8, 'start_column': 8},
        'name': {'columns': 25, 'lines': 1, 'start_line': 2, 'start_column': 8},
        'evo': {'columns': 80, 'lines': 4, 'start_line': 16, 'start_column': 0},
        'image': {'columns': 48, 'lines': 48, 'start_line': 0, 'start_column': 30}
    }
    placement = place[placement]
    content = list(content)
    content_index = 0
    done = False
    # TODO: find better way to loop and break
    for line in range(placement['start_line'], placement['start_line']+placement['lines']):
        for column in range(placement['start_column'],placement['start_column']+placement['columns']):
            if content[content_index] == '\n':
                content_index += 1
                break
            canvas[line][column][1] = content[content_index]
            content_index += 1
            if content_index >= len(content):
                done = True
                break
        if done:
            break
    return canvas

# TODO: Merge with add_to_canvas, fix color for Terminal
def add_image_to_canvas(canvas, image):
    place = {
        'image': {'columns': 26, 'lines': 20, 'start_line': 0, 'start_column': 54}
    }
    placement = place['image']
    image = list(image)
    image_index = 0
    done = False
    # TODO: find better way to loop and break
    for line in range(placement['start_line'], placement['start_line']+placement['lines']):
        for column in range(placement['start_column'],placement['start_column']+placement['columns']):
            if image[image_index] == '\n':
                image_index += 1
                break
            canvas[line][column][0] = image[image_index]
            image_index += 1
            if image_index >= len(image):
                done = True
                break
        if done:
            break
    return canvas

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

def get_image():
    pokemon = requests.get('https://pokeapi.co/api/v2/pokemon/4').json()
    image_url = pokemon.get("sprites").get("front_default")
    urllib.request.urlretrieve(image_url, 'image.png')
    return Image.open('image.png')


canvas = create_canvas()

response = requests.get("https://pokeapi.co/api/v2/pokemon-species/4")
json = response.json()
# TODO: get index of language dynamically
poke_desc = json.get('flavor_text_entries')[0].get('flavor_text').replace('\u000c', ' ')
evolutions = get_evolutions()
evolutions = create_evolutions_string(evolutions)
canvas = add_to_canvas(canvas, 'description', poke_desc)
canvas = add_to_canvas(canvas, 'name', json.get('name').title())
canvas = add_to_canvas(canvas, 'evo', evolutions)
image = get_image()
width, height = image.size
left = 18
top = height / 4
right = 70
bottom = 3 * height / 4
image = image.crop((left, top, right, bottom))
image = image.resize((26,20))
image = image.convert('RGB')
# Shows the image in image viewer
canvas = add_image_to_canvas(canvas, image.getdata())

text = ""
for line in canvas:
    for field in line:
        text += print_color(255, field[0], field[1])
    text += "\n"
print(text)

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


