import logging
import openai
from config import api_key

openai.api_key = api_key
    
logging.basicConfig(level=logging.INFO)

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
        # return "An error occurred while processing your request."
        return str(e)