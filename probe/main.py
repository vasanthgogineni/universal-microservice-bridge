import yaml, os
from discover import discover_endpoints
from detect import probe_http, probe_grpc, probe_amqp, probe_kafka
from schema import fetch_openapi
from ai_analyzer import analyze_with_ai

def detect_protocol(addr):
    if probe_http(addr): return "http"
    if probe_grpc(addr): return "grpc"
    # …

def write_plan(plan, path="/etc/plan/connection-plan.yaml"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f: yaml.safe_dump(plan, f)

def main():
    src = discover_endpoints("connect-from=myapp")
    dst = discover_endpoints("connect-to=other")
    src_proto, dst_proto = detect_protocol(src), detect_protocol(dst)
    src_schema = fetch_openapi(src) if src_proto=="http" else None
    dst_schema = fetch_openapi(dst) if dst_proto=="http" else None
    ai_spec = analyze_with_ai(src_schema, dst_schema)
    plan = {
      "src": {"address": src, "protocol": src_proto, "auth": ai_spec["auth"]},
      "dst": {"address": dst, "protocol": dst_proto, "auth": ai_spec["auth"]},
      "transform": ai_spec.get("fieldMappings", {})
    }
    write_plan(plan)

if __name__=="__main__": main()
