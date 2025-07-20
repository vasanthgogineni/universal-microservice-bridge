import importlib
class Runtime:
    def __init__(self, plan): self.plan=plan
    def start(self):
        src_plug = importlib.import_module(f"plugins.{self.plan['src']['protocol']}_adapter")
        dst_plug = importlib.import_module(f"plugins.{self.plan['dst']['protocol']}_adapter")
