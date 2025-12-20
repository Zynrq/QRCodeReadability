import threading
import time
import random
import qrcode
from pyzbar.pyzbar import decode
from PIL import ImageDraw
from multiprocessing import Pool, cpu_count

##### variables #####
error_correction = qrcode.constants.ERROR_CORRECT_M
cover_percentage = 0.10
cover_function_patterns = False
#####################

box_size = 4
border = 4

qr = qrcode.QRCode(
    error_correction=error_correction,
    box_size=box_size,
    border=border
)
qr.add_data("https://www.jfsg.nl")
qr.make(fit=True)
base_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

grid_size = base_img.size[0] // box_size - 2 * border
total_pixels = grid_size * grid_size
pixels_to_cover = int(total_pixels * cover_percentage)

def is_function_pattern(x, y):
    if x < 8 and y < 8:
        return True
    if x >= grid_size - 8 and y < 8:
        return True
    if x < 8 and y >= grid_size - 8:
        return True
    if grid_size - 10 < x < grid_size - 4 and grid_size - 10 < y < grid_size - 4:
        return True
    if x == 6:
        return True
    if y == 6:
        return True
    if x == 8 and y == grid_size - 8:
        return True
    return False

pixels = []
for pixel in range(total_pixels):
    x = pixel % grid_size
    y = pixel // grid_size
    if is_function_pattern(x, y) and not cover_function_patterns:
        continue
    x1 = (x + border) * box_size
    y1 = (y + border) * box_size
    x2 = x1 + box_size - 1
    y2 = y1 + box_size - 1
    pixels.append((x1, y1, x2, y2))

def cover_qr(_):
    img = base_img.copy()
    draw = ImageDraw.Draw(img)

    for rect in random.sample(pixels, pixels_to_cover):
        draw.rectangle(rect, fill="red")

    result = decode(img)
    if len(result) > 0:
        return img
    return None

if __name__ == "__main__":
    batch_size = 100
    attempts = 0

    def print_attempts():
        while True:
            print(attempts)
            time.sleep(1)

    thread = threading.Thread(target=print_attempts, daemon=True)
    thread.start()

    with Pool(cpu_count()) as pool:
        while True:
            results = pool.map(cover_qr, range(batch_size))
            attempts += batch_size

            for img in results:
                if img is not None:
                    print(attempts)
                    img.save("qrcode.png")
                    pool.terminate()
                    exit()