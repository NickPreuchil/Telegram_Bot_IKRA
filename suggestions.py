import json


# Добавить предложение
# Аргумент - строка, предложение
# Возвращает None
def suggest(message) -> None:
    with open('suggestions.json', 'r') as f:
        data = json.load(f)
        data['suggestions'].append(message)
    with open('suggestions.json', 'w') as f:
        json.dump(data, f)


# Получить предложения
# Аргументы - нет
# Возвращает список предложений
def get_suggestions() -> list:
    with open('suggestions.json', 'r') as f:
        data = json.load(f)
        return data['suggestions']


# Очистить предложения
# Аргументы - нет
# Возвращает количество удаленных предложений
def clear() -> int:
    cleared = 0
    with open('suggestions.json', 'r') as f:
        data = json.load(f)
        cleared = len(data['suggestions'])
        data['suggestions'] = []
    with open('suggestions.json', 'w') as f:
        json.dump(data, f)
    return cleared


if __name__ == '__main__':
    print(get_suggestions())
