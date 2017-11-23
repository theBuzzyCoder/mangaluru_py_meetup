import socket
from async.timethis import timeit
from selectors import DefaultSelector, EVENT_READ, EVENT_WRITE

selector = DefaultSelector()
njobs = 0


@timeit
def get_data(path):
    """
    Returns the data sent by the server

    :param str path: url path
    :return: data
    :rtype: str
    """
    global njobs
    sock = socket.socket()
    sock.setblocking(False)
    try:
        sock.connect(('localhost', 5000))
    except BlockingIOError:
        pass

    njobs += 1

    @timeit
    def callback_connected():
        connected(sock, path)
    selector.register(sock.fileno(), EVENT_WRITE, data=callback_connected)


def connected(sock, path):
    buffer = list()
    selector.unregister(sock.fileno())
    request = 'GET {path} HTTP/1.0\r\n\r\n'.format(path=path)
    sock.send(request.encode())

    @timeit
    def callback_readable():
        readable(sock, buffer)
    selector.register(sock.fileno(), EVENT_READ, data=callback_readable)


def readable(sock, buffer):
    global njobs
    chunk = sock.recv(1)  # Receive 128 Bytes data at a time.
    if chunk:
        buffer.append(chunk)
    else:
        selector.unregister(sock.fileno())
        njobs -= 1
        data = b''.join(buffer)
        sock.close()
        with open('job%s' % njobs, mode='w', encoding='utf-8') as f:
            f.write(data.decode('utf-8', 'strict'))
        return


@timeit
def main():
    get_data('/getServerCode')
    get_data('/getServerCode')
    get_data('/')
    while njobs:
        events = selector.select()
        for key, mask in events:
            key.data()
    selector.close()


if __name__ == '__main__':
    main()
