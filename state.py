from pathlib import Path

import yaml

class State:

    state_file = Path(__file__).parent / 'state.yaml'

    def __init__(self):
        self.items_table = None
        self.items_extra_data = []
        self.last_item_visited_name = None
        self.last_item_visited_index = 0
        self.header = None

    def serialize(self):
        yaml.dump(self, open(self.state_file, 'w'))

    @classmethod
    def from_file(cls) -> 'State':
        return yaml.load(open(cls.state_file))

    @property
    def table_with_header(self):
        return [self.header] + self.items_table