# universal_connector/connector/plugins/transforms.py
class FieldMap:
    def __init__(self, src_field, dst_field):
        self.src = src_field
        self.dst = dst_field
    def apply(self, message: dict) -> dict:
        if self.src in message:
            message[self.dst] = message.pop(self.src)
        return message