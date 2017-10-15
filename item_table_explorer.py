from pathlib import Path
from typing import List

from selenium.webdriver.remote.webelement import WebElement

from item_page_explorer import ItemPageExplorer, ItemTableType
from state import State


class ItemTableExplorer:

    def __init__(self, driver, table, file):
        self.file = file
        self.table = table
        self.driver = driver
        try:
            self.state = State.from_file()
        except IOError:
            self.state = State()

    def explore(self):
        type = ItemTableType.active if self.file == 'active_items.csv' else ItemTableType.passive
        if not self.state.header:
            header: List[WebElement] = self.table.find_element_by_tag_name('thead').find_elements_by_tag_name('th')
            header = [el.text.replace("\n", "") for el in header]
            header[1:1] = ['Item Pool', 'Unlock Method', 'Page link']
            self.state.header = header
        if not self.state.items_table:
            active_items = self.table.find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')
            active_items = [self.mine_data(item) for item in active_items]
            self.state.items_table = active_items
        if self.state.last_item_visited_index < len(self.state.items_table):
            ItemPageExplorer(self.driver, self.state, type).explore()
        return self.state.table_with_header

    def mine_data(self, item):
        line = []
        for i, attr in enumerate(item.find_elements_by_tag_name('td')):
            if i == 0:
                itempage_link = attr.find_element_by_tag_name('a')
                itemname = itempage_link.text
                line.append(itemname)
                line.append(itempage_link.get_property('href'))
            elif i == 2:
                img_link = attr.find_element_by_tag_name('a').get_property('href')
                line.append(img_link)
            else:
                line.append(attr.text.replace("\n", " "))
        return line



