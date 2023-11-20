import face_recognition
import sys
import cv2
import numpy as np


class FaceRecognition:
    face_locations = []

    def __init__(self):
        self.video_capture = cv2.VideoCapture(0)
        self.center_point = (0, 0)

        if not self.video_capture.isOpened():
            sys.exit("Couldn't open video capture")

    def update(self):
        ret, frame = self.video_capture.read()

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = np.ascontiguousarray(small_frame[:, :, ::-1])

        self.face_locations = face_recognition.face_locations(rgb_small_frame)

        for (top, right, bottom, left), in zip(self.face_locations):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            self.center_point = (int(left - (left - right) / 2), int(bottom - (bottom - top) / 2))
            cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)
            cv2.rectangle(frame, (left, bottom), (right, bottom), (255, 0, 0), -1)
            # cv2.circle(frame, (int(left-(left-right)/2), int(bottom-(bottom-top)/2)), 1, (0, 0, 0))

        cv2.imshow('Face Tracking', frame)

        if cv2.waitKey(1) == ord('q'):
            return False
        else:
            return True


fr = FaceRecognition()

while fr.update():
    referenced_center_point = (fr.center_point[0] - 300, fr.center_point[1] - 200)
    print(referenced_center_point)

fr.video_capture.release()
cv2.destroyAllWindows()