import openai
import logging
from telegram import Update
from config import *
from telegram.ext import (ApplicationBuilder, CommandHandler, ContextTypes,
                          MessageHandler, filters)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TELEGRAM_API_TOKEN = token
openai.api_key = api_key


def request_chat_gpt(user_message):
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": user_message}
            ]
        )
        return completion.choices[0].message['content']
    except openai.error.AuthenticationError as auth_error:
        logging.error(f"Authentication Error: {auth_error}")
        return "An authentication error occurred."
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return "An error occurred while processing your request."


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    first_name = user.first_name
    
    welcome_message = f"Hello, {first_name}! I'm a bot, please talk to me!"
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=welcome_message
    )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')
    response = request_chat_gpt(update.message.text)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "Here are some available commands:\n"
        "/start - Begin interacting with the bot\n"
        "/help - Get assistance with using the bot\n"
        "/about - Learn more about the bot and its features\n"
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=help_text)


async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    about_text = (
        "ChatGPT Bot: Sparking creativity through engaging conversations.\n"
        "Share and chat now!"
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=about_text)




if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_API_TOKEN).build()

    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    help_handler = CommandHandler('help', help_command)
    about_handler = CommandHandler('about', about_command)


    application.add_handler(start_handler)
    application.add_handler(echo_handler)
    application.add_handler(help_handler)
    application.add_handler(about_handler)

    application.run_polling()