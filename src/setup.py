import cv2
import face_recognition
import dlib
import csv
import numpy as np
import sys

lesson_id = sys.argv[1]
student_amount = sys.argv[2]
start_sec = sys.argv[3]

cap = cv2.VideoCapture("inputs/lesson" + str(lesson_id) + "/video.mp4")
cap.set(cv2.CAP_PROP_POS_FRAMES, int(start_sec) * 30)
trackers = []
frame_count = 0

f = open("calibration/lesson" + str(lesson_id) + "/face_locations.csv", 'w')
writer = csv.writer(f)

while True:
    # Grab a single frame of video
    ret, frame = cap.read()    # Convert the image from BGR color (which OpenCV uses) to RGB
    frame = cv2.resize(frame, (854, 480))  # Resize video
    image_cpy = np.copy(frame)

    if frame_count % 30 == 0:
        trackers = []
        face_locations = face_recognition.face_locations(image_cpy)

        face_count = "face count: " + \
            str(len(face_locations)) + " of " + str(student_amount)
        print("second: " + str(int(frame_count/30)))
        print(face_count)
        if len(face_locations) == int(student_amount):
            print(face_locations)

        for top, right, bottom, left in face_locations:
            # Draw a box around the face
            cv2.rectangle(image_cpy, (left, top), (right, bottom),
                          (0, 0, 255), 2)    # Display the resulting image
            tracker = dlib.correlation_tracker()
            rect = dlib.rectangle(left, top, right, bottom)
            tracker.start_track(image_cpy, rect)
            trackers.append(tracker)

    else:
        for tracker in trackers:
            tracker.update(image_cpy)
            pos = tracker.get_position()

            # unpack the position object
            startX = int(pos.left())
            startY = int(pos.top())
            endX = int(pos.right())
            endY = int(pos.bottom())

            cv2.rectangle(image_cpy, (startX, startY),
                          (endX, endY), (0, 0, 255), 3)

    frame_count += 1
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(image_cpy,
                face_count,
                (50, 50),
                font, 1,
                (0, 255, 255),
                2,
                cv2.LINE_4)
    cv2.imshow('Video', image_cpy)

    # Wait for Enter key to stop
    if cv2.waitKey(25) == 13:
        break
writer.writerow(("id", "left", "top", "right", "bottom"))
id = 0
for top, right, bottom, left in face_locations:
    writer.writerow((id, left, top, right, bottom))
    id += 1

print("saved location data to: face_locations.csv")
cap.release()
cv2.destroyAllWindows()
