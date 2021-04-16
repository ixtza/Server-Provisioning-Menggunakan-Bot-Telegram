import requests
import os
import boturl
from bottle import (
    run, post, response, request as bottle_request
)

BOT_URL = boturl.BOT_URL

def get_chat_id(data):
    chat_id = data['message']['chat']['id']
    return chat_id

def get_message(data):  
    """
    Method to extract message id from telegram request.
    """
    message_text = data['message']['text']
    return message_text

def send_message(prepared_data):  
    """
    Prepared data should be json which includes at least `chat_id` and `text`
    """ 
    message_url = BOT_URL + 'sendMessage'
    requests.post(message_url, json=prepared_data)  # don't forget to make import requests lib

def prepare_data_for_answer(data):  
    answer = "done"

    json_data = {
        "chat_id": get_chat_id(data),
        "text": answer,
    }

    return json_data

@post('/')
def main():  
    data = bottle_request.json  # <--- extract all request data
    query = get_message(data)
    answer_data = prepare_data_for_answer(data)
    if query == "tes":
        send_message(answer_data)
    elif query == "nginx start":
        os.system("cd ~/ansible && ansible-playbook -i inventory.yml nginx_start.yml")
        send_message(answer_data)
    elif query == "nginx stop":
        os.system("cd ~/ansible && ansible-playbook -i inventory.yml nginx_stop.yml")
        send_message(answer_data)
    elif query == "mysql start":
        os.system("cd ~/ansible && ansible-playbook -i inventory.yml mysql_start.yml")
        send_message(answer_data)
    elif query == "mysql stop":
        os.system("cd ~/ansible && ansible-playbook -i inventory.yml mysql_stop.yml")
        send_message(answer_data)

    return response


if __name__ == '__main__':  
    run(host='localhost', port=8080, debug=True)
