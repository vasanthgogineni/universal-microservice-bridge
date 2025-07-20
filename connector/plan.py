import yaml
def load_plan(path="/etc/plan/connection-plan.yaml"):
    return yaml.safe_load(open(path))
