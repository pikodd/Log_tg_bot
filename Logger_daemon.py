import daemon
import time
from subprocess import check_output
import telebot
from os import _exit

def main_program():
    while True:
        # your user id
        bot = telebot.TeleBot('1234')
        # your user id
        user_id = 12345678
        a = False

        @bot.message_handler(commands=['start'])
        def start_message(message):
            global a
            bot.send_message(message.chat.id, 'Regular notification activated')
            a = True
            while True:
                try:
                    bot.send_message(message.chat.id, 'Your access.log, master')
                    time.sleep(1)
                    bot.send_message(message.chat.id,
                                     check_output("cat /var/log/nginx/access.log| tail -n 20 ", shell=True))
                    if a:
                        time.sleep(3600)
                    else:
                        break
                except:
                    bot.send_message(message.chat.id, 'error')

        @bot.message_handler(content_types=['text'])
        def send_text(message):
            global a
            if message.text.lower() == 'access.log':
                try:
                    bot.send_message(message.chat.id,
                                     check_output("cat /var/log/nginx/access.log|tail -n 20", shell=True))
                except:
                    bot.send_message(message.chat.id, 'error')
            elif message.text.lower() == 'error.log':
                try:
                    bot.send_message(message.chat.id,
                                     check_output("cat /var/log/nginx/error.log|tail -n 20", shell=True))
                except:
                    bot.send_message(message.chat.id, 'error')
            elif message.text.lower() == 'stop bot':
                bot.send_message(message.chat.id, 'Bot is stopped')
                _exit(0)
            elif message.text.lower() == 'stop':
                a = False
                bot.send_message(message.chat.id, 'timer stopped')
                print(a)
            elif message.text.lower() == 'status':
                if a:
                    bot.send_message(message.chat.id, 'Regular notification is activated now')
                else:
                    bot.send_message(message.chat.id, 'Regular notification is deactivated now')

        if __name__ == '__main__':
            while True:
                try:
                    bot.polling(none_stop=True)
                except:
                    time.sleep(10)



with daemon.DaemonContext():
    main_program()
