import socket
import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops

def recvall(sock, n):
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return
        data.extend(packet)
    return data

host = "84.237.21.36"
port = 5152

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((host, port))
    plt.ion()

    for i in range(10):
        sock.send(b"get")
        data = recvall(sock, 40_002)
        if not data:
            break

        image = np.frombuffer(data[2:], dtype="uint8").reshape(data[0], data[1])
        binary = (image >= np.max(image) * 0.7)
        labeled = label(binary)
        regions = regionprops(labeled)

        if len(regions) == 2:
            d = round(np.linalg.norm(np.array(regions[0].centroid) - np.array(regions[1].centroid)), 1)
            sock.send(f"{d}".encode())
            answer = sock.recv(6).decode()
            print(f"{i + 1} картинка, дистанция = {d}")

            plt.clf()
            plt.title(f"{i + 1} картинка, {answer}, дистанция: {d}")
            plt.subplot(1, 2, 1)
            plt.imshow(image)
            plt.subplot(1, 2, 2)
            plt.imshow(labeled)
            plt.pause(0.01)

        sock.send(b"beat")
        beat = sock.recv(6)