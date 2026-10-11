import logging
from telegram import Update
from telegram.ext import ApplicationBuilder , ContextTypes , CommandHandler , MessageHandler , filters , ConversationHandler
from telegram.ext import Application
from telegram.request import HTTPXRequest
import time
import requests as req
import random as rand
from openai import OpenAI
from getpass import getpass
from sentence_transformers import SentenceTransformer
import chromadb

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

Text = 1
model = SentenceTransformer('all-MiniLM-L6-v2')
text_2 = [
    'برای رفتن به بخش ثبت نام کاربران بزرگ سال باید در بخش خدمات و در بخش ثبت نام بزرگسالان مراجعه کنید',
    'برای ثبت نام کاربران خوردسال باید در بخش خدمات و در بخش ثبت نام خوردسالان مراجعه کنید',
    'برای ثبت نام کاربران جوانان باید در بخش خدمات و در بخش ثبت نام جوانان مراجعه کنید',
    'برای مراجعه به بخش فرم کمیسیون باید در بخش امور مالی و در بخش فرم ها بخش فرم کمیسیون مراجعه کنید',
    'برای مراجعه به بخش پرداخت مالی شما باید در بخش امور مالی و در بخش پرداخت مالی مراجعه کنید'
]

vecrors = model.encode(text_2)
client = chromadb.Client()

collection = client.create_collection(name='my_documents')

collection.add(documents=text_2,embeddings=vecrors.tolist(),ids=['1','2','3','4','5'])
api_key_gpt = getpass('your api gpt :')
api_key_weather = getpass('api key weather :')
client_ai = OpenAI(base_url='https://api.gapgpt.app/v1', api_key=api_key_gpt)

async def robot(update : Update , context : ContextTypes.DEFAULT_TYPE) :
    text = update.message.text
    if not "/" in str(text)  :
        my_text_embidding = model.encode(text)
        result = collection.query(query_embeddings=my_text_embidding.tolist(),n_results=2)
        documets = result['documents'][0]
        contexts = '\n'.join(documets)
        prompt = f"""
        اطلاعات (اگر کاربر سوالی داشت بگو و گر نه باهاش صحبت معمولی کن و چیزی به نام لینک بهشون نده و اگر درخواست لینک کردن لینکی وجود نداره و اینکه صحبت های اضافی هم اگر خواست باهاش صحبت نکن و محدودش کن) :
        {contexts}
        سوال :         
        {text}
        """
        resposnce = client_ai.responses.create(
        model='gpt-5',
        input=prompt
        )

        await update.message.reply_text(resposnce.output_text)

async def start(update : Update , context : ContextTypes.DEFAULT_TYPE) :
    await context.bot.send_message(chat_id=update.effective_chat.id,text=('لطفا با ما چت کنید'))

async def weather(update : Update , context : ContextTypes.DEFAULT_TYPE) :
    await update.message.reply_text('لطفا اسم شهر خود را بنویسید')
    return Text


async def get_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    city = update.message.text.strip()

    url = "https://api.openweathermap.org/data/2.5/weather"
    
    params = {
        "q": city,
        "appid": api_key_weather,
        "units": "metric"
    }

    try:
        result = req.get(url, params=params, timeout=10)

        if result.status_code == 404:
            await update.message.reply_text(
                "your city is not find please enter agian"
            )

        elif result.status_code == 401:
            await update.message.reply_text(
                "api is not found"
            )

        else:
            result.raise_for_status()
            data = result.json()

            temperature = data["main"]["temp"]
            description = data["weather"][0]["description"]

            await update.message.reply_text(
                f"دمای {city}: {temperature} °C\n"
                f"وضعیت هوا: {description}"
            )

    except req.exceptions.Timeout:
        await update.message.reply_text(
            "server is time out please enter agian"
        )

    except req.exceptions.RequestException:
        await update.message.reply_text(
            f"server error status code is {result.status_code}"
        )

    finally:
        return ConversationHandler.END
    


async def robot_photo(update : Update , context : ContextTypes.DEFAULT_TYPE) :
    print(update.message)
    photo = await update.message.photo[-1].get_file()
    await photo.download_to_drive('image_user.jpg')
    
    await update.message.reply_text('عکس شما دریافت شد')

async def robot_voice(update : Update , context : ContextTypes.DEFAULT_TYPE) :
    print(update.message)
    voice = await update.message.voice.get_file()

    await update.message.reply_text('ویس شما دریافت شد')
    await voice.download_to_drive('voice_user.wav')

     

if __name__ == '__main__' :
    #proxy_url = "socks5://127.0.0.1:12334"
    #request = HTTPXRequest(proxy_url=proxy_url)
    api_key_telegram = getpass('your api key telegram :')
    app = Application.builder().token(api_key_telegram).build()

    starts = CommandHandler('start',start)

    conversation = ConversationHandler(
    entry_points=[CommandHandler("weather", weather)],

    states={
        Text: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, get_city)
        ]
    },

    fallbacks=[]
    )

    new_TEXT = MessageHandler(filters.TEXT,robot)
    new_PHOTO = MessageHandler(filters.PHOTO,robot_photo)
    new_VOICE = MessageHandler(filters.VOICE,robot_voice)
    

    app.add_handler(starts)
    app.add_handler(conversation)
    
    app.add_handler(new_TEXT)
    app.add_handler(new_PHOTO)
    app.add_handler(new_VOICE)
    

    app.run_polling()




