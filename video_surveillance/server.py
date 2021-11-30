import socket
import time
import cv2
import struct
import numpy
import threading

from video_surveillance.target_detection import TargetDetection


class Server:
    def __init__(self,
                 addr_port: tuple = ('127.0.0.1', 11000),
                 max_connect: int = 32,
                 resolution: tuple = (640, 480)):
        # 设置tcp服务端的socket
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 设置重复使用
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        # 绑定地址和端口
        self.server.bind(addr_port)

        self.server.listen(max_connect)
        self.resolution = resolution

    # def run(self):
    #     while True:
    #         print('等待客户端连接')
    #         # 等待客户端连接
    #         client, addr = self.server.accept()
    #         ProcessClient(client).start()

    def receive_image(self,
                      interval: float = 0.1,
                      output_path: str = "./output_path.avi",
                      detect_flag: bool = False):
        video_fourcc = cv2.VideoWriter_fourcc(*'XVID')
        video_write = cv2.VideoWriter(output_path, video_fourcc, 30,
                                      self.resolution)
        taget_detection = TargetDetection()
        while True:
            # time.sleep(interval)
            data = self.client.recv(8)
            if not data:
                print("no data")
                break
            # 图片的长度 图片的宽高
            length, width, height = struct.unpack('ihh', data)

            img_buf = b''
            # 存放最终的图片数据
            while length:
                # 接收图片
                temp_size = self.client.recv(length)
                length -= len(temp_size)
                # 每次减去收到的数据大小
                img_buf += temp_size
                # 每次收到的数据存到img里
            # 把二进制数据还原
            data = numpy.frombuffer(img_buf, dtype='uint8')
            # 还原成矩阵数据
            image = cv2.imdecode(data, cv2.IMREAD_UNCHANGED)
            #cv2.imshow('win1', image)
            video_write.write(image)
            # key = cv2.waitKey(0)
            if (detect_flag):
                taget_detection.run_detection(image)
            else:
                cv2.imshow('frame', image)
            if cv2.waitKey(10) == 27:
                # 按下ESC时，退出
                self.client.close()
                cv2.destroyAllWindows()
                break
        video_write.release()

    def receive_run(self,
                    output_path: str = "./output_path.avi",
                    detect_flag: bool = False):
        while True:
            print('等待客户端连接')
            # 等待客户端连接
            self.client, self.addr = self.server.accept()
            self.name = self.addr[0] + " Camera"
            print(self.name)
            receive_thread = threading.Thread(target=self.receive_image,
                                              kwargs={
                                                  "output_path": output_path,
                                                  "detect_flag": detect_flag
                                              })
            receive_thread.start()
            receive_thread.join()


# class ProcessClient(threading.Thread):
#     def __init__(self, client):
#         super().__init__()
#         self.client = client
#         # 创建一个窗口

#     def run(self,
#             interval: float = 0.1,
#             output_path: str = "./output_path.avi",
#             resolution: tuple = (640, 480)):
#         video_fourcc = cv2.VideoWriter_fourcc(*'XVID')
#         video_write = cv2.VideoWriter(output_path, video_fourcc, 30,
#                                       resolution)
#         while True:
#             # time.sleep(interval)
#             data = self.client.recv(8)
#             if not data:
#                 print("no data")
#                 break
#             # 图片的长度 图片的宽高
#             length, width, height = struct.unpack('ihh', data)

#             imgg = b''  # 存放最终的图片数据
#             while length:
#                 # 接收图片
#                 temp_size = self.client.recv(length)
#                 length -= len(temp_size)  # 每次减去收到的数据大小
#                 imgg += temp_size  # 每次收到的数据存到img里
#             # 把二进制数据还原
#             data = numpy.frombuffer(imgg, dtype='uint8')
#             # 还原成矩阵数据
#             image = cv2.imdecode(data, cv2.IMREAD_UNCHANGED)
#             #cv2.imshow('win1', image)
#             video_write.write(image)
#             key = cv2.waitKey(60) & 0xff
#             if key == 27:  # 按下ESC时，退出
#                 break
#         video_write.release()
#         # cv2.destroyAllWindows()

if __name__ == '__main__':
    server = Server()
    server.receive_run()
