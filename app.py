import argparse
import json
import os
import smtplib
import ssl
import urllib.error
import urllib.request
from email.message import EmailMessage
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

WORD_DEFINITIONS = {
    "abandon": "to leave something behind or stop supporting completely",
    "ability": "the skill or power to do something",
    "adventure": "an exciting or unusual experience",
    "balance": "a steady position without falling",
    "capture": "to catch or take control of something",
    "change": "to make something different",
    "clarity": "the quality of being clear and easy to understand",
    "comfort": "a state of physical ease and relaxation",
    "culture": "the ideas and customs of a group of people",
    "decide": "to choose one option after thinking about it",
    "delight": "a feeling of great pleasure or happiness",
    "discover": "to find or learn something for the first time",
    "effort": "physical or mental energy used to do something",
    "enable": "to make something possible or easier",
    "energy": "the ability to do work or cause change",
    "engine": "a machine that converts energy into motion",
    "example": "something that shows what is typical or possible",
    "experience": "knowledge gained from doing things",
    "global": "relating to the whole world",
    "growth": "the process of increasing in size or ability",
    "happy": "feeling or showing joy and pleasure",
    "honest": "telling the truth and acting sincerely",
    "imagine": "to form a picture or idea in your mind",
    "journey": "a trip from one place to another",
    "justice": "fair treatment according to the law",
    "knowledge": "facts and information learned through study",
    "language": "a system of words used to communicate",
    "learn": "to gain knowledge or skill from experience",
    "legacy": "something handed down from the past",
    "limit": "the greatest amount or degree allowed",
    "local": "related to a nearby place",
    "memory": "the ability to remember information",
    "mentor": "a trusted guide or adviser",
    "method": "a way of doing something",
    "moment": "a very short period of time",
    "nature": "the physical world, including plants and animals",
    "notice": "to become aware of something",
    "object": "a thing that can be seen or touched",
    "opinion": "a personal belief or judgment",
    "peace": "a state without war or trouble",
    "people": "human beings in general",
    "planet": "a large body that moves around a star",
    "positive": "thinking in a hopeful and confident way",
    "practice": "to do something repeatedly to improve",
    "question": "a sentence used to ask for information",
    "reason": "a cause or explanation for something",
    "refresh": "to make something feel new or energetic",
    "respect": "a feeling of admiration for someone",
    "result": "what happens because of an action",
    "review": "to look at something again carefully",
    "reward": "something given for good work or behavior",
    "science": "the study of the natural world",
    "service": "help or work done for others",
    "simple": "easy to understand or do",
    "skill": "a learned ability to do something well",
    "smile": "a happy expression made with the mouth",
    "strength": "the power to do something physical or mental",
    "success": "the achievement of a goal",
    "talent": "a natural ability to do something well",
    "thanks": "a polite expression of gratitude",
    "think": "to use your mind to form ideas",
    "travel": "to go from one place to another",
    "unique": "being the only one of its kind",
    "value": "the importance or worth of something",
    "vision": "a clear idea of what something should be",
    "voice": "the sound made when speaking or singing",
    "wonder": "a feeling of surprise and admiration",
    "world": "the planet and all the people on it",
    "worthy": "deserving respect or attention",
    "yellow": "the color between green and orange",
    "youth": "the time of being young",
    "zeal": "great energy or enthusiasm for a goal",
    "zone": "an area with a particular characteristic"
}

WORD_LIST = list(WORD_DEFINITIONS.keys())
DAILY_WORD_COUNT = 5


def load_dotenv_file(filename='.env'):
    if not os.path.exists(filename):
        return

    with open(filename, 'r', encoding='utf-8') as env_file:
        for line in env_file:
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue

            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value


load_dotenv_file()

SMTP_SERVER = os.environ.get('SMTP_SERVER')
SMTP_PORT = int(os.environ.get('SMTP_PORT', '587'))
SMTP_USERNAME = os.environ.get('SMTP_USERNAME')
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD')
SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
SENDGRID_SENDER = os.environ.get('SENDGRID_SENDER') or os.environ.get('EMAIL_SENDER') or SMTP_USERNAME
EMAIL_SENDER = os.environ.get('EMAIL_SENDER') or SMTP_USERNAME

def is_sendgrid_configured():
    return bool(SENDGRID_API_KEY and SENDGRID_SENDER)


def is_smtp_configured():
    return bool(SMTP_SERVER and SMTP_USERNAME and SMTP_PASSWORD and EMAIL_SENDER)


@app.route('/')
def index():
    return render_template(
        'index.html',
        word_list=WORD_LIST,
        word_definitions=WORD_DEFINITIONS,
        daily_word_count=DAILY_WORD_COUNT,
        smtp_configured=is_smtp_configured(),
        sendgrid_configured=is_sendgrid_configured(),
        smtp_server=SMTP_SERVER,
        smtp_username=SMTP_USERNAME,
        sendgrid_sender=SENDGRID_SENDER,
    )

def build_email_body(words):
    parts = ['<h2>Daily English Word Reminder</h2>', '<p>Here are your 5 words for today:</p>', '<ul>']
    plain_lines = ['Daily English Word Reminder', '', 'Here are your 5 words for today:', '']
    for word in words:
        definition = WORD_DEFINITIONS.get(word, 'No definition available.')
        plain_lines.append(f'{word}: {definition}')
        parts.append(f'<li><strong>{word}</strong>: {definition}</li>')
    parts.append('</ul>')
    parts.append('<p>Keep practicing and review them again later today.</p>')
    plain_lines.append('')
    plain_lines.append('Keep practicing and review them again later today.')
    return '\n'.join(plain_lines), '\n'.join(parts)


def send_smtp_message(recipients, subject, words):
    if not is_smtp_configured():
        raise ValueError('SMTP configuration is incomplete. Set SMTP_SERVER, SMTP_USERNAME, SMTP_PASSWORD, and EMAIL_SENDER.')

    plain_text, html_text = build_email_body(words)
    message = EmailMessage()
    message['Subject'] = subject
    message['From'] = EMAIL_SENDER
    message['To'] = ', '.join(recipients)
    message.set_content(plain_text)
    message.add_alternative(html_text, subtype='html')

    context = ssl.create_default_context()
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=20) as server:
        server.starttls(context=context)
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.send_message(message)


def send_sendgrid_message(recipients, subject, words):
    if not is_sendgrid_configured():
        raise ValueError('SendGrid is not configured. Set SENDGRID_API_KEY and SENDGRID_SENDER.')

    plain_text, html_text = build_email_body(words)
    payload = {
        'personalizations': [
            {
                'to': [{'email': recipient} for recipient in recipients],
                'subject': subject,
            }
        ],
        'from': {'email': SENDGRID_SENDER},
        'content': [
            {'type': 'text/plain', 'value': plain_text},
            {'type': 'text/html', 'value': html_text},
        ],
    }
    request_data = json.dumps(payload).encode('utf-8')
    request_headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {SENDGRID_API_KEY}',
    }
    request = urllib.request.Request(
        'https://api.sendgrid.com/v3/mail/send',
        data=request_data,
        headers=request_headers,
        method='POST',
    )

    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            if response.status not in (200, 202):
                raise RuntimeError(f'SendGrid returned status {response.status}')
    except urllib.error.HTTPError as error:
        body = error.read().decode('utf-8', errors='ignore')
        raise RuntimeError(f'SendGrid error: {error.code} {error.reason} - {body}') from error


def send_email_message(recipients, subject, words):
    if is_sendgrid_configured():
        return send_sendgrid_message(recipients, subject, words)
    return send_smtp_message(recipients, subject, words)


@app.route('/send-email', methods=['POST'])
def send_email_route():
    payload = request.get_json(silent=True) or {}
    recipients_raw = payload.get('recipients', '')
    recipients = [address.strip() for address in recipients_raw.replace(';', ',').split(',') if address.strip()]

    if not recipients:
        return jsonify(success=False, error='Enter at least one email address.'), 400

    words = payload.get('words') or []
    if not isinstance(words, list) or len(words) == 0:
        return jsonify(success=False, error='No words available to send.'), 400

    subject = payload.get('subject', 'Daily English Word Reminder')

    try:
        send_email_message(recipients, subject, words)
        return jsonify(success=True, message='Email reminder sent successfully.')
    except Exception as exc:
        return jsonify(success=False, error=str(exc)), 500

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run the English word reminder app.')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind the server to')
    parser.add_argument('--port', type=int, default=int(os.environ.get('PORT', 5000)), help='Port to bind the server to')
    args = parser.parse_args()
    app.run(debug=True, host=args.host, port=args.port)
