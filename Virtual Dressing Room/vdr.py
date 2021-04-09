import tkinter as tk
import cv2
import PIL.Image
import PIL.ImageTk
import time
import numpy as np
import keyboard

frame_width = 800
frame_height = 800
ID = 0
offset = 0


class App:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        global offset

        self.cap = VideoCapture()

        self.back_label = tk.Label(window)
        self.back_label.place(relwidth=1, relheight=1, relx=0, rely=0)

        self.frame = tk.Frame(window, bd=10)
        self.frame.place(relx=0.52, width=frame_width,
                         height=frame_height, anchor='n')

        self.canvas = tk.Canvas(
            self.frame, width=self.cap.width, height=self.cap.height)
        self.canvas.pack()

        self.delay = 5
        self.update()

        self.window.mainloop()

    def update(self):
        _, frame = self.cap.get_frame()

        if _:
            self.photo = PIL.ImageTk.PhotoImage(
                image=PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.window.after(self.delay, self.update)


class VideoCapture:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)

        if not self.cap.isOpened():
            print("Unable to open Camera as ", self.cap.isOpened())

        self.width = frame_width
        self.height = frame_height

    def __del__(self):
        if self.cap.isOpened():
            self.cap.release()

    def get_frame(self):
        if self.cap.isOpened():
            _, frame = self.cap.read()
            cv2.flip(frame, 1)
            if _:
                assert not isinstance(frame, type(None)), 'frame not found'

                global ID, offset
                shirts_type = ['images/denim.jpg', 'images/wtshirt.jpg']
                threshold = [200, 254]
                shirt_id = ID
                imgshirt = cv2.imread(shirts_type[shirt_id])
                musgray = cv2.cvtColor(imgshirt, cv2.COLOR_BGR2GRAY)
                ret, orig_mask = cv2.threshold(
                    musgray, threshold[ID], 255, cv2.THRESH_BINARY)
                orig_mask_inv = cv2.bitwise_not(orig_mask)
                origshirtHeight, origshirtWidth = imgshirt.shape[:2]
                face_cascade = cv2.CascadeClassifier(
                    '.\haarcascade_frontalface_default.xml')
                img_h, img_w = frame.shape[:2]
                self.cap.set(3, frame_width)
                self.cap.set(4, frame_height)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 0), 1)

                    face_w = w
                    face_h = h
                    face_x1 = x
                    face_x2 = face_x1 + face_w
                    face_y1 = y
                    face_y2 = face_y1 + face_h

                    # shirt size w.r.t tracked face
                    shirtWidth = int(2.9 * face_w + offset)
                    shirtHeight = int(
                        (shirtWidth * origshirtHeight / origshirtWidth)+offset/3)
                    print(str(shirtWidth)+" "+str(shirtHeight))

                    # shirt centered w.r.t recognized face
                    shirt_x1 = face_x2 - int(face_w / 2) - int(shirtWidth / 2)
                    shirt_x2 = shirt_x1 + shirtWidth
                    shirt_y1 = face_y2 + 5
                    shirt_y2 = shirt_y1 + shirtHeight

                    if shirt_x1 < 0:
                        shirt_x1 = 0
                    if shirt_y1 < 0:
                        shirt_y1 = 0
                    if shirt_x2 > img_w:
                        shirt_x2 = img_w
                    if shirt_y2 > img_h:
                        shirt_y2 = img_h

                    shirtWidth = shirt_x2 - shirt_x1
                    shirtHeight = shirt_y2 - shirt_y1
                    if shirtWidth < 0 or shirtHeight < 0:
                        continue

                    # Re-sizing original image and masks to shirt sizes
                    shirt = cv2.resize(
                        imgshirt, (shirtWidth, shirtHeight), interpolation=cv2.INTER_AREA)
                    mask = cv2.resize(
                        orig_mask, (shirtWidth, shirtHeight), interpolation=cv2.INTER_AREA)
                    mask_inv = cv2.resize(
                        orig_mask_inv, (shirtWidth, shirtHeight), interpolation=cv2.INTER_AREA)

                    roi = frame[shirt_y1:shirt_y2, shirt_x1:shirt_x2]

                    roi_bg = cv2.bitwise_and(roi, roi, mask=mask)
                    roi_fg = cv2.bitwise_and(shirt, shirt, mask=mask_inv)
                    dst = cv2.add(roi_bg, roi_fg)

                    kernel = np.ones((5, 5), np.float32) / 25
                    imgshirt = cv2.filter2D(dst, -1, kernel)

                    if face_y1 + shirtHeight + face_h < frame_height:
                        frame[shirt_y1:shirt_y2, shirt_x1:shirt_x2] = dst

                    else:
                        print('Too close to the camera')

                    if keyboard.is_pressed('i'):
                        if offset > 100:
                            print("THIS IS THE MAXIMUM SIZE AVAILABLE")
                        else:
                            offset += 50
                            print('+ pressed')

                    if keyboard.is_pressed('d'):
                        if offset < 0:
                            print("THIS IS THE MINIMUM SIZE AVAILABLE")
                        else:
                            offset -= 50
                            print('- pressed')

                if _:
                    return (_, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                else:
                    return (_, None)
        else:
            return (None, None)


App(tk.Tk(), "V-SHOP Virtual Dressing Room")
