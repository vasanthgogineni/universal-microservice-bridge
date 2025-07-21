# universal_connector/probe/schema.py
import requests

def fetch_openapi(addr: str) -> dict:
    try:
        resp = requests.get(f"http://{addr}/openapi.json", timeout=1)
        return resp.json() if resp.ok else {}
    except Exception:
        return {}