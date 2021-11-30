from video_surveillance.server import Server
from video_surveillance.client import Client
from config.config import addr_port, resolution, iamge_quality,input_path



if __name__ == '__main__':
    client = Client(addr_port=addr_port,
                    resolution=resolution,
                    iamge_quality=iamge_quality)
    if client.connect():
        client.send2server(input_path=input_path)