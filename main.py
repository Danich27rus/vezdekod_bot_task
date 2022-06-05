# -*- coding: cp1251 -*-
import vk_api
import random
from collections import Counter
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api import VkUpload
from vk_api.utils import get_random_id
from vk_api.keyboard import VkKeyboard

token = 'aed776a58d7eac4d1a2f52dfa2f7659791a61cb350c4944a4e40010271e66e7184670aaa8ef19978ef5a7'
vk_session = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk_session, group_id=213720712)
upload = VkUpload(vk_session)

random_img_words = \
    [line.split('\t') for line in open('C:/repos git/vezdekod_bot_task/Имаджинариум/vezdekod_bot_taskwords.txt')]


def write_msg(user_id, message, attachments, keyboard):
    vk_session.method('messages.send', {'user_id': user_id,
                                        'message': message,
                                        'attachment': ','.join(attachments),
                                        'random_id': get_random_id(),
                                        'keyboard': keyboard})


def write_msg_text(user_id, message):
    vk_session.method('messages.send', {'user_id': user_id,
                                        'message': message,
                                        'random_id': get_random_id()})


user = {'user_id': 0,
        'cards': [],
        'words': [],
        'points': 0}
pseudo_user = {'id': 0,
               'cards': []}
all_cards_list = []


def random_words_for_each_img(sentences):
    words = []
    for i in sentences:
        list_words = i.split()
        list_words_len = random.randint(0, len(list_words)-1)
        word = list_words[list_words_len]
        if word not in words:
            words.append(word)
        else:
            remember = word
            while word == remember:
                list_words_len = random.randint(0, len(list_words) - 1)
                word = list_words[list_words_len]
    return words


def create_keyboard(words):
    keyboard = vk_api.keyboard.VkKeyboard(inline=True)
    i = 0
    for word in words:
        keyboard.add_button(word, color=vk_api.keyboard.VkKeyboardColor.PRIMARY)
        if i == 3:
            keyboard.add_line()
        i += 1
    return keyboard.get_keyboard()


def main():
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                request = event.text
                if request == "Старт":
                    for i in range(5):
                        cards_list = []
                        pseudo_user['id'] = i
                        while len(cards_list) != 5:
                            p = random.randint(1, 99)
                            if p not in all_cards_list:
                                cards_list.append(p)
                            cards_list = list(set(cards_list))
                        [all_cards_list.append(i) for i in cards_list]
                        for _ in range(5):
                            pseudo_user['cards'] += ['C:/repos git/vezdekod_bot_task/Имаджинариум/' +
                                                     str(cards_list[_]) + '.jpg']

                    user['user_id'] = event.user_id
                    cards_list = []
                    while len(cards_list) != 5:
                        p = random.randint(1, 98)
                        if p not in all_cards_list:
                            cards_list.append(p)
                        cards_list = list(set(cards_list))
                    for _ in range(5):
                        user['cards'] += ['C:/repos git/vezdekod_bot_task/Имаджинариум/' +
                                          str(cards_list[_]) + '.jpg']
                        user['words'] += [word[1].replace('\n', '') for word in random_img_words
                                          if word[0] == (str(cards_list[_]) + '.jpg')]

                    print(user['cards'])
                    user['words'] = random_words_for_each_img(user['words'])
                    print(user['words'])
                    #upload = vk_api.VkUpload(vk)
                    attachments = []
                    keyboard = create_keyboard([1, 2, 3, 4, 5])
                    for img in user['cards']:
                        upload_image = upload.photo_messages(photos=img)[0]
                        attachments.append('photo{}_{}'.format(upload_image['owner_id'], upload_image['id']))
                    print(attachments)
                    random_word = user['words'][random.randint(0, 5)]
                    write_msg(event.user_id, "Ваши карты, рандомное слово:" + random_word, attachments, keyboard)
                else:

                    if user['words'][int(event.text)] == random_word:
                        user['points'] += 3
                        write_msg_text(event.user_id, "Вы угадали слово, вам начислено 3 балла")
                    else:
                        write_msg_text(event.user_id, "Вы не угадали слово, вам начислено 0 баллов")


if __name__ == '__main__':
    main()
