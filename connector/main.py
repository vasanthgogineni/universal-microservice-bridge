# universal_connector/connector/main.py
from plan import load_plan
from runtime import Runtime

if __name__ == "__main__":
    plan = load_plan()
    rt = Runtime(plan)
    rt.start()