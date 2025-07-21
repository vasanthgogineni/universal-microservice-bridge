# universal_connector/connector/plugins/http_adapter.py
import uvicorn
from fastapi import FastAPI, Request, Response
import httpx
import yaml

class Adapter:
    def __init__(self, config):
        self.config = config
        self.app = FastAPI()
        self._setup_routes()

    def _setup_routes(self):
        plan = self.config
        dst = plan["address"]
        @self.app.api_route("/{path:path}", methods=["GET","POST","PUT","DELETE","PATCH"])
        async def proxy(path: str, request: Request):
            body = await request.json() if request.method != "GET" else None
            headers = dict(request.headers)
            url = f"http://{dst}/{path}"
            async with httpx.AsyncClient() as client:
                resp = await client.request(request.method, url, json=body, headers=headers)
            return Response(content=resp.content, status_code=resp.status_code, headers=resp.headers)

    def listen(self, handler):
        uvicorn.run(self.app, host="0.0.0.0", port=8080)

    def send(self, message):
        # Not used for HTTP source
        pass
