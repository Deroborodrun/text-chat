import socket
import threading

from constants import SERVER_HOST, SERVER_PORT, BUFFER_SIZE
from utils import get_logger

connections = set()
log = get_logger(__name__)

def send_all(message):
    """Send message to all participants"""
    for con in connections:
        log.debug("Sending {}".format(message))
        try:
            con.send(''.join([message, '\n']).encode('utf-8'))
        except Exception as e:
            log.critical("An error on sending message to all users: {}"
                         .format(e))

def receive(con):
    """Respond processing """
    while True:
        log.debug("Waiting for message")
        try:
            message = con.recv(BUFFER_SIZE).decode("utf-8")
        except ConnectionResetError:
            connections.remove(con)
            log.debug("user left this chat")
            return
        if not message:
            log.debug("Closing connection and removing from registry")
            connections.remove(con)
            return
        log.debug("Received %s, sending to all" % message)
        send_all(message)

def main():
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        soc.bind((SERVER_HOST, SERVER_PORT))
    except OSError as e:
        log.critical('Get error on start ({}:{}) "{}"'
                     .format(SERVER_HOST, SERVER_PORT, e))
        return
    soc.listen(10)
    while True:
        log.debug("Waiting for a connection")
        (connection, address) = soc.accept()
        log.debug("Connection received. {} Adding to registry"
                  .format(address))
        connections.add(connection)
        log.debug("Spawning receiver")
        threading.Thread(target=receive, args=[connection]).start()

if __name__ == '__main__':
    main()
