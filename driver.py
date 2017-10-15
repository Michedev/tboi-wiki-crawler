import logging
from os import getenv
from pathlib import Path

import sys
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

from item_table_explorer import ItemTableExplorer
from logsetup import config_log

HOME = Path(getenv('HOME'))

def load_extension(id_extensions, options=None):
    basepath = HOME / ".config/chromium/Default/Extensions"
    if isinstance(id_extensions, list):
        arg = ','.join([str(basepath/id_extension) for id_extension in id_extensions])
    else:
        arg = str(basepath / id_extensions)
    options = options or webdriver.ChromeOptions()
    options.add_argument('--load-extension=' + arg)
    return options


config_log()
home_url = Path('http://bindingofisaacrebirth.gamepedia.com')
itemtable_url = home_url / 'Item'
options = webdriver.ChromeOptions()
options.add_argument("--disable-popup-blocking")
adblock_id = "gighmmpiobklfepjocnamgkkbiglidom/3.13.0_0"
options = load_extension(adblock_id, options)
driver = webdriver.Chrome(chrome_options=options)
driver.implicitly_wait(1)
driver.get(str(itemtable_url))
actives, passives, _ = driver.find_elements_by_tag_name('table')
file = 'passive_items.csv'
table = actives if file == 'active_items.csv' else passives
item_explorer = ItemTableExplorer(driver, table, file)
sep = "@"
try:
    data = item_explorer.explore()
    with open(Path(__file__).parent / file, 'w') as f:
        text = '\n'.join((sep.join((str(el) for el in line)) for line in data))
        f.write(text)

except Exception as e:
    item_explorer.state.serialize()
    logging.error(f"Catched exeception: {str(e.with_traceback(sys.exc_traceback))}")

