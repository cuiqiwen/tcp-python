"""
启动一个TCP服务
聊天室程序
"""
from typing import List
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

all_client_socket: List[socket] = []


def server_read_msg(client_socket: socket, client_info: tuple):
    """接收不了客户端信息"""
    # 保持连接中 并开始与client 保持通讯
    while True:
        data_bytes = client_socket.recv(1024)
        if data_bytes:
            msg = data_bytes.decode("utf-8")
            print(f"server 收到{client_info}消息:{msg}")
            if msg.startswith("Bye"):
                break
            # 服务端回消息给客户端
            # client_socket.send(f"server 收到客户端{client_info}的消息！".encode("utf-8"))
            # 另一种通知 服务端向所有收到的连接 都发送每个连接的消息
            for soc in all_client_socket:
                content = f"{client_info}:{msg}"
                soc.send(content.encode("utf-8"))
    # 关闭客户端连接
    client_socket.close()


def server_run():
    """服务端主程序"""
    server_socket = socket(AF_INET, SOCK_STREAM)
    # 绑定端口
    server_socket.bind(("127.0.0.1", 8080))
    # 监听
    server_socket.listen(1000)
    # loop 保持进程常驻
    while True:
        # 阻塞 等待客户端连接 若有连接 则往下执行 否则等待
        client_socket, client_info = server_socket.accept()
        all_client_socket.append(client_socket)
        print(f"server 收到客户端{client_info} 连接请求 并自动开启线程处理")
        # 开启线程处理该连接
        thread1 = Thread(target=server_read_msg, args=(client_socket, client_info))
        thread1.start()


if __name__ == "__main__":
    print("\033[0;49;32mTCP server starting...\033[0m")
    server_run()
