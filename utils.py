import datetime


def get_family_status(status):
    statuses = {
        1: 'не женат/не замужем',
        2: 'есть друг/есть подруга',
        3: 'помолвлен/помолвлена',
        4: 'женат/замужем',
        5: 'всё сложно',
        6: 'в активном поиске',
        7: 'влюблён/влюблена',
        8: 'в гражданском браке',
        0: 'не указано'
    }

    return statuses[status]


def format_date(date):
    return datetime.datetime.fromtimestamp(date).strftime('%Y-%m-%d %H:%M:%S')
