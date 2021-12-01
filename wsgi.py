"""
Message in a Bottle
Web Server Gateway Interface

This file is the entry point for
mib-users-ms microservice.
"""
from mib import create_app, create_celery
from celery import Celery
from celery.schedules import crontab
from flask_mail import Mail
from flask_mail import Message as MessageFlask
import datetime
from flask import abort
import os, requests

# application instance
app = create_app()
celery_app = create_celery()
mail = Mail(app)

from mib.db_model.message_db import db, Message

# Celery Tasks
@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    '''
        Set the time for Celery tasks:
         - every 1 minute execute the task "checkNewMessage"
         - every 1 minute execute the task "checkMessageOpened"
         - every month at day 1 and time 11:00 execute the task "lottery"
    '''
    # NOTIFY FOR A MESSAGE RECEIVED: Executes every minute
    sender.add_periodic_task(60.0, checkNewMessage.s(), name='check for new message received...')

    # NOTIFY FOR A MESSAGE OPENED: Executes every minute
    sender.add_periodic_task(60.0, checkMessageOpened.s(), name='check for message opened...')


def send_mail(email, body):
    '''
        This function will send mail at users provided in "email" field.
        In case the body is none the function will be called from "checkNewMessage" task,
        otherwise will be called from "checkMessageOpened" task.
    '''

    print("sending_mail...")

    # Case "new message received"
    if body is None:
        msg = MessageFlask("You have recived a new message!", sender="provaase5@gmail.com", recipients=[email])
        msg.body = """new message in the "fantastic" social media Message In a Bottle!"""

    # Case "message opened"
    elif body is not None:
        msg = MessageFlask("Your message has been read!", sender="provaase5@gmail.com", recipients=[email])
        msg.html = """<p>Your message has been read.</p>
                    <p>Message read:</br>{}</p>""".format(body)

    if mail.send(msg):
        return False
    else:
        return True


def get_email_by_id(receiver_id):
    REQUESTS_TIMEOUT_SECONDS = 60.0
    USERS_ENDPOINT = app.config['USERS_MS_URL']
    email = ""
    user_id = str(receiver_id)

    try:
        response = requests.get(USERS_ENDPOINT+'/user/'+user_id,
                                timeout=REQUESTS_TIMEOUT_SECONDS)
        json_payload = response.json()
        if response.status_code == 200:
            # user is authenticated
            email = json_payload["email"]
        else:
            raise RuntimeError('Server has sent an unrecognized status code %s' % response.status_code)
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        return abort(500)
    return email


@celery_app.task
def checkNewMessage():
    '''
        This method will notify the user when recive a new message.
        This method also send the message to users.
    '''

    # Take current time
    now = datetime.datetime.now()
    print("orario esecuzione task:" +str(now))
    # Retrive all the message delivered and not notified
    to_notify = db.session.query(Message).filter(Message.is_delivered == False).filter(Message.delivery_date <= now)
    print(to_notify.all())
    # For-each message, flag it as notified and send an email to the user
    for item in to_notify.all():
        mail_user = get_email_by_id(item.receiver_id)
        item.is_delivered = True
        db.session.commit()
        send_mail(mail_user, None)


@celery_app.task
def checkMessageOpened():
    '''
        This method will send a notification when a send message has been opened
    '''

    # Retrive all the message opened and not notified
    to_notify = db.session.query(Message).filter(Message.opened == True).filter(Message.is_opened_notified == False)

    # For-each message, flag it as notified and send an email to the user
    for item in to_notify.all():
        mail_user = get_email_by_id(item.receiver_id)
        item.is_opened_notified = True
        db.session.commit()
        send_mail(mail_user, item.body)

    return True


if __name__ == '__main__':
    app.run()
