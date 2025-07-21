# universal_connector/connector/plan.py
import yaml

def load_plan(path: str = "/etc/plan/connection-plan.yaml") -> dict:
    with open(path) as f:
        return yaml.safe_load(f)