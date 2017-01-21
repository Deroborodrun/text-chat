import socket
import threading
import logging

from constants import SERVER_HOST, SERVER_PORT, BUFFER_SIZE
import utils

log = utils.get_logger(__name__, log_level=logging.ERROR)

def recv_loop(connection):
    """Process  connection in infinity loop"""
    while True:
        try:
            message = connection.recv(BUFFER_SIZE)
        except ConnectionResetError:
            log.warning("Sever is down")
            break
        if not message:
            log.debug("Disconnected")
            return
        print(message.decode("utf-8"))


def main():
    name = input("Enter your name:")
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print("Connecting to server")
    try:
        soc.connect((SERVER_HOST, SERVER_PORT))
    except OSError as e:
        log.critical('Get error on connection to the server ({}:{}) "{}"'
                     .format(SERVER_HOST, SERVER_PORT, e))
        return
    log.debug("Starting receive thread")
    threading.Thread(target=recv_loop, args=[soc]).start()
    while True:
        input_text = input('>')
        if input_text == 'exit':
            break
        soc.send((name + " : " + input_text).encode('utf-8'))


if __name__ == '__main__':
    main()
