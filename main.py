import streamlit as st
import telebot
st.write("Hello World")
api="5985194933:AAG3TEbCAkslC1Vh8B8CmrnU00gtdEit5w8"
bot = telebot.TeleBot(api)

# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Hi there, I am EchoBot.
I am here to echo your kind words back to you. Just say anything nice and I'll say the exact same thing to you!\
""")
bot.infinity_polling()

