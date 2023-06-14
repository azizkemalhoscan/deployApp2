import asyncio
import requests
from telegram import Update,InlineKeyboardButton,InlineKeyboardMarkup,Bot
from telegram.ext import ApplicationBuilder, PollHandler,ContextTypes, filters, MessageHandler,CallbackQueryHandler
import json

async def handle_poll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    results=[]
    results.append({'Question' : update.poll.question,'shoot':update.poll.options[0].voter_count, 'hold':update.poll.options[1].voter_count})
    with open('results.json','w')as fp:
        json.dump(results,fp,indent=2)

app = ApplicationBuilder().token("5942564261:AAHAxGhNQVlWQlfEh7HvuOV563EN4oukPG4").build()

app.add_handler(PollHandler(handle_poll))
app.run_polling()