import threading
import time
import random
import qrcode
from pyzbar.pyzbar import decode
from PIL import ImageDraw

filename = "qrcode.png"
box_size = 3
border = 4
cover_percentage = 0.07

qr = qrcode.QRCode(
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=box_size,
    border=border
)
qr.add_data("https://www.jfsg.nl")
qr.make(fit=True)
base_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

grid_size = base_img.size[0] // box_size - 2 * border
total_pixels = grid_size * grid_size
pixels_to_cover = int(total_pixels * cover_percentage)

pixels = []
for pixel in range(total_pixels):
    x = pixel % grid_size
    y = pixel // grid_size
    x1 = (x + border) * box_size
    y1 = (y + border) * box_size
    x2 = x1 + box_size - 1
    y2 = y1 + box_size - 1
    pixels.append((x1, y1, x2, y2))

def random_coordinates():
    while True:
        yield random.sample(pixels, pixels_to_cover)

coord_gen = random_coordinates()

i = 0

def print_i():
    while True:
        print(i)
        time.sleep(1)

thread = threading.Thread(target=print_i, daemon=True)
thread.start()

while True:
    img = base_img.copy()
    draw = ImageDraw.Draw(img)

    for (x1, y1, x2, y2) in next(coord_gen):
        draw.rectangle([x1, y1, x2, y2], fill="red")

    result = decode(img)
    if len(result) > 0:
        print(i)
        img.save(filename)
        break

    i += 1