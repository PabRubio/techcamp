import sensor, image, lcd, time, utime, gc
import KPU as kpu
from Maix import FPIOA, GPIO
from fpioa_manager import fm
from board import board_info

task_fd = kpu.load("/sd/FaceDetection.smodel")
task_ld = kpu.load("/sd/FaceLandmarkDetection.smodel")
task_fe = kpu.load("/sd/FeatureExtraction.smodel")

clock = time.clock()

fm.register(board_info.BOOT_KEY, fm.fpioa.GPIOHS0)
key_gpio = GPIO(GPIO.GPIOHS0, GPIO.IN)
start_processing = False

BOUNCE_PROTECTION = 50

def set_key_state(_):
    global start_processing
    start_processing = True
    utime.sleep_ms(BOUNCE_PROTECTION)

key_gpio.irq(set_key_state, GPIO.IRQ_RISING, GPIO.WAKEUP_NOT_SUPPORT)

lcd.init(type=1)
sensor.reset()

sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)

sensor.set_hmirror(1)
sensor.set_vflip(0)

sensor.run(1)

anchor = (1.889, 2.5245, 2.9465, 3.94056, 3.99987, 5.3658, 5.155437, 6.92275, 6.718375, 9.01025)

dst_point = [(44, 59), (84, 59), (64, 82), (47, 105), (81, 105)]

kpu.init_yolo2(task_fd, 0.5, 0.3, 5, anchor)

img_lcd = image.Image()
img_face = image.Image(size= (128,128))

img_face.pix_to_ai()

record_ftr = []
record_ftrs = []

names = ['Person 1', 'Person 2', 'Person 3', 'Person 4', 'Person 5',
         'Person 6', 'Person 7', 'Person 8', 'Person9', 'Person 10']

ACCURACY = 85

while (1):
    img = sensor.snapshot()
    clock.tick()
    faces_detected = kpu.run_yolo2(task_fd, img)
    if faces_detected:
        for i in faces_detected:
            # Cut face and resize to 128x128
            img.draw_rectangle(i.rect())
            face_cut = img.cut(i.x(), i.y(), i.w(), i.h())
            face_cut_128 = face_cut.resize(128, 128)
            face_cut_128.pix_to_ai()
            # Landmark for face 5 points
            fmap = kpu.forward(task_ld, face_cut_128)
            plist = fmap[:]
            le = (i.x() + int(plist[0] * i.w() - 10), i.y() + int(plist[1] * i.h()))
            re = (i.x() + int(plist[2] * i.w()), i.y() + int(plist[3] * i.h()))
            nose = (i.x() + int(plist[4] * i.w()), i.y() + int(plist[5] * i.h()))
            lm = (i.x() + int(plist[6] * i.w()), i.y() + int(plist[7] * i.h()))
            rm = (i.x() + int(plist[8] * i.w()), i.y() + int(plist[9] * i.h()))
            img.draw_circle(le[0], le[1], 4)
            img.draw_circle(re[0], re[1], 4)
            img.draw_circle(nose[0], nose[1], 4)
            img.draw_circle(lm[0], lm[1], 4)
            img.draw_circle(rm[0], rm[1], 4)
            # align face to standart position
            src_point = [le, re, nose, lm, rm]
            T = image.get_affine_transform(src_point, dst_point)
            image.warp_affine_ai(img, img_face, T)
            img_face.ai_to_pix()
            del(face_cut_128)
            # calculate face feature vector
            fmap = kpu.forward(task_fe, img_face)
            feature = kpu.face_encode(fmap[:])
            reg_flag = False
            scores = []
            for j in range(len(scores)):
                score = kpu.face_compare(record_ftrs[j], feature)
                scores.append(score)
            max_score = 0
            index = 0
            for k in range(len(scores)):
                if max_score < scores[k]:
                    max_score = scores[k]
                    index[k]
            if max_score > ACCURACY:
                a = img.draw_string(i.x(), i.y(), ("%s :%2.1f" % (
                    names[index], max_score)), color=(0, 255, 0), scale=2)
            else:
                a = img.draw_string(i.x(), i.y(), ("X :%2.1f" % (
                    max_score)), color=(0, 255, 0), scale=2)
            if start_processing:
                record_ftr = feature
                record_ftrs.append(record_ftr)
                start_processing = False
                break
    fps = clock.fps()
    img.draw_string(0, 0, ("%2.1f fps" % fps), color=(255, 0, 0), scale=2)
    a = lcd.display(img)
    gc.collect()
