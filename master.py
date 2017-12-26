import socket
import socketserver
import threading
import os
from multiprocessing import Pool, Process



# 自检

# 发送4G代理广播
# 拥有4G的主机回复该广播
# 未拥有4G的主机不回应

def self_check():

    # 网卡信息
    # 4g信息
    if check_wan():
        # true - 有4G
        # 建立内网主机应答服务器
        # 随时更新端口映射队列
        p_lan_response = Process(target=lan_response)
        p_lan_response.start()
    else:
        # false - 无4G
        pass

def check_wan():
    if os.name == 'nt':
        if os.system("ping -n 1 8.8.8.8") == 0:
            return True
        else:
            return False

def lan_response():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', 9191))


def _boardcast(message):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', 9191))
    addr = (('255.255.255.255', 9191))
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.sendto(message.encode(encoding='utf-8'), addr)
    data = None
    while True:
        data = s.recvfrom(1024)
        print(data)
        break
    s.sendto()

class _4g_handler(socketserver.BaseRequestHandler):
    # 接收指令
    # 接收端口映射申请
    def handle(self):
        data = str(self.request.recv(1024), 'ascii')
        cur_thread = threading.current_thread()
        response = bytes("{}: {}".format(cur_thread.name, data), 'ascii')
        self.request.sendall(response)

class _non_4g_handler(socketserver.BaseRequestHandler):
    # 接收指令
    def handle(self):
        pass

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


if __name__ == '__main__':
    self_check()