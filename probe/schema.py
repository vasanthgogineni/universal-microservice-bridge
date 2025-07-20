import requests
def fetch_openapi(addr):
    resp = requests.get(f"http://{addr}/openapi.json", timeout=1)
    return resp.json() if resp.ok else None

