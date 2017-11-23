import socket
from async.timethis import timeit


@timeit
def get_data(path):
    """
    Returns the data sent by the server

    :param str path: url path
    :return: data
    :rtype: str
    """
    sock = socket.socket()
    sock.connect(('localhost', 5000))
    connected(sock, path)


@timeit
def connected(sock, path):
    buffer = list()
    request = 'GET {path} HTTP/1.0\r\n\r\n'.format(path=path)
    sock.send(request.encode())
    readable(sock, buffer)


@timeit
def readable(sock, buffer):
    while True:
        chunk = sock.recv(2048)  # Receive 2KB data at a time.
        if chunk:
            buffer.append(chunk)
        else:
            data = b''.join(buffer)
            sock.close()
            with open('job0', mode='w', encoding='utf-8') as f:
                f.write(data.decode('utf-8', 'strict'))
            return


@timeit
def main():
    get_data('/getServerCode')
    get_data('/getServerCode')
    get_data('/')


if __name__ == '__main__':
    main()
