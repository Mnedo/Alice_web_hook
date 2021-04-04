from flask import Flask, request
import logging
import os
# библиотека, которая нам понадобится для работы с JSON
import json

app = Flask(__name__)

# Устанавливаем уровень логирования
logging.basicConfig(level=logging.INFO)

sessionStorage = {}
data = {'is_bought': False}


@app.route('/post', methods=['POST'])
def main():
    global data

    logging.info(f'Request: {request.json!r}')

    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }

    handle_dialog(request.json, response)

    logging.info(f'Response:  {response!r}')
    logging.info(f'DATA:  {data!r}')

    return json.dumps(response)


def handle_dialog(req, res):
    global data

    user_id = req['session']['user_id']

    if req['session']['new']:
        sessionStorage[user_id] = {
            'suggests': [
                "Не хочу.",
                "Не буду.",
                "Отстань!",
            ]
        }
        data = {'is_bought': False}
        res['response']['text'] = 'Купи слона'
        res['response']['buttons'] = get_suggests(user_id)
        return

    if req['request']['original_utterance'].lower() in [
        'ладно',
        'куплю',
        'покупаю',
        'хорошо'
    ]:
        if not data['is_bought']:
            # Пользователь согласился, прощаемся.
            res['response']['text'] = 'Слона можно найти на Яндекс.Маркете!'
        else:
            res['response']['text'] = 'Кролика можно найти на Яндекс.Маркете!'
            res['response']['end_session'] = True
        return

    # Если нет, то убеждаем его купить слона!
    if not data['is_bought']:
        res['response']['text'] = \
            f"Все говорят '{req['request']['original_utterance']}', а ты купи слона!"
    else:
        res['response']['text'] = \
            f"Все говорят '{req['request']['original_utterance']}', а ты купи кролика!"
    res['response']['buttons'] = get_suggests(user_id)


# Функция возвращает две подсказки для ответа.
def get_suggests(user_id):
    global data

    session = sessionStorage[user_id]

    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests'][:2]
    ]

    session['suggests'] = session['suggests'][1:]
    sessionStorage[user_id] = session

    if len(suggests) < 2:
        if not data['is_bought']:
            suggests.append({
                "title": "Ладно",
                "url": "https://market.yandex.ru/search?text=слон",
                "hide": True
            })
        else:
            suggests.append({
                "title": "Ладно",
                "url": "https://market.yandex.ru/search?text=кролик",
                "hide": True
            })

    return suggests


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
