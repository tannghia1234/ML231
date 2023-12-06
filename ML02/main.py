import cv2
import numpy
import dlib
from time import sleep
import pyautogui

# setup các thông số-----------------------------
speed = 20 # tốc độ di chuyển của chuột
count = 0 # đếm thời gian thực các vòng lặp

# lấy đường dẫn đến file train-------------------
direct = 'C:\\Users\\Lenovo\\Desktop\\ML02\\'
datfile = direct + 'shape_predictor_68_face_landmarks.dat'

# khởi tạo biến đọc hình ảnh từ camera ----------
cap = cv2.VideoCapture(0)
_, frame = cap.read()

# khởi tạo các hàm để phát hiện và dự đoán ------
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(datfile)


# hàm tính khoảng cách hai điểm -----------------
def pytago(a, b):
    return numpy.sqrt(pow(a[0] - b[0], 2) + pow(a[1] - b[1], 2))


while True:
    count += 1
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(frame)
    for face in faces:
        landmarks = predictor(gray_frame, face)


        def notes(): 
            for i in range(68):
                dotx = (landmarks.part(i).x, landmarks.part(i).y)
                cv2.circle(frame, dotx, 0, (255, 0, 0), 5)
                
        # notes()

        # hàm trả về giá trị tọa độ các điểm
        def dot(x):
            return (landmarks.part(x).x, landmarks.part(x).y)
        
        
        def eyes():
            lew = pytago(dot(38), dot(40)) # mắt trái
            rew = pytago(dot(43), dot(47)) # mắt phải
            base = pytago(dot(28), dot(29))
            cv2.putText(frame, 'L: ' + str(round(lew, 2)), (10, 70), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 0, 0))
            cv2.putText(frame, 'R: ' + str(round(rew, 2)), (10, 90), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 0, 0))
            cv2.putText(frame, 'B: ' + str(round(base, 2)), (10, 110), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 0, 0))
            cv2.putText(frame, 'S: ' + str(round(speed, 2)), (10, 150), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 0, 0))
            
            # phát hiện mắt trái nhắm
            if lew < (base*7.5/18):
                cv2.putText(frame, 'Eyes closed', (230, 20), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 0, 0))
                pyautogui.click() # click màn hình
            else:
                cv2.putText(frame, 'Eyes opened', (230, 20), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 255, 0))

        
        eyes()

        # hiển thị số vòng lặp
        cv2.putText(frame, 'Time: ' + str(round(count, 2)), (10, 210), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 0, 0))
  

        # hàm phát hiện chuyển động miệng
        def mouth(speed):
            mid = pytago(dot(62), dot(66))
            cv2.putText(frame, 'M: ' + str(round(mid, 2)), (10, 130), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 0, 0))
            if mid > 8:
                cv2.putText(frame, 'Talking', (255, 50), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 255))
                if speed >= 80:
                    speed = 20
                    sleep(0.2)
                else:
                    speed += 20
                    sleep(0.2)
                    
            return speed
        
        
        # cập nhật tốc độ trỏ chuột
        speed = mouth(speed)
        
        
        # hàm phát hiện hướng di chuyển khuôn mặt
        def face():
            if pytago(dot(2), dot(30)) / pytago(dot(30), dot(13)) >= 1.5:
                cv2.putText(frame, 'Right look', (355, 110), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 255))
                pyautogui.move(speed, 0, duration=pyautogui.MINIMUM_DURATION)
                    
            elif pytago(dot(13), dot(30)) / pytago(dot(30), dot(2)) >= 1.5:
                cv2.putText(frame, 'Left look', (155, 110), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 255))
                pyautogui.move(-speed, 0, duration=pyautogui.MINIMUM_DURATION)
            else:
                if pytago(dot(8), dot(33)) / pytago(dot(33), dot(27)) >= 1.5:
                    cv2.putText(frame, 'Up look', (255, 90), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 255))
                    pyautogui.move(0, -speed, duration=pyautogui.MINIMUM_DURATION)
                    
                elif pytago(dot(23), dot(43)) / pytago(dot(43), dot(47)) <= 1.5:
                    cv2.putText(frame, 'Down look', (255, 390), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 255))
                    pyautogui.move(0, speed, duration=pyautogui.MINIMUM_DURATION)
                else:
                    cv2.putText(frame, 'Straight look', (255, 110), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 255))
            
            
        face()
    # hiển thị hình ảnh
    cv2.imshow('App', frame)
    key = cv2.waitKey(1)
    if key == 27:
        break