import os, sys
from flask import Flask, request
from pymessenger import Bot

app = Flask(__name__)

PAGE_ACCESS_TOKEN = "EAAdceYcByOEBAKlRwgRmtrDwNkwOjNxr7Em8TvwOXZBdTNeQZBW7IK9JdwDrYu6sK2cexKZC8aC5NUXgqo6md6BzTC1BAtVZAxNXq4zrAIGuB2GB6AZCOswKbBmlW4vpw9JZAmB279miujxRA9uqKw2qHmAmsdmUnbgZADZBBOpiW6ChAdZBJo4nB"

bot = Bot(PAGE_ACCESS_TOKEN)

@app.route("/", methods=['GET'])
def verify():
	if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
		if not request.args.get("hub.verify_token") == "hello":
			return "Verification token mismatch", 403
		return request.args["hub.challenge"], 200
	return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():
	data = request.get_json()
	log(data)

	if data['object'] == 'page':
		for entry in data['entry']:
			for messaging_event in entry['messaging']:


				sender_id = messaging_event['sender']['id']
				recipient_id = messaging_event['recipient']['id']

				if messaging_event.get('message'):
					if 'text' in messaging_event['message']:
						messaging_text = messaging_event['message']['text']
					else:
						messaging_text = 'no text'
						bot.send_text_message(sender_id, "Nice pic")
						

					if messaging_text == "Hi":
						response = get_message()
						bot.send_text_message(sender_id, response)
					elif messaging_text == "Fine":
						response = Hau()
						bot.send_text_message(sender_id, response)
					elif messaging_text == "Yes":
						response = Info()
						goodbye = Bye()
						bot.send_text_message(sender_id, response)
						bot.send_text_message(sender_id, goodbye)
					elif messaging_text == "No":
						response = No()
						bot.send_text_message(sender_id, response)
					elif messaging_text == "Send me link":
						response = result
						bot.send_generic_message(sender_id, response)
					else:
						response = Dont()
						bot.send_text_message(sender_id, response)

	return "ok", 200

class Buttons(object):
    def __init__(self, text, buttons):
        self.type = 'template'
        self.payload = {
            'template_type': 'button',
            'text': text,
            'buttons': Buttons.convert_shortcut_buttons(buttons)
        }

    @staticmethod

    def convert_shortcut_buttons(items):
        if items is not None and isinstance(items, list):
            result = []
            for item in items:
                if isinstance(item, BaseButton):
                    result.append(item)
                elif isinstance(item, dict):
                    if item.get('type') in ['web_url', 'postback', 'phone_number', 'element_share']:
                        type = item.get('type')
                        title = item.get('title')
                        value = item.get('value', item.get('url', item.get('payload')))
                        type == 'web_url':
                        result.append(ButtonWeb(title=title, url=value)
                    else:
                        raise ValueError('Invalid button type')
                else:
                    raise ValueError('Invalid buttons variables')
            return result
        else:
            return items

class BaseButton(object):
    pass

class ButtonWeb(BaseButton):
    def __init__(self, title, url):
        self.type = 'web_url'
        self.title = "Site"
        self.url = "isport.ua"

def Bye():
	return "Thx for ur visit, goodbye"

def No():
	return "Ok,see u soon"

def Info():
	return "Site: isport.ua, Email: supra11@ukr.net, Contact number: 095-838-16-26"

def Hau():
	return "Too,u need some information about company?"

def get_message():
	return "Hello,how are u?"

def Dont():
	return "Dont understand"

def log(message):
	print(message)
	sys.stdout.flush()

if __name__ == "__main__":
	app.run(debug = True, port = 80)