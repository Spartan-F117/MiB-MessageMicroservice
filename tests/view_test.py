from re import M
import unittest
#from mib.db_model.message_db import Message
from flask.globals import session



class ViewTest(unittest.TestCase):
    """
    This class should be implemented by
    all classes that tests resources
    """
    message = None

    @classmethod

    def setUpClass(self):
        from mib import create_app
        app = create_app()
        self.message = app.test_client()

    def test_send_message(self):
    
        print('trying sending message....')

        payload = dict(sender_id='1', sender_nickname='nick1',receiver_id='2',receiver_nickname='nick2', body='test body', delivery_date='1111-01-01', image='')
        response = self.message.post("/send_message", json=payload)
        assert response.status_code == 202

    def test_draft_message(self):
    
        print('trying sending message....')

        payload = dict(sender_id='1', sender_nickname='nick1',receiver_id='2',receiver_nickname='nick2', body='test body', delivery_date='1111-01-01', image='')
        response = self.message.post("/draft_message", json=payload)
        assert response.status_code == 202

    def test_send_draft_message(self):
    
        print('trying sending message....')

        payload = dict(sender_id='1', sender_nickname='nick1',receiver_id='2',receiver_nickname='nick2', body='test body', delivery_date='1111-01-01', image='', draft_id='1')
        response = self.message.post("/send_draft_message", json=payload)
        assert response.status_code == 202

    def test_update_draft_message(self):
    
        print('trying sending message....')

        payload = dict(sender_id='1', sender_nickname='nick1',receiver_id='2',receiver_nickname='nick2', body='test body', delivery_date='1111-01-01', image='', draft_id='1')
        response = self.message.post("/update_draft_message", json=payload)
        assert response.status_code == 202

    # def test_delete_message(self):
    
    #     print('trying sending message....')

    #     response = self.message.get("/delete_message/1")
    #     assert response.status_code == 200

    def test_draft_message_info(self):
    
        print('trying sending message....')

        response = self.message.get("/draft_message_info/1")
        assert response.status_code == 200

    def test_delete_received_message(self):
    
        print('trying sending message....')
        response = self.message.get("/delete_received_message/2")
        assert response.status_code == 200
    
    def test_open_received_message(self):
    
        print('trying sending message....')
        #id=db.session.query(Message).first().message_id
        response = self.message.get("/open_received_message/1")
        assert response.status_code == 200

    def test_open_send_message(self):
    
        print('trying sending message....')
        #id=db.session.query(Message).first().message_id
        response = self.message.get("/open_send_message/1")
        assert response.status_code == 200

    def test_mailbox_without_filter(self):
    
        print('trying sending message....')

        payload = dict(id='1', filter='')
        response = self.message.post("/mailbox", json=payload)
        assert response.status_code == 202

    def test_mailbox_with_filter(self):
    
        print('trying sending message....')

        payload = dict(id='2', filter='hello')
        response = self.message.post("/mailbox", json=payload)
        assert response.status_code == 202

    def test_calendar_without_filter(self):
    
        print('trying sending message....')

        payload = dict(id='1', filter='')
        response = self.message.post("/calendar", json=payload)
        assert response.status_code == 202

    def test_calendar_with_filter(self):
    
        print('trying sending message....')

        payload = dict(id='1', filter='hello')
        response = self.message.post("/calendar", json=payload)
        assert response.status_code == 202