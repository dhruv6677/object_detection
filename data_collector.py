import os
import cv2
import time
import uuid
IMAGE_PATH = "CollectedImages"
labels = ['Hello','Yes','No','IloveYou','Please']
number_of_images = 5
for label in labels:
    image_path = os.path.join(IMAGE_PATH,label)
    os.makedirs(image_path)
    # open camera
    cap = cv2.VideoCapture(0)
    print(f"collecting images for{label} ")
    time.sleep(3)

    for imagnum in range(number_of_images):
        ret,frame = cap.read()
        imagename = os.path.join(IMAGE_PATH,label,label+'.'+'{}.jpg'.format(str(uuid.uuid1())))
        cv2.imwrite(imagename,frame)
        cv2.imshow('frame',frame)
        time.sleep(2)

        if cv2.waitKey(1) & 0xFF==ord('q'):
            break
    cap.release()




