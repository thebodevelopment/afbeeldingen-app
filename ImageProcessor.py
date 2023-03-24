import PIL

class ImageProcessor:
    def __init__(self, image):
        self.image = image

    def trim(self):
        background = PIL.Image.new(self.image.mode, self.image.size, self.image.getpixel((0, 0)))
        difference = PIL.ImageChops.difference(self.image, background)
        difference = PIL.ImageChops.add(difference, difference, 2.0, 0)
        bbox = difference.convert('RGB').getbbox()
        return self.image.crop(bbox)
    
    def resize(self, width, height):
        ratio_width = width / self.image.width
        ratio_height = height / self.image.height
        if ratio_width < ratio_height:
            resize_width = width
            resize_height = round(ratio_width * self.image.height)
        else:
            resize_width = round(ratio_height * self.image.width)
            resize_height = height
        image_resize = self.image.resize((resize_width, resize_height), PIL.Image.ANTIALIAS)
        background = PIL.Image.new('RGBA', (width, height), (255, 255, 255, 255))
        offset = (round((width - resize_width) / 2), round((height - resize_height) / 2))
        background.paste(image_resize, offset)
        return background.convert('RGB')