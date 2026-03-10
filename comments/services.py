from PIL import Image


def resize_image(image):

    if not image:
        return

    img = Image.open(image)

    if img.width > 320 or img.height > 240:
        img.thumbnail((320, 240))
        img.save(image.path)
