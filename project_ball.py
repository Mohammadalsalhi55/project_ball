import cv2 as cv
import numpy as np
class Ball:
    def __init__(self):
        self.vid = cv.VideoCapture(0)
        self.min_h = None
        self.max_h = None
        self.lower = None
        self.upper = None
        self.exposure = None
        self.black = None
        self.kernel = None
        self.contours = None
        self.frame = None
        self.hsv = None
        self.mask = None
        self.no_use = None
        self.masking_ball = None
        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0
        self.angle = 0
        self.saturation1 = 0
        self.value1= 0
        self.stop = 0
        self.var = 100
        self.trackbar_name = "trackpar_ball"
    def nothing(self):
        pass
    def Get_vid(self):
        return self.vid
    def Trackbar(self):
        cv.namedWindow(self.trackbar_name)
        cv.createTrackbar("exposure", self.trackbar_name, 1, 7, self.nothing)
        cv.createTrackbar("min_h", self.trackbar_name, 0, 180, self.nothing)
        cv.createTrackbar("max_h", self.trackbar_name, 0, 180, self.nothing)
    def Frame_detect(self):
        self.trackbar()
        self._, self.frame = self.vid.read()
        self.frame = cv.GaussianBlur(self.frame, (7, 7), 0)
        self.hsv = cv.cvtColor(self.frame, cv.COLOR_BGR2HSV)
        self.value=np.average(self.hsv[: ,: ,1])
        self.saturation=np.average(self.hsv[:, :,2])
    def trackbar(self):
        self.exposure = cv.getTrackbarPos("exposure", self.trackbar_name)
        self.min_h = cv.getTrackbarPos("min_h", self.trackbar_name)
        self.max_h = cv.getTrackbarPos("max_h", self.trackbar_name)
        self.lower = np.array([self.min_h, self.saturation1, self.value1])
        self.upper = np.array([self.max_h, 255, 255])
        self.vid.set(15, -self.exposure)


    def masking(self):
        self.Frame_detect()
        self.mask = cv.inRange(self.hsv, self.lower, self.upper)
        self.black = np.zeros(self.frame.shape[:2], np.uint8)
        self.kernel = np.ones((3, 3), np.uint8)
        self.mask = cv.erode(self.mask, self.kernel)
    def contourS(self):
        self.masking()
        self.contours, self.no_use = cv.findContours(self.mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        if len(self.contours) != 0:
            for contour in self.contours:
                if cv.contourArea(contour) > 1500:
                    rect = cv.minAreaRect(contour)
                    box = cv.boxPoints(rect)
                    box = np.int0(box)
                    cv.drawContours(self.frame, [box], -1, (255, 0, 0), 3)
                    (self.x, self.y), (self.w, self.h), self.angle = rect
        rectangle = cv.rectangle(self.black.copy(), (int(self.x - self.var), int(self.y - self.var)), (int(self.x + self.var), int(self.y + self.var)), 255, -1)
        self.masking_ball = cv.bitwise_and(self.frame, self.frame, mask=rectangle)
    def show(self):
        self.contourS()
        cv.imshow("vid", cv.flip(self.mask, 1))
        cv.imshow("vid_original", cv.flip(self.masking_ball, 1))
