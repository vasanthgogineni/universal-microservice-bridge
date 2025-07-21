# universal_connector/probe/main.py

import os, yaml
from detect import probe_http
from schema import fetch_openapi
from ai_analyzer import analyze_with_ai

def write_plan(plan: dict, path: str = "/etc/plan/connection-plan.yaml"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        yaml.safe_dump(plan, f)

def main():
    # Read addresses directly (bypass K8s discovery)
    src = os.getenv("SRC_ADDR")
    dst = os.getenv("DST_ADDR")
    if not src or not dst:
        raise RuntimeError("SRC_ADDR and DST_ADDR must be set")

    # Detect protocols
    src_proto = "http" if probe_http(src) else "unknown"
    dst_proto = "http" if probe_http(dst) else "unknown"

    # Fetch schemas
    src_schema = fetch_openapi(src) if src_proto == "http" else {}
    dst_schema = fetch_openapi(dst) if dst_proto == "http" else {}

    # AI analysis (you can stub this if you just want to test proxy)
    ai_spec = analyze_with_ai(src_schema, dst_schema)

    plan = {
        "src": {"address": src, "protocol": src_proto, "auth": ai_spec.get("auth", {})},
        "dst": {"address": dst, "protocol": dst_proto, "auth": ai_spec.get("auth", {})},
        "fieldMappings": ai_spec.get("fieldMappings", {})
    }
    write_plan(plan)
    print("Probe succeeded, plan written to /etc/plan/connection-plan.yaml")

if __name__ == "__main__":
    main()
