import socket
import struct
import time
import traceback
import cv2
import numpy


class Client(object):
    def __init__(self,
                 addr_port: tuple = ('127.0.0.1', 11000),
                 resolution: tuple = (640, 480),
                 iamge_quality: int = 100):
        # 连接的服务器的地址
        # 连接的服务器的端口
        self.addr_port = addr_port
        # 创建套接字
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 地址端口可以复用
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # 分辨率
        self.resolution = resolution
        self.iamge_quality = iamge_quality

    def connect(self):
        """链接服务器"""
        flag = False
        try:
            self.client.connect(self.addr_port)
            print('连接成功')
            flag = True
        except Exception as e:
            traceback.print_exc()
            print('连接失败')
        return flag

    def send2server(self,
                    interval: float = 0.5,
                    image_format: str = '.jpg',
                    input_path=None):
        """读摄像头数据 发送给服务器"""
        if input_path is None:
            # 摄像头对象
            camera = cv2.VideoCapture(0)
        else:
            # 读取本地视频
            camera = cv2.VideoCapture(input_path)
        print('isOpened:', camera.isOpened())
        while camera.isOpened():
            try:
                # 获取摄像头数据
                ret, frame = camera.read()
                # 对每一帧图片做大小处理　和大小的压缩
                if (ret):
                    # print(ret)
                    frame = cv2.resize(frame, self.resolution)
                # 参1图片后缀名 参2 原图片的数据 参3图片质量 0-100 越大越清晰
                _, img = cv2.imencode(
                    image_format, frame,
                    [cv2.IMWRITE_JPEG_QUALITY, self.iamge_quality])
                # img 是被压缩后的数据 无法正常显示
                #print(img)
                print('sender image frame')
                #print(img.tostring())
                # 转换为numpy格式数据
                img_code = numpy.array(img)
                # 转为二进制数据
                img = img_code.tobytes()
                # 获取数据长度
                length = len(img)
                # 发送的数据  大小 宽 高 图片数据
                # 数据打包变为二进制
                # pack方法参数1 指定打包数据的数据大小  i 4字节 h代表2字节
                all_data = struct.pack('ihh', length, self.resolution[0],
                                       self.resolution[1]) + img
                self.client.send(all_data)
                time.sleep(interval)
            except:
                camera.release()
                # 释放摄像头
                traceback.print_exc()
                return


if __name__ == '__main__':
    client = Client()
    if client.connect():
        client.send2server()
