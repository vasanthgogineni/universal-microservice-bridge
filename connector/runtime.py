import importlib

class Runtime:
    def __init__(self, plan: dict):
        self.plan = plan

    def start(self):
        # Normalize protocols: default any unknown to http
        src_proto = self.plan['src']['protocol']
        dst_proto = self.plan['dst']['protocol']
        if src_proto not in ("http", "grpc", "amqp"):
            src_proto = "http"
        if dst_proto not in ("http", "grpc", "amqp"):
            dst_proto = "http"

        # load adapters from the top‑level plugins/ directory
        src_mod = importlib.import_module(f"plugins.{src_proto}_adapter")
        dst_mod = importlib.import_module(f"plugins.{dst_proto}_adapter")
        src_adapter = src_mod.Adapter(self.plan["src"])
        dst_adapter = dst_mod.Adapter(self.plan["dst"])

        # load transforms from plugins/transforms.py
        from plugins.transforms import FieldMap
        transforms = [FieldMap(s, d) for s, d in self.plan.get("fieldMappings", {}).items()]

        # wire adapter → transforms → adapter
        src_adapter.listen(lambda msg: self._forward(msg, dst_adapter, transforms))

    def _forward(self, msg, dst_adapter, transforms):
        for t in transforms:
            msg = t.apply(msg)
        dst_adapter.send(msg)
