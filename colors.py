import json

class Colors:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            with open('config.json') as f:
                config = json.load(f)
            cls._instance.colors = config["colors"]
        return cls._instance

    def __getattr__(self, name):
        return tuple(self.colors.get(name, [0, 0, 0]))

    @classmethod
    def get_cell_colors(cls):
        instance = cls()
        return [
            instance.dark_grey, instance.green, instance.red,
            instance.orange, instance.yellow, instance.purple,
            instance.cyan, instance.blue,instance.white,
        ]