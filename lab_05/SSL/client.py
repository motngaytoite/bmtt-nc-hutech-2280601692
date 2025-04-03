import socket
import ssl
import threading

server_address = ('localhost', 12346)

def receive_data(ssl_socket):
    try:
        while True:
            data = ssl_socket.recv(1024)
            if not data:
                break
            print("Nhận:", data.decode('utf-8'))
    except Exception as e:
        print("Lỗi nhận dữ liệu:", e)
    finally:
        ssl_socket.close()
        print("Kết nối đã đóng.")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

context = ssl.SSLContext(ssl.PROTOCOL_TLS)
context.verify_mode = ssl.CERT_NONE 
context.check_hostname = False

ssl_socket = context.wrap_socket(client_socket, server_hostname="localhost")

try:
    ssl_socket.connect(server_address)

    receive_thread = threading.Thread(target=receive_data, args=(ssl_socket,))
    receive_thread.start()

    while True:
        message = input("Nhập tin nhắn: ")
        ssl_socket.send(message.encode('utf-8'))
except ConnectionRefusedError:
    print("Không thể kết nối đến server. Kiểm tra lại server và cổng.")
except KeyboardInterrupt:
    print("\nNgắt kết nối.")
finally:
    ssl_socket.close()
