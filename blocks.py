from block import Block
from position import Position
import json


class BlockFactory:
    def __init__(self, config):
        self.config = config["blocks"]
        self.block_classes = {
            "I": self.create_block,
            "J": self.create_block,
            "L": self.create_block,
            "O": self.create_block,
            "S": self.create_block,
            "T": self.create_block,
            "Z": self.create_block,
        }

    def create_block(self, block_type):
        block_config = self.config[block_type]
        block = Block(id=block_config["id"])
        block.cells = {
            int(rot): [Position(*pos) for pos in cells]
            for rot, cells in block_config["cells"].items()
        }
        block.move(*block_config["initial_offset"])
        return block

    def get_all_blocks(self):
        return [self.create_block(block_type) for block_type in self.config.keys()]
