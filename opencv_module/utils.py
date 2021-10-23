import cv2
from datetime import datetime

def movement_detected(status_list):
        if status_list[-1] == 1 and status_list[-2] == 0:
            print(f'{datetime.now()}: Movement detected')

def generate_frames():
    baseline_image = None
    status_list = [None, None]
    video = cv2.VideoCapture(0)

    while True:
        check, frame = video.read()
        if not check:
            print(f'Could not read camera output')
            break

        status = 0
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_frame = cv2.GaussianBlur(gray_frame, (25, 25), 0)

        if baseline_image is None:
            baseline_image = gray_frame
            continue

        delta = cv2.absdiff(baseline_image, gray_frame)
        threshold = cv2.threshold(delta, 30, 255, cv2.THRESH_BINARY)[1]
        (contours, _) = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            if cv2.contourArea(contour) < 10000:
                continue
            status = 1
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)
            movement_detected(status_list)
        status_list.append(status)

        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield(
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'
        )

        key = cv2.waitKey(1)

        if key == ord('q'):
            break
    video.release()