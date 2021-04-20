# импортируем библиотеки
from flask import Flask, request
import logging
from deep_translator import MyMemoryTranslator
import json
import os

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

sessionStorage = {}


@app.route('/post', methods=['POST'])
def main():
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

    return json.dumps(response)


def handle_dialog(req, res):
    user_id = req['session']['user_id']

    if req['session']['new']:
        res['response']['text'] = 'Привет! Что хочещб перевести?'
        return
    else:
        phrase = req['request']['nlu']['tokens'][2:]
        translated = MyMemoryTranslator(source="ru", target="en").translate(text=phrase)
        res['response']['text'] = translated


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
