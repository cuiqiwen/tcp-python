"""
启动一个TCP服务
聊天室程序
"""
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread


def client_read_msg(client_socket: socket):
    """客户端接收服务端消息"""
    while True:
        data_bytes = client_socket.recv(1024)
        if data_bytes:
            msg = data_bytes.decode("utf-8")
            print(f"client 收到消息:{msg}")


def client_write_msg(client_socket: socket):
    """发送消息给服务端"""
    while True:
        msg = input("输入消息>")
        msg = f"{msg}"
        client_socket.send(msg.encode("utf-8"))


def client_run():
    """开启客户端程序"""
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect(("127.0.0.1", 8080))
    # 开启线程接收服务端消息
    read_thread = Thread(target=client_read_msg, args=(client_socket,))
    read_thread.start()
    # 开启线程 发送用户输入消息给服务端
    write_thread = Thread(target=client_write_msg, args=(client_socket,))
    write_thread.start()


if __name__ == "__main__":
    print("\033[0;49;32mTCP client starting...\033[0m")
    client_run()
