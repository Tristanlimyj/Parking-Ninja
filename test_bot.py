import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config
from bot.Modules import TeleFunc, StaticActions

class TestTeleFunc():
    # Need to come up with a test for this
    def test_send_message(self):
        print('Need to create test for send message')
    def test_create_params(self):
        url, params = TeleFunc.create_params('/sendMessage', 123, 'How are you doing?')

        assert '/sendMessage' in url
        assert params['chat_id'] == 123
        assert params['text'] == 'How are you doing?'
    
    # Basic means all strings in the list
    def test_basic_create_reply_keyboard(self):
        keyboard = TeleFunc.create_reply_keyboard([
                'Test',
                'Test',
                'Test'
            ])

        assert ['Test'] in keyboard['keyboard']
    
    # Nested means list and str in the list
    def test_nested_create_reply_keyboard(self):
        keyboard = TeleFunc.create_reply_keyboard([
                'Test',
                [
                    'Test',
                    'Test'
                ]
            ])

        assert ['Test', 'Test'] in keyboard['keyboard']

    def test_if_list_create_send_location_btn(self):
        location_btn = TeleFunc.create_send_location_btn()
        assert type(location_btn)
    
    def test_output_create_send_location_btn(self):
        location_btn = TeleFunc.create_send_location_btn()
        desired_output = {
            'text' :  'Send Location📍',
            'request_location': True
        }

        assert location_btn[0] == desired_output

class TestStatic:
    def test_start(self):
        text = StaticActions.start()
        assert type(text) == str
        
    def test_description(self):
        text = StaticActions.description()
        assert type(text) == str

    def test_settings(self):
        text = StaticActions.settings()
        assert type(text) == str

    def test_error(self):
        text = StaticActions.error()
        assert type(text) == str
