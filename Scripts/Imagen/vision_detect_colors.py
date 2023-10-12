
from google.cloud import vision
from matplotlib.colors import to_hex
from PIL import Image, ImageDraw

def detect_properties(path):
    """Detects image properties in the file."""

    client = vision.ImageAnnotatorClient()

    with open(path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.image_properties(image=image)
    props = response.image_properties_annotation
    print("Properties:")

    colors = []

    for color in props.dominant_colors.colors:

        rgb = color.color
        hex_color = to_hex((rgb.red / 255.0, rgb.green / 255.0, rgb.blue / 255.0))
        
        print(f"fraction: {color.pixel_fraction}")
        print(f"\tr: {color.color.red}")
        print(f"\tg: {color.color.green}")
        print(f"\tb: {color.color.blue}")
        print(f"\ta: {color.color.alpha}")

        colors.append(hex_color)

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )
    
    # Color palette creation
    palette_width = 1000
    palette_height = 300
    palette = Image.new("RGB", (palette_width, palette_height))
    draw = ImageDraw.Draw(palette)

    # Each color block
    block_width = palette_width // len(colors)

    # Draw color blocks
    for i, color in enumerate(colors):
        draw.rectangle([i * block_width, 0, (i + 1) * block_width, palette_height], fill=color)

    # Save the palette image
    palette.save("palette.png")