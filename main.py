
import os
import vk_api
from vk_api.longpoll import VkEventType, VkLongPoll
from config import VK_TOKEN
from vk_bot import VkBot


def main():

    def write_msg(user_id, message, random_id):
        vk.method('messages.send', {'user_id': user_id,
                                    'message': message, "random_id": random_id})

    vk = vk_api.VkApi(token=VK_TOKEN)

    longpoll = VkLongPoll(vk)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:

                print('New message:')
                print(f'For me by: {event.user_id}', end='')

                bot = VkBot(event.user_id)
                write_msg(event.user_id, bot.new_message(
                    event.text), random_id=event.random_id)

                print('Text: ', event.text)


if __name__ == '__main__':
    main()
