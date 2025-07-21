# universal_connector/probe/detect.py
import socket

def probe_http(addr: str, timeout: float = 0.5) -> bool:
    host, port = addr.split(":")
    try:
        s = socket.create_connection((host, int(port)), timeout=timeout)
        s.send(b"GET / HTTP/1.1\r\nHost: %b\r\n\r\n" % host.encode())
        data = s.recv(1024)
        return b"HTTP/" in data
    except Exception:
        return False