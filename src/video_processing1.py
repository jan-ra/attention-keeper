import cv2
import face_recognition
import dlib
import csv
import numpy as np

cap = cv2.VideoCapture("inputs/lesson1/video.mp4")
trackers = []
frame_count = 0
attention = " "
size = (640, 360)
f = open("processed/lesson1/faces.csv", 'w')
writer = csv.writer(f)
writer.writerow(("seconds", "luuk", "jan", "carlos", "mayank"))

result = cv2.VideoWriter('filename.avi',
                         cv2.VideoWriter_fourcc(*'MJPG'),
                         25, size)

while True:
    # Grab a single frame of video
    ret, frame = cap.read()    # Convert the image from BGR color (which OpenCV uses) to RGB
    frame = cv2.resize(frame, (640, 360))
    # rgb_frame = frame[:, :, ::-1]

    image_cpy = np.copy(frame)

    if frame_count % 30 == 0:
        trackers = []
        att0 = 0
        att1 = 0
        att2 = 0
        att3 = 0
        face_locations = face_recognition.face_locations(image_cpy)
        print(face_locations)
        for top, right, bottom, left in face_locations:
            if right >= 480:
                att3 = 1
            elif right >= 320:
                att2 = 1
            elif right >= 160:
                att1 = 1
            elif right >= 0:
                att0 = 1

        print("sec: " + str(frame_count/30))
        attention = "luuk : " + str(att0) + ", jan: " + str(att1) + \
            ", carlos: " + str(att2) + ", mayan: " + str(att3)
        print(attention)
        writer.writerow((frame_count/30, att0, att1, att2, att3))

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
                attention,
                (50, 50),
                font, 1,
                (0, 255, 255),
                2,
                cv2.LINE_4)
    result.write(image_cpy)
    cv2.imshow('Video', image_cpy)

    # Wait for Enter key to stop
    if cv2.waitKey(25) == 13:
        break

result.release()
cap.release()
cv2.destroyAllWindows()
f.close()
