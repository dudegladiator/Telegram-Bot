import streamlit as st
import gradio as gr
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
st.write("Hello World")
st.write("Project in Progress")
def greet(name):
  return "hello " + name 
demo = gr.interface(fn=greet,input="text",outputs="text")
demo.launch()
token=st.secrets["token"]
bot = telebot.TeleBot(token)


#Remove Bg
def RemoveBg(imagepath,id,format):
  from PIL import Image
  from rembg import remove
  img=Image.open(imagepath)
  output=remove(img)
  try:
      output.save("RemoveBg"+id+"."+format)
  except OSError:
    output=output.convert("RGB")
    output.save("RemoveBg"+id+"."+format)
  return "RemoveBg"+id+"."+format

#Resize Image
#imagepath can be relative
#format it must be jpg
#width and heigth must be integer
# id must be string format of integer
def resize_img(imagepath,width,heigth,id,format):
  from PIL import Image
  
  with Image.open(imagepath) as im:
    if(width>=im.width or heigth>=im.height):
      return False
    img=im.resize((width,heigth))
    try:
      img.save("ResizeImage"+id+"."+format)
    except OSError:
      img=img.convert("RGB")
      img.save("ResizeImage"+id+"."+format) 
  return "ResizeImage"+id+"."+format    

#Compress image
#quality must be in between 1 to 100 with integer
#imagepath can be relative
#for compressing image it must be jpg
# id must be string format of integer

def compress_img(imagepath,id,format,quality):
  from PIL import Image
  img=Image.open(imagepath)
  try:
    img.save("CompressImage"+id+"."+format,quality=quality,optimised=True)
  except OSError:
    img=img.convert("RGB")
    img.save("CompressImage"+id+"."+format,quality=quality,optimised=True)

  return "CompressImage"+id+"."+format  


from telebot.types import ReplyKeyboardMarkup, KeyboardButton
@bot.message_handler(commands=['start'])
def First_time(message):
  chat_id=message.chat.id
  bot.send_message(chat_id,"Welcome to Image Manipulation Bot")
  bot.send_message(chat_id,"To use this bot\n \n1->Send Photo\n2->Choose option")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    # Get the file_id of the photo
    chat_id=message.chat.id
    file_id = message.photo[-1].file_id
    # Download the photo using the file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    # Save the photo to disk
    with open('ImgRec'+str(chat_id)+'.png', 'wb') as new_file:
        new_file.write(downloaded_file)

    # Reply to the user
    bot.reply_to(message, 'Photo received!')
    print(chat_id)
    markup = ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
    markup.add(KeyboardButton("Compress Image"))
    markup.add(KeyboardButton("Resize Image"))
    markup.add(KeyboardButton("Remove Background"))
    
    bot.send_message(chat_id,"Choose the Option",reply_markup=markup)

@bot.message_handler(func= lambda m: True)
def message_handler(message):
  chat_id=message.chat.id
  if(message.text=="Compress Image"):
    bot.reply_to(message,"Send the quality of picture(Integer(1-100)) \n 'Quality 20'")
  elif("Quality" in message.text):
    quality=int(message.text.split()[-1])
    if(quality<1 or quality>99):
      bot.reply_to(message,"Send the quality of picture in range of 1 - 100 \n 'Quality=20'")
      return
    compress_file=open(compress_img('ImgRec'+str(chat_id)+'.png',str(chat_id),"jpg",quality),'rb')
    bot.send_photo(chat_id,compress_file)
  elif(message.text=="Resize Image"):
    bot.reply_to(message,"Send the New size of picture(width,heigth) \n 'Size 100 300'")
  elif ("Size"in message.text):
    width,heigth=int(message.text.split()[-1]) , int(message.text.split()[-2])
    k=resize_img('ImgRec'+str(chat_id)+'.png',width,heigth,str(chat_id),"jpg")
    if k:
      resize_file=open(k,"rb")
      bot.send_photo(chat_id,resize_file)
    return
  elif (message.text=="Remove Background"):
    store=bot.send_message(chat_id,"Removing Background\nPlease wait..")
    RemBG_file=open(RemoveBg('ImgRec'+str(chat_id)+'.png',str(chat_id),"jpg"),"rb")
    bot.delete_message(chat_id,store.message_id)
    bot.send_photo(chat_id,RemBG_file)

bot.polling()    
