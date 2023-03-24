import PIL

def open_image(file):
    image = PIL.Image.open(file)
    image = image.convert('RGBA')
    if image.mode in ('RGBA', 'LA'):
        background = PIL.Image.new(image.mode[:-1], image.size, (255, 255, 255))
        background.paste(image, image.split()[-1])
        image = background
    image.convert('RGB')
    return image

def trim(image):
    background = PIL.Image.new(image.mode, image.size, image.getpixel((0, 0)))
    difference = PIL.ImageChops.difference(image, background)
    difference = PIL.ImageChops.add(difference, difference, 2.0, 0)
    bbox = difference.convert('RGB').getbbox()
    return image.crop(bbox)

def resize(image, width, height):
    ratio_width = width / image.width
    ratio_height = height / image.height
    if ratio_width < ratio_height:
        resize_width = width
        resize_height = round(ratio_width * image.height)
    else:
        resize_width = round(ratio_height * image.width)
        resize_height = height
    image_resize = image.resize((resize_width, resize_height), PIL.Image.ANTIALIAS)
    background = PIL.Image.new('RGBA', (width, height), (255, 255, 255, 255))
    offset = (round((width - resize_width) / 2), round((height - resize_height) / 2))
    background.paste(image_resize, offset)
    return background.convert('RGB')