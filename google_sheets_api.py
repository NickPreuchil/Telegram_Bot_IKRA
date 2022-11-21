import requests
import threading
import time
import datetime
import hashlib
import logging
import random

TABLE_WHICH = 'which'
TABLE_FRAME = 'frame'
TABLE_HOW = 'how'
TABLE_1 = '1'
TABLE_2 = '2'
TABLE_3 = '3'
TABLE_4 = '4'
TABLE_5 = '5'
TABLE_6 = '6'

_tables = {
    'which': {
        'link': 'https://docs.google.com/spreadsheets/d/1CRdJHfLuEeD4nkoEvIucVr1_sf9m6ZKEQ6zT31zNQbE/export?format=csv&id=1CRdJHfLuEeD4nkoEvIucVr1_sf9m6ZKEQ6zT31zNQbE&gid=1674921523',
        'cached_content': '',
        'lock': False,
        'last_refreshed': datetime.datetime.now(),
        'last_updated': datetime.datetime.now()
    },
    'frame': {
        'link': 'https://docs.google.com/spreadsheets/d/1CRdJHfLuEeD4nkoEvIucVr1_sf9m6ZKEQ6zT31zNQbE/export?format=csv&id=1CRdJHfLuEeD4nkoEvIucVr1_sf9m6ZKEQ6zT31zNQbE&gid=1111974126',
        'cached_content': '',
        'lock': False,
        'last_refreshed': datetime.datetime.now(),
        'last_updated': datetime.datetime.now()
    },
    'how': {
        'link': 'https://docs.google.com/spreadsheets/d/1CRdJHfLuEeD4nkoEvIucVr1_sf9m6ZKEQ6zT31zNQbE/export?format=csv&id=1CRdJHfLuEeD4nkoEvIucVr1_sf9m6ZKEQ6zT31zNQbE&gid=1962552036',
        'cached_content': '',
        'lock': False,
        'last_refreshed': datetime.datetime.now(),
        'last_updated': datetime.datetime.now()
    },
    '1': {
        'link': 'https://docs.google.com/spreadsheets/d/1CRdJHfLuEeD4nkoEvIucVr1_sf9m6ZKEQ6zT31zNQbE/export?format=csv&id=1CRdJHfLuEeD4nkoEvIucVr1_sf9m6ZKEQ6zT31zNQbE&gid=1650945103',
        'cached_content': '',
        'lock': False,
        'last_refreshed': datetime.datetime.now(),
        'last_updated': datetime.datetime.now()
    },
    '2': {
        'link': 'https://docs.google.com/spreadsheets/d/1CRdJHfLuEeD4nkoEvIucVr1_sf9m6ZKEQ6zT31zNQbE/export?format=csv&id=1CRdJHfLuEeD4nkoEvIucVr1_sf9m6ZKEQ6zT31zNQbE&gid=407960411',
        'cached_content': '',
        'lock': False,
        'last_refreshed': datetime.datetime.now(),
        'last_updated': datetime.datetime.now()
    },
    '3': {
        'link': 'https://docs.google.com/spreadsheets/d/1CRdJHfLuEeD4nkoEvIucVr1_sf9m6ZKEQ6zT31zNQbE/export?format=csv&id=1CRdJHfLuEeD4nkoEvIucVr1_sf9m6ZKEQ6zT31zNQbE&gid=1620518638',
        'cached_content': '',
        'lock': False,
        'last_refreshed': datetime.datetime.now(),
        'last_updated': datetime.datetime.now()
    },
    '4': {
        'link': 'https://docs.google.com/spreadsheets/d/1CRdJHfLuEeD4nkoEvIucVr1_sf9m6ZKEQ6zT31zNQbE/export?format=csv&id=1CRdJHfLuEeD4nkoEvIucVr1_sf9m6ZKEQ6zT31zNQbE&gid=1786079260',
        'cached_content': '',
        'lock': False,
        'last_refreshed': datetime.datetime.now(),
        'last_updated': datetime.datetime.now()
    },
    '5': {
        'link': 'https://docs.google.com/spreadsheets/d/1CRdJHfLuEeD4nkoEvIucVr1_sf9m6ZKEQ6zT31zNQbE/export?format=csv&id=1CRdJHfLuEeD4nkoEvIucVr1_sf9m6ZKEQ6zT31zNQbE&gid=575223293',
        'cached_content': '',
        'lock': False,
        'last_refreshed': datetime.datetime.now(),
        'last_updated': datetime.datetime.now()
    },
    '6': {
        'link': 'https://docs.google.com/spreadsheets/d/1CRdJHfLuEeD4nkoEvIucVr1_sf9m6ZKEQ6zT31zNQbE/export?format=csv&id=1CRdJHfLuEeD4nkoEvIucVr1_sf9m6ZKEQ6zT31zNQbE&gid=1801983427',
        'cached_content': '',
        'lock': False,
        'last_refreshed': datetime.datetime.now(),
        'last_updated': datetime.datetime.now()
    }
}

_refreshing = False

# Рандомная строка из 1-6 таблицы
# Если таблицы нет, вернет ""
# Аргумент - номер таблицы
def get_random_line(table_number) -> str:
    table_number = str(table_number)
    if table_number not in _tables:
        return ''
    table_content = get_table(table_number)

    table_content = table_content.split('\n')
    random_line = random.choice(table_content)
    return random_line



# To be called in other thread
def _endless_refresh(table_name, delay):
    global _refreshing
    if _refreshing:
        return
    _refreshing = True
    try:
        while True:
            try:
                refresh_table(table_name=TABLE_WHICH)
                refresh_table(table_name=TABLE_FRAME)
                refresh_table(table_name=TABLE_HOW)
                refresh_table(table_name=TABLE_1)
                refresh_table(table_name=TABLE_2)
                refresh_table(table_name=TABLE_3)
                refresh_table(table_name=TABLE_4)
                refresh_table(table_name=TABLE_5)
                refresh_table(table_name=TABLE_6)
            except requests.exceptions.ConnectionError:
                time.sleep(5)
            time.sleep(delay)
    except Exception as e:
        _refreshing = False
        raise e


def start_refreshing_all_tables(delay=5):
    all_tables_refresh_thread = threading.Thread(target=_endless_refresh, args=(None, delay))
    all_tables_refresh_thread.start()


def _strip_quotes(table_content) -> str:
    table_content = table_content.replace('"""', '^')
    table_content = table_content.replace('""', '^')
    table_content = table_content.replace('"', '')
    table_content = table_content.replace('^', '"')
    return table_content


def refresh_table(table_name):
    global _tables
    prev_val = _tables[table_name]['cached_content']
    prev_hash = hashlib.sha256(prev_val.encode('UTF-8'))

    res = requests.get(url=_tables[table_name]['link']).content.decode('UTF-8')
    _tables[table_name]['lock'] = True

    if table_name == TABLE_FRAME:
        _tables[table_name]['cached_content'] = _strip_quotes(res)
    else:
        _tables[table_name]['cached_content'] = res.strip()

    new_val = _tables[table_name]['cached_content']
    new_hash = hashlib.sha256(new_val.encode('UTF-8'))
    if prev_hash.hexdigest() != new_hash.hexdigest():
        _tables[table_name]['last_updated'] = datetime.datetime.now()

    _tables[table_name]['lock'] = False
    _tables[table_name]['last_refreshed'] = datetime.datetime.now()


def get_table(table_name) -> str:
    global _tables

    # Обновляем кэш, если пуст
    if _tables[table_name]['cached_content'] == '':
        refresh_table(table_name)

    # Ждем окончания начатой синхронизации
    while _tables[table_name]['lock']:
        time.sleep(0.01)

    return _tables[table_name]['cached_content']


def monitor_last_update_time():
    print('Which table last update        Frame table last update        How table last update')
    while True:
        #pass
        print(f'\r{datetime.datetime.now() - _tables[TABLE_WHICH]["last_updated"]}                   '
              f'{datetime.datetime.now() - _tables[TABLE_FRAME]["last_updated"]}               '
              f'{datetime.datetime.now() - _tables[TABLE_HOW]["last_updated"]}', end='')


def get_last_updated_time(table_name) -> datetime.datetime:
    return _tables[table_name]['last_updated']


def main():
    start_refreshing_all_tables(2)
    monitor_last_update_time()


if __name__ == '__main__':
    main()
