from enum import Enum
from typing import List

import logging
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement

from state import State

class ItemTableType(Enum):
    active = 'active'
    passive = 'passive'

class ItemPageExplorer:
    
    def __init__(self, driver, state: State, type: ItemTableType):
        self.type = type
        self.state = state
        self.driver = driver
        self.index = 0

    def explore(self):
        logging.debug(f"Start to explore items page from index {self.state.last_item_visited_index}")
        self.index = self.state.last_item_visited_index
        items_unvisited = self.state.items_table[self.index:]
        for line in items_unvisited:
            self.mine_data(line)
        logging.debug(f"Finish successfully item pages exploration."
                      f" Total page explored: {self.state.last_item_visited_index}"
                      f" - Last item name explored: {self.state.last_item_visited_name}")
        return self.state.items_table

    def mine_data(self, line):
        pagedata = []
        itemname, item_url, *_ = line
        self.driver.get(str(item_url))
        itemtable = self.get_itemtable()
        rows = itemtable.find_elements_by_tag_name('tr')
        i = self.index_row_with_text(rows, 'Item Pool')
        if i != -1:
            row_item_pool = rows[i + 1]
            pagedata.append(self.item_pools(row_item_pool))
        else:
            pagedata.append(None)
        i = self.index_row_with_text(rows, 'Unlock Method')
        if i != -1:
            unlock_method = rows[i + 1].text
            pagedata.append(unlock_method)
        else:
            pagedata.append('Yet unlocked')
        logging.info(f'Data from itempage: {pagedata}')
        line[1:1] = pagedata
        print(line)
        print(self.state.items_table[self.index])
        self.update_state(line, pagedata, itemname)

    def index_row_with_text(self, rows: List[WebElement], text):
        for i, row in enumerate(rows):
            try:
                if row.find_element_by_tag_name('th').text == text:
                    return i
            except NoSuchElementException:
                continue
        return -1

    def item_pools(self, row_item_pool) -> List[List[str]]:
        links: List[WebElement] = row_item_pool.find_elements_by_tag_name('a')
        img_item_pool = []
        for i in range(0, len(links), 2):
            try:
                img_link = links[i].find_element_by_tag_name('img').get_property('src')
            except NoSuchElementException:
                i = i+1
                img_link = None
            if len(links) > i+1:
                item_pool_name = links[i + 1].text
            else:
                item_pool_name = None
            img_item_pool.append([img_link, item_pool_name])
        return img_item_pool

    def get_itemtable(self):
        try:
            itemtable: WebElement = self.driver.find_elements_by_tag_name('table')[0]
            return itemtable
        except IndexError:
            self.driver.refresh()
            return self.get_itemtable()

    def update_state(self, line, itempagedata, itemname):
        self.state.items_table[self.index] = line
        self.index += 1
        self.state.last_item_visited_index = self.index
        self.state.last_item_visited_name = itemname
        self.state.items_extra_data.append(itempagedata)



