import os
import json
import time


def process_bytes(new_bytes: bytes):
    file_title = f'{str(time.time() * 1000).split(".")[0]}.jpg'

    dir_path = os.path.join(os.getcwd(), 'recorded_data')
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    with open(os.path.join(dir_path, file_title), 'wb') as f:
        f.write(new_bytes)


def process_text(text_data: str):
    text_data_json = json.loads(text_data)
    message = text_data_json['message']

    return {
        'type': 'send_message',
        'message': message
    }
