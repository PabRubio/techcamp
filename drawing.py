import lcd, image

lcd.init(type=1)

lcd.draw_string(120, 120, "Pablo")
lcd.fill_rectangle(200, 100, 100, 100, lcd.BLUE)
lcd.fill_rectangle(100, 50, 50, 50, lcd.GREEN)
lcd.fill_rectangle(50, 150, 100, 50, lcd.ORANGE)
