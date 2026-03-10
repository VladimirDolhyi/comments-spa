from PIL import Image


def resize_image(image):

    with Image.open(image.path) as img:
        if img.width > 320 or img.height > 240:
            img.thumbnail((320, 240))
            img.save(image.path, img.format)
