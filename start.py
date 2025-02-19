import cv2                              # библиотека opencv (получение и обработка изображения)
import mediapipe as mp                  # библиотека mediapipe (распознавание рук)
import serial                           # библиотека pyserial (отправка и прием информации)


camera = cv2.VideoCapture(0)            # объявление камеры (0 - порядковый номер камеры в системе)
mpHands = mp.solutions.hands            # подключение раздела распознавания рук
hands = mpHands.Hands()                 # создание экземпляра класса "руки"
mpDraw = mp.solutions.drawing_utils     # подключение инструменты для рисования


portNo = "COM9"                         # порт, к которому подключена Arduino
uart = serial.Serial(portNo, 9600)


p = [0 for i in range(21)]
finger = [0 for i in range(5)]

def distance(point1, point2):
    return abs(point1 - point2)


while True:
    good, img = camera.read()                                               # получаем один кадр из видеопотока
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)                           # преобразуем кадр в RGB


    results = hands.process(imgRGB)                                         # результат распознавания
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:                        # получение координаты каждой точки

            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

            for id, point in enumerate(handLms.landmark):
                width, height, color = img.shape
                widthP, heightP = int(point.x * height), int(point.y * width)

                p[id] = heightP
                if id == 9:         # выбор нужной точки

                    cv2.circle(img, (widthP, heightP), 15, (255, 0, 255), cv2.FILLED)
                    if widthP < 0:
                        widthP = 0
                    if widthP > width:
                        widthP = width
                    if heightP < 0:
                        heightP = 0
                    if heightP > height:
                        heightP = height
                    msg = "," + str(widthP * 40 // width) + "," + str(heightP * 30 // height)
                if id == 12:
                    cv2.circle(img, (widthP, heightP), 15, (0, 0, 255), cv2.FILLED)

            # получение расстояния, с которым сравнивается каждый палец
            distanceGood = distance(p[0], p[5]) + (distance(p[0], p[5]) / 2)

            finger[1] = 1 if distance(p[0], p[8]) > distanceGood else 0
            finger[2] = 1 if distance(p[0], p[12]) > distanceGood else 0
            finger[3] = 1 if distance(p[0], p[16]) > distanceGood else 0
            finger[4] = 1 if distance(p[0], p[20]) > distanceGood else 0
            finger[0] = 1 if distance(p[4], p[17]) > distanceGood else 0

            if not(finger[1]) and not(finger[2]) and not(finger[3]) and not(finger[4]):
                msg += ',^;'
            else:
                msg += ',V;'
            print(msg)

            # отправка сообщения в Arduino
            msg = bytes(str(msg), 'utf-8')
            uart.write(msg)
            print(msg)

    cv2.imshow("Image", img)                # вывод окна с изображением
    if cv2.waitKey(1) == ord('q'):                  # ожидание нажатия клавиши q в течение 1 мс
        break