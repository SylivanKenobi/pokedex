import requests
import json
from PIL import Image
import climage
import urllib.request

response = requests.get("https://pokeapi.co/api/v2/pokemon/4")
pokemon = response.json()
# image_url_og = pokemon.get("sprites").get("versions").get("generation-i").get("red-blue").get("front_default")
# # print(pokemon.get("sprites").get("versions").get("generation-v").get("black-white").keys())
# image_url_new = pokemon.get("sprites").get("versions").get("generation-v").get("black-white").get("front_default")
# print(climage.convert(requests.get(image_url_og, stream=True).raw, palette="gruvboxdark"))
# print(climage.convert(requests.get(image_url_new, stream=True).raw, is_unicode=True,palette="gruvboxdark"))
print(pokemon.get("sprites").get("versions").keys())
for i in pokemon.get("sprites").get("versions").keys():
    print(pokemon.get("sprites").get("versions").get(i).keys())
    for blu in pokemon.get("sprites").get("versions").get(i).keys():
        print(pokemon.get("sprites").get("versions").get(i).get(blu).get("front_default"))
        if str(pokemon.get("sprites").get("versions").get(i).get(blu).get("front_default")) != "None":
            image_url = pokemon.get("sprites").get("versions").get(i).get(blu).get("front_default")
            urllib.request.urlretrieve(image_url, f'bla{blu}.png')
            img = Image.open(f'bla{blu}.png')
            print(img.size)
            # print(f'{i}  {blu} {image_url}')
            # img = Image.open(requests.get(image_url, stream=True).raw)
            newsize = (160, 160)
            bla = img.resize(newsize)
            bla.save(f'blu{blu}.png')

            print(climage.convert(f'blu{blu}.png', palette="gruvboxdark", is_unicode=True, width=60, is_256color=False, is_truecolor=True))
