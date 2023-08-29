import asyncpg
import logging
import random
from config import token, database
from chatgpt import request_chat_gpt
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, User
from telegram.ext import (ApplicationBuilder, CommandHandler, ContextTypes,
                          MessageHandler, filters)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
TELEGRAM_API_TOKEN = token

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    first_name = user.first_name
    welcome_message = f"Hello, {first_name}! I'm a bot, please talk to me!"
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=welcome_message
    )


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')
    response = request_chat_gpt(update.message.text)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "Here are some available commands:\n"
        "/start - Begin interacting with the bot\n"
        "/help - Get assistance with using the bot\n"
        "/about - Learn more about the bot and its features\n"
        "/settings - Configure preferences and settings\n"
        "/topic - Set a conversation topic\n"
        "/random - Receive a random response\n"
        "/inspire - Get an inspirational message\n"
        "/joke - Enjoy a lighthearted joke\n"
        "/fact - Discover an interesting fact\n"
        "/story - Listen to a short story"
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=help_text)


async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    about_text = (
        "ChatGPT Bot: Sparking creativity through engaging conversations.\n"
        "Share and chat now!"
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=about_text)


async def settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    settings_text = "You can customize your settings here."
    await context.bot.send_message(chat_id=update.effective_chat.id, text=settings_text)


async def topic_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    topic_text = "Enter a topic you'd like to discuss."
    await context.bot.send_message(chat_id=update.effective_chat.id, text=topic_text)


async def random_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    random_responses = [
        "Here's a random response!",
        "Enjoy this unexpected reply.",
        "Surprise!",
        "Life is full of surprises.",
        "Ready for something completely different?",
        "Rolling the dice: you get this reply!",
    ]
    random_response = random.choice(random_responses)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=random_response)


async def inspire_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    inspire_responses = [
        "You're capable of amazing things!",
        "Embrace your creativity.",
        "Inspiration is all around you.",
        "Believe in yourself and your potential.",
        "Challenges are opportunities in disguise.",
        "Dream big, and make it happen!",
    ]
    inspire_message = random.choice(inspire_responses)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=inspire_message)


async def joke_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    joke_responses = [
        "Why did the chicken go to the seance? To talk to the other side!",
        "Did you hear about the mathematician who’s afraid of negative numbers? He’ll stop at nothing to avoid them.",
        "Parallel lines have so much in common. It’s a shame they’ll never meet.",
        "I told my wife she was drawing her eyebrows too high. She seemed surprised.",
        "I used to play piano by ear, but now I use my hands.",
        "What do you call a can opener that doesn’t work? A can’t opener.",
    ]
    joke = random.choice(joke_responses)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=joke)

async def fact_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    fact_responses = [
        "Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still perfectly edible!",
        "The shortest war in history was between Britain and Zanzibar on August 27, 1896. Zanzibar surrendered after 38 minutes.",
        "Bananas are berries, but strawberries are not!",
        "Octopuses have three hearts: two pump blood to the gills, and one pumps it to the rest of the body.",
        "A group of flamingos is called a 'flamboyance.'",
        "The average person will spend six months of their life waiting for red lights to turn green.",
    ]
    fact = random.choice(fact_responses)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=fact)


async def story_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    story_responses = [
        "Once upon a time, in a faraway land, there lived a curious cat named Whiskers. Whiskers loved exploring the enchanted forest...",
        "In a world where time traveled backward, Sarah found herself reliving each day with newfound perspective. She learned to cherish every moment...",
        "On a distant planet, a group of explorers discovered a hidden cave that held ancient secrets. As they ventured deeper...",
        "In a small village nestled between rolling hills, a young blacksmith named Liam dreamt of forging the finest sword ever crafted...",
        "High above the clouds, a brave pilot named Amelia embarked on a solo flight around the world. Along the way, she encountered...",
        "In a bustling city, a street artist named Maya used vibrant colors to transform ordinary walls into breathtaking murals...",
    ]
    story = random.choice(story_responses)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=story)


if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_API_TOKEN).build()

    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    help_handler = CommandHandler('help', help_command)
    about_handler = CommandHandler('about', about_command)
    settings_handler = CommandHandler('settings', settings_command)
    topic_handler = CommandHandler('topic', topic_command)
    random_handler = CommandHandler('random', random_command)
    inspire_handler = CommandHandler('inspire', inspire_command)
    joke_handler = CommandHandler('joke', joke_command)
    fact_handler = CommandHandler('fact', fact_command)
    story_handler = CommandHandler('story', story_command)

    application.add_handler(start_handler)
    application.add_handler(echo_handler)
    application.add_handler(help_handler)
    application.add_handler(about_handler)
    application.add_handler(settings_handler)
    application.add_handler(topic_handler)
    application.add_handler(random_handler)
    application.add_handler(inspire_handler)
    application.add_handler(joke_handler)
    application.add_handler(fact_handler)
    application.add_handler(story_handler)

    application.run_polling()