import random
import qrcode
from pyzbar.pyzbar import decode
from PIL import Image, ImageDraw
filename = "qrcode.png"
box_size = 3
border = 4

qr = qrcode.QRCode(
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=box_size,
    border=border
)
qr.add_data("https://www.jfsg.nl")
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white")

def cover_percentage(percentage):
    img = Image.open(filename).convert("RGB")
    size = int(img.size[0] / box_size) - 2 * border
    area = size ** 2 * percentage

    draw = ImageDraw.Draw(img)
    covered = 0
    dots = []

    while covered < area:
        x = None
        y = None

        while x is None or y is None or (x, y) in dots:
            x = random.randint(0, size - 1)
            y = random.randint(0, size - 1)

        dots.append((x, y))

        x1 = (x + border) * box_size
        y1 = (y + border) * box_size
        x2 = x1 + box_size - 1
        y2 = y1 + box_size - 1

        draw.rectangle([x1, y1, x2, y2], fill="red")
        covered += 1

    img.save(filename)

for i in range(10000):
    img.save(filename)

    cover_percentage(0.07)

    result = decode(Image.open(filename))
    if len(result) > 0:
        print(i)
        break