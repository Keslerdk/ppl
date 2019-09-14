from PIL import Image, ImageDraw
import math

def yaw(img):
    img = Image.open(img)
    img.show()
    flag = False
    x, y = img.size
    for i in range((y - 1)//2, 0, -1):
        for g in range(0, x):
            if img.getpixel((g, i)) == (0, 0, 255):
                t1x, t1y = g, i
                flag = True
                break
        if flag:
            break

    t2x, t2y = t1x, (t1y - 30)

    for i in range(x):
        if img.getpixel((i, t2y)) == (0, 0, 255):
            t3x, t3y = i, t2y
            break

    tg = abs(t3x - t2x) / 30
    arctg = math.atan(tg)
    draw = ImageDraw.Draw(img)
    draw.line((t1x, 0, t1x, y), fill=128, width=3)
    draw.line((0, t2y, x, t2y), fill=128, width=3)
    draw.line((t1x, t1y, t3x, t3y), fill=10, width=3)
    img.show()
    return arctg

print(yaw('line.png'))