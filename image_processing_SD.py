import image, lcd, time

lcd.init()

img = image.Image("/sd/images/chicken.jpg")

tim = time.time()
while True:
    lcd.display(img)
    if (time.time() - tim) >10:
        break

tim = time.time()
while True:
    lcd.mirror(True)
    lcd.display(img)
    if (time.time() - tim) >10:
        break

tim = time.time()
while True:
    lcd.display(img)
    if (time.time() - tim) >10:
        break

lcd.clear()
