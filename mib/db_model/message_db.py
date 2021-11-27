from werkzeug.security import generate_password_hash, check_password_hash
from mib import db

class Message(db.Model):
    __tablename__ = 'Message'

    # A list of fields to be serialized
    SERIALIZE_LIST = ['message_id',
                      'sender_id',
                      'receiver_id',
                      'delivery_date',
                      'creation_date',
                      'body',
                      'image',
                      'is_delivered',
                      'is_draft',
                      'opened',
                      'is_opened_notified',
                      'deleted',
                      'sender_nickname',
                      'receiver_nickname']

    message_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # primary key for the message, autoincremental
    sender_id = db.Column(db.Integer, nullable=False)  # user_id of the sender
    receiver_id = db.Column(db.Integer, nullable=False)  # user_id of the reciver
    delivery_date = db.Column(db.Date)  # scheduled date for sending message
    creation_date = db.Column(db.Date)  # Creation date for the message
    body = db.Column(db.Unicode(128), nullable=True)  # body of the message
    image = db.Column(db.Unicode(1000000), nullable=True)  # The image unicode (saving image in the db)
    is_delivered = db.Column(db.Boolean, nullable=False, default=False)  # True when a notification is send to the recipient
    is_draft = db.Column(db.Boolean, nullable=True)  # True when a message is not send, but saved as draft
    opened = db.Column(db.Boolean, nullable=True)  # True when the message is opened by the recipient
    is_opened_notified = db.Column(db.Boolean, nullable=True, default=False)  # True when the notification is send for an opened message
    deleted = db.Column(db.Boolean, nullable=True)  # True when a message is delete
    sender_nickname = db.Column(db.Unicode(128), nullable=True)
    receiver_nickname = db.Column(db.Unicode(128), nullable=True)

    def __init__(self, *args, **kw):
        super(Message, self).__init__(*args, **kw)

    def serialize(self):
        return dict([(k, self.__getattribute__(k)) for k in self.SERIALIZE_LIST])
