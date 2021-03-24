import requests
import vk_api
from emoji import emojize
from config import VK_TOKEN, WEATHERSTACK_API_KEY
from utils import format_date, get_family_status


class VkBot:

    vk = vk_api.VkApi(token=VK_TOKEN)
    api = vk.get_api()

    def __init__(self, user_id):
        self._USER_ID = user_id
        self._USERNAME = self._get_user_name_from_vk_id(user_id)
        self._COMMANDS = ["ПРИВЕТ", "ПОГОДА", "ПОКА", "ПОЛЬЗОВАТЕЛЬ"]

    def _get_user_name_from_vk_id(self, user_id):
        user = self.api.users.get(user_id=user_id)
        return user[0].get('first_name')

    def _get_user_info(self, user):
        try:
            user = self.api.users.get(user_ids=user, fields=[
                'bdate', 'relation', 'city', 'last_seen', 'domain'])
        except:
            return 'Такой пользователь не найден'

        id = user[0].get('id')
        first_name = user[0].get('first_name')
        last_name = user[0].get('last_name')

        bdate = user[0].get('bdate')
        relation = user[0].get('relation')

        if relation:
            relation = get_family_status(relation)

        city = user[0].get('city').get('title')
        last_seen = format_date(user[0].get('last_seen').get('time'))
        domain = 'https://vk.com/' + user[0].get('domain')

        return f'''{first_name} {last_name}\n Id: {id}\nСтраница: {domain}
            Дата рождения: {bdate}\n Семейное положение: {relation}
            Город: {city}\n Был(а) в сети: {last_seen}'''

    def _get_weather(self, city: str = "Москва") -> str:
        params = {'access_key': WEATHERSTACK_API_KEY, 'query': city}
        api_result = requests.get(
            'http://api.weatherstack.com/current', params)
        api_response = api_result.json()

        if api_response.get('request'):
            temp = api_response['current']['temperature']
            feelslike = api_response['current']['feelslike']
            country = api_response['location']['country']
            res = f'Погода в городе {city.capitalize()} ({country}): {temp}°\nОщущается как {feelslike}°'
        else:
            res = 'К сожалению, информации о погоде в данном городе нет. Попробуй другой.'

        return res

    @staticmethod
    def _clean_all_tag_from_str(string_line):
        result = ""
        not_skip = True
        for i in list(string_line):
            if not_skip:
                if i == "<":
                    not_skip = False
                else:
                    result += i
            else:
                if i == ">":
                    not_skip = True

        return result

    def new_message(self, message):
        # Привет
        if message.upper() == self._COMMANDS[0]:
            SMILE = '👋'
            return f'Привет-привет, {self._USERNAME}! {emojize(SMILE)}'

        # Погода
        elif message.upper().split(' ')[0] == self._COMMANDS[1]:
            try:
                city = message.split(' ')[1]
                return self._get_weather(city)
            except:
                return 'Пожалуйста, укажи город через пробел\n (прим. Погода Москва)'

        # Пока
        elif message.upper() == self._COMMANDS[2]:
            return f'Пока-пока, {self._USERNAME}!'

        # Пользователь
        elif message.split(' ')[0].upper() == self._COMMANDS[3]:
            try:
                user = message.split(' ')[1]
                return self._get_user_info(user)
            except:
                return 'Пожалуйста, введи id/nickname нужного пользователя\n (прим. Пользователь 123)'

        else:
            SMILE = '🤔'
            return f'''Не понимаю тебя {emojize(SMILE)}
            Знаю команды "Привет", "Пока", "Погода", "Пользователь.'''
