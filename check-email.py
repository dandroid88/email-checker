#!/usr/bin/env python
import os
import hashlib
import redis
import pynotify
from selenium import webdriver

USERNAME = ''
PASSWORD = ''
EMAIL_URL = ''
REDIS_KEY = 'email:last_check_hash'
PHANTOMJS_BIN = '/home/dan/phantomjs/phantomjs'

class UnreadEmail():
    def __init__(self, sender, subject):
        self.sender = sender
        self.subject = subject

    def __repr__(self):
        return self.sender + ': ' + self.subject

    def __str__(self):
        return self.sender + ': ' + self.subject

def check_email(username, password):
    driver = _get_driver()
    _login(driver, username, password)
    _notify(_get_unread_message_count(driver), _get_unread_messages(driver))
    driver.quit()

def _get_driver():
    return webdriver.PhantomJS(PHANTOMJS_BIN)

def _login(driver, username, password):
    driver.get(EMAIL_URL)
    driver.find_element_by_id('username').send_keys(username)
    driver.find_element_by_id('password').send_keys(password)
    driver.find_element_by_css_selector('input.btn').click()

def _get_unread_messages(driver):
    unread_emails = []
    for el in driver.find_elements_by_css_selector('div.cntnt tbody tr'):
        if 'font-weight: bold;' in el.get_attribute('style'):
            unread_emails.append(
                UnreadEmail(
                    el.find_elements_by_tag_name('td')[4].text,
                    el.find_elements_by_tag_name('td')[5].text
                )
            )
    return unread_emails

def _get_unread_message_count(driver):
    return driver.find_element_by_css_selector('span.unrd') .text.replace('(', '').replace(')', '')

def _notify(unread_email_count, unread_emails):
    pynotify.init("Unread Emails")
    title = unread_email_count + ' Unread Messages'
    message = ''.join([str(email) + '\n' for email in unread_emails]) + '...'
    if _should_notify(title, message, unread_email_count):
        notification = pynotify.Notification(title, message)
        notification.set_timeout(4)
        notification.show()
        _save_hash(title, message)

def _save_hash(title, message):
    redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
    redis_client.set(REDIS_KEY, _create_hash(title, message))

def _get_hash():
    redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
    return redis_client.get(REDIS_KEY)

def _create_hash(title, message):
    h = hashlib.md5()
    h.update(title)
    h.update(message)
    return h.digest()

def _should_notify(title, message, unread_email_count):
    return (_create_hash(title, message) != _get_hash()) and int(unread_email_count) and message != '...'

if __name__ == "__main__":
    check_email(USERNAME, PASSWORD)
