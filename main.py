import telebot
from groq import Groq


client = Groq(
    api_key="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")
bot = telebot.TeleBot("6625489610:AAErUXtLcFg3EbqfB3ImeNUk7LM0FQRt7Tk")
messages = []


@bot.message_handler(commands=['new'])
def handle_start(message):
    i = -1
    while True:
        try:
            i += 1
            bot.delete_message(message.chat.id, message.message_id-i)
        except:
            break
    bot.send_message(
        message.chat.id, 'Теперь вы можете начать новый диалог.')


@ bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global messages
    messages.append({"role": 'user', "content": message.text})
    if len(messages) > 6:
        messages = messages[-6:]
    response = client.chat.completions.create(
        model='llama3-70b-8192', messages=messages, temperature=0)
    bot.send_message(message.from_user.id, response.choices[0].message.content)
    messages.append(
        {"role": 'assistant', "content": response.choices[0].message.content})


while True:
    bot.polling(none_stop=True, interval=0, timeout=0)
