import yaml
import uvicorn
from fastapi import FastAPI, Request, Response
import httpx

app = FastAPI()
plan = yaml.safe_load(open("/etc/plan/connection-plan.yaml"))
dst_addr = plan["dst"]["address"]
transformations = plan.get("transform", {})

async def apply_transforms(payload: dict) -> dict:
    for src_field, dst_field in transformations.items():
        if src_field in payload:
            payload[dst_field] = payload.pop(src_field)
    return payload

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy(path: str, request: Request):
    body = await request.json() if request.method != "GET" else None
    headers = dict(request.headers)
    method = request.method

    if body is not None:
        body = await apply_transforms(body)

    url = f"http://{dst_addr}/{path}"
    async with httpx.AsyncClient() as client:
        resp = await client.request(method, url, json=body, headers=headers)

    return Response(
        content=resp.content,
        status_code=resp.status_code,
        headers=resp.headers,
        media_type=resp.headers.get("content-type"),
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
