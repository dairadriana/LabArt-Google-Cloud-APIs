import requests

font_url = "https://github.com/google/fonts/raw/main/ofl/baloo2/Baloo2-Regular.ttf"
response = requests.get(font_url)

with open("Baloo2-Regular.ttf", "wb") as f:
    f.write(response.content)