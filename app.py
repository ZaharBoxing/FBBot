import os, sys
from flask import Flask, request
from utils import wit_response
from pymessenger import Bot
from pymessenger import Button

app = Flask(__name__)

PAGE_ACCESS_TOKEN = "YOUR_PAGE_ACCESS_TOKEN"

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

					response = None

					entity, value = wit_response(messaging_text)
					if entity == 'wit_greetings':
						response = "Hi, how are u?"
					elif entity == 'wit_mood':
						response = "I am too, do u want some info about company?"
					elif entity == 'wit_confirmation':
						response = bot.send_button_message(sender_id, text, buttons)
					elif entity == 'wit_negation':
						response = "Okey, see u next time. Good bye!"

					if response == None:
						response = "Sry, but i dont understand"

					bot.send_text_message(sender_id, response)

	return "ok", 200

def log(message):
	print(message)
	sys.stdout.flush()


buttons = []
button = Button(title='Site', type='web_url', url='your site')
buttons.append(button)
text = "Click here"


if __name__ == "__main__":
	app.run(debug = True, port = 80)