from network_esp32 import wifi

wifi.reset()

enc_str = ["OPEN", "", "WPA PSK", "WPA2 PSK", "WPA/WPA2 PSK", "", "", ""] + [""]*255
aps = wifi.nic.scan()

for ap in aps:
    print("SSID:{:^20}, ENC:{:>5} , RSSI:{:^20}".format(ap[0], enc_str[ap[1]], ap[2]))
