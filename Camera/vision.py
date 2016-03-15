import cv2
import numpy as np

class GoalFinder(object):

    def __init__(self):
        #HLS
        self.minHLS = np.array([50, 112, 100])
        self.maxHLS = np.array([141, 171, 255])
        self.minArea = 150;

        self.targetAreas = []
        self.targetXs = []
        self.targetYs = []
        self.targetHeights = []
        self.targetWidths = []

    def process_image(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)

        mask = cv2.inRange(gray, self.minHLS, self.maxHLS)

        contours, hierarchy = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_TC89_KCOS)

        self.targetAreas = []
        self.targetXs = []
        self.targetYs = []
        self.targetHeights = []
        self.targetWidths = []

        for c in contours:

            area = cv2.contourArea(c)
            x, y, w, h = cv2.boundingRect(c)

            if (area > self.minArea and #Min Area
                    w < 1000 and        #Max Width
                    h < 1000):          #Max Height

                #Center of image
                x += w / 2.0
                y += h / 2.0

                #print cv2.boundingRect(c)

                self.targetAreas.append(area)
                self.targetHeights.append(h)
                self.targetWidths.append(w)
                self.targetXs.append(x)
                self.targetYs.append(y)
