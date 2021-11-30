import cv2
import numpy as np

class TargetDetection:
    def __init__(self) -> None:
        self.knn = cv2.createBackgroundSubtractorKNN(detectShadows = True) 
        #创建KNN接口
        self.es = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (20,12))
        # camera = cv2.VideoCapture("./output_path.avi")
 
    def drawCnt(self,fn, cnt):
        if cv2.contourArea(cnt) > 1400:
            (x, y, w, h) = cv2.boundingRect(cnt)
            cv2.rectangle(fn, (x, y), (x + w, y + h), (255, 255, 0), 2)


    def run_detection(self,frame):
        fg = self.knn.apply(frame.copy()) 
        #计算了前景掩码
        fg_bgr = cv2.cvtColor(fg, cv2.COLOR_GRAY2BGR)  
        #进行色彩转换
        bw_and = cv2.bitwise_and(fg_bgr, frame)
        draw = cv2.cvtColor(bw_and, cv2.COLOR_BGR2GRAY)
        draw = cv2.GaussianBlur(draw, (21, 21), 0)
        draw = cv2.threshold(draw, 20, 255, cv2.THRESH_BINARY)[1]  
        #二值化操作
        draw = cv2.dilate(draw, self.es, iterations = 2)
        contours, hierarchy = cv2.findContours(draw.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for c in contours:
            self.drawCnt(frame, c)
        cv2.imshow("motion detection", frame)
        # if cv2.waitKey(10) & 0xff == ord("q"):
        #     break
            # cv2.destroyAllWindows()
        # camera.release()
        