import json
from os import memfd_create
from mib.db_model.message_db import Message, db
from flask import jsonify, request
import datetime
from datetime import date
from werkzeug.security import check_password_hash, generate_password_hash
import base64


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

    listobj_sentMessages = []

    for item in _sentMessages:
        listobj_sentMessages.append(item.serialize())

    listobj_draftMessages = []

    for item in _draftMessage:
        listobj_draftMessages.append(item.serialize())


    response_code = 201

    # remove the messages that don't respect the filter word list
    if _filter_word != "":
        print(_filter_word)
        for message in _recMessages.all():
            print(message)
            new_filter_word_list = _filter_word.split(',')
            control_flag = 0
            for elem in new_filter_word_list:
                if elem != "":
                    if elem in message.body:
                        control_flag = 1
            if control_flag == 0:
                new_rec_list.append(message.serialize())
            print(new_rec_list)
        response = {
            'received_message': new_rec_list,
            'sent_message': listobj_sentMessages,
            'draft_message': listobj_draftMessages
        }
    else:
        listobj = []

        for item in _recMessages:
            listobj.append(item.serialize())
        
        response = {
            'received_message': listobj,
            'sent_message': listobj_sentMessages,
            'draft_message': listobj_draftMessages
        }
    response_code=202
    return jsonify(response), response_code
    

def delete_message(draft_id):
    db.session.query(Message).filter(Message.message_id==draft_id).delete()    
    db.session.commit()
    response_code = 200
    return response_code


def draft_message_info(draft_id):
    result = db.session.query(Message).filter(Message.message_id==draft_id).first()   
    response = {
        'draft_message': ''
    }
    response['draft_message']=result.serialize()
    return response,200

def send_message():
    response = {
        'message': 'message not sent'
    }

    post_data = request.get_json()
    sender_id = post_data.get('sender_id')
    sender_nickname = post_data.get('sender_nickname')
    receiver_id = post_data.get('receiver_id')
    receiver_nickname = post_data.get('receiver_nickname')
    body = post_data.get('body')
    delivery_date = post_data.get('delivery_date')
    image = post_data.get('image')[2:-1]
    
    new_message = Message()
    new_message.sender_id = sender_id
    new_message.sender_nickname = sender_nickname
    new_message.receiver_id = receiver_id
    new_message.receiver_nickname = receiver_nickname
    new_message.body = body
    new_message.delivery_date = datetime.datetime.fromisoformat(delivery_date)
    new_message.image = image
    new_message.is_draft = False
    new_message.deleted = False

    db.session.add(new_message)
    db.session.commit()
    response["message"] = "message sent"
    return jsonify(response), 202

def draft_message():
    response = {
        'message': 'message not drafted'
    }

    post_data = request.get_json()
    sender_id = post_data.get('sender_id')
    sender_nickname = post_data.get('sender_nickname')
    receiver_id = post_data.get('receiver_id')
    receiver_nickname = post_data.get('receiver_nickname')
    body = post_data.get('body')
    delivery_date = post_data.get('delivery_date')
    image = post_data.get('image')[2:-1]
    
    new_message = Message()
    new_message.sender_id = sender_id
    new_message.sender_nickname = sender_nickname
    new_message.receiver_id = receiver_id
    new_message.receiver_nickname = receiver_nickname
    new_message.body = body
    new_message.delivery_date = datetime.datetime.fromisoformat(delivery_date)
    new_message.image = image
    new_message.is_draft = True
    new_message.deleted = False

    db.session.add(new_message)
    db.session.commit()
    response["message"] = "message drafted"
    return jsonify(response), 202

def send_draft_message():
    response = {
        'message': 'message not sent'
    }

    post_data = request.get_json()
    sender_id = post_data.get('sender_id')
    sender_nickname = post_data.get('sender_nickname')
    receiver_id = post_data.get('receiver_id')
    receiver_nickname = post_data.get('receiver_nickname')
    body = post_data.get('body')
    delivery_date = post_data.get('delivery_date')
    image = post_data.get('image')[2:-1]
    draft_id = post_data.get('draft_id')
    
    new_message = db.session.query(Message).filter(Message.message_id==draft_id).first()
    new_message.sender_id = sender_id
    new_message.sender_nickname = sender_nickname
    new_message.receiver_id = receiver_id
    new_message.receiver_nickname = receiver_nickname
    new_message.body = body
    new_message.delivery_date = datetime.datetime.fromisoformat(delivery_date)
    new_message.image = image
    new_message.is_draft = False
    new_message.deleted = False

    db.session.commit()
    response["message"] = "draft message sent"
    return jsonify(response), 202

def update_draft_message():
    response = {
        'message': 'message not sent'
    }

    post_data = request.get_json()
    sender_id = post_data.get('sender_id')
    sender_nickname = post_data.get('sender_nickname')
    receiver_id = post_data.get('receiver_id')
    receiver_nickname = post_data.get('receiver_nickname')
    body = post_data.get('body')
    delivery_date = post_data.get('delivery_date')
    image = post_data.get('image')[2:-1]
    draft_id = post_data.get('draft_id')
    
    new_message = db.session.query(Message).filter(Message.message_id==draft_id).first()
    new_message.sender_id = sender_id
    new_message.sender_nickname = sender_nickname
    new_message.receiver_id = receiver_id
    new_message.receiver_nickname = receiver_nickname
    new_message.body = body
    new_message.delivery_date = datetime.datetime.fromisoformat(delivery_date)
    new_message.image = image

    db.session.commit()
    response["message"] = "draft message update"
    return jsonify(response), 202

def delete_received_message(id):
    message = db.session.query(Message).filter(Message.message_id==id).first()   
    message.deleted = True
    db.session.commit()
    response_code = 200
    return response_code

def open_received_message(id):
    message_new = db.session.query(Message).filter(Message.message_id==id).first()
    message_new.opened = True
    db.session.commit()

    message = db.session.query(Message).filter(Message.message_id==id)

    listobj = []
    for item in message:
        listobj.append(item.serialize())

    response = {
            'received_message': listobj
        }

    print(response)

    return jsonify(response)

def open_send_message(id):
    message = db.session.query(Message).filter(Message.message_id==id) 
    message.opened = True
    db.session.commit()

    listobj = []
    for item in message:
        listobj.append(item.serialize())

    response = {
            'send_message': listobj
        }

    print(response)

    return jsonify(response)

