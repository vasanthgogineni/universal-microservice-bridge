import socket, ssl

def probe_http(addr, timeout=0.5):
    host, port = addr.split(':')
    s = socket.create_connection((host, int(port)), timeout=timeout)
    s.send(b"GET / HTTP/1.1\r\nHost: %b\r\n\r\n" % host.encode())
    return b"HTTP/" in s.recv(1024)

