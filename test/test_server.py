from catch_camera.server import Server
from catch_camera.client import Client
from config.config import addr_port, resolution, max_connect, output_path

if __name__ == '__main__':
    server = Server(addr_port=addr_port,
                    resolution=resolution,
                    max_connect=max_connect)
    server.receive_run(output_path=output_path)
