import json
from mib.db_model.message_db import Message, db
from flask import jsonify, request
import datetime
from datetime import date
from werkzeug.security import check_password_hash, generate_password_hash


def check_none(**kwargs):
    for name, arg in zip(kwargs.keys(), kwargs.values()):
        if arg is None:
            raise ValueError('You can\'t set %s argument to None' % name)


def validate_date(date_text):
    try:
        print(date_text)
        if date_text != datetime.strptime(date_text, "%Y-%m-%d").strftime('%Y-%m-%d'):
            raise ValueError
        return True
    except ValueError:
        return False


def mailbox():
    post_data = request.get_json()
    id = post_data.get('id')
    _filter_word = post_data.get('filter')

    _sentMessages = db.session.query(Message).filter(Message.sender_id == id).filter(Message.is_draft == False)#.filter(Message.deleted==False)
    _recMessages = db.session.query(Message).filter(Message.receiver_id == id).filter(Message.is_draft == False).filter(Message.delivery_date <= date.today()).filter(Message.deleted == False)
    _draftMessage = db.session.query(Message).filter(Message.sender_id == id).filter(Message.is_draft == True)

    new_rec_list = []

    response = {
        'recived_message': '',
        'sent_message': '',
        'draft_message': ''
    }

    # remove the messages that don't respect the filter word list
    if _filter_word != "":
        print(_recMessages.all())
        for message in _recMessages.all():
            print(message)
            new_filter_word_list = _filter_word.first().list.split(',')
            control_flag = 0
            for elem in new_filter_word_list:
                if elem != "":
                    if elem in message[0].body:
                        control_flag = 1
            if control_flag == 0:
                new_rec_list.append(message)
            print(new_rec_list)
    else:
        pass







