import time
import threading
from multiprocessing import Process
from socket import socket


def get_data(path):
    buff = []
    sock = socket()
    sock.connect(('localhost', 5000))
    request = 'GET {} HTTP/1.1\r\n\r\nHost: {}'.format(path, 'localhost')
    sock.send(request.encode('ascii'))
    data = sock.recv(4096)
    while data:
        buff.append(data)
        data = sock.recv(4096)
    else:
        resp = b''.join(buff).decode()
        print(resp.splitlines()[0])


def thread_approach():
    threads = []
    args = ['/getServerCode', '/getServerCode']
    for i in range(2):
        t = threading.Thread(target=get_data, args=(args[i],))
        threads.append(t)

    for t in threads:
        t.start()
    
    for t in threads:
        t.join()


def synchronous_approach():
    get_data('/getServerCode')
    get_data('/getServerCode')


def multiprocess_approach():
    processes = []
    args = ['/getServerCode', '/getServerCode']
    for i in range(2):
        p = Process(target=get_data, args=(args[i],))
        processes.append(p)
        
    for p in processes:
        p.start()

    for p in processes:
        p.join()


if __name__ == '__main__':
    start = time.time()
    synchronous_approach()
    end = time.time()
    print("%s Took %.2f seconds" % (synchronous_approach.__name__, end - start))
    
    start = time.time()
    thread_approach()
    end = time.time()
    print("%s Took %.2f seconds" % (thread_approach.__name__, end - start))

    start = time.time()
    multiprocess_approach()
    end = time.time()
    print("%s Took %.2f seconds" % (multiprocess_approach.__name__, end - start))