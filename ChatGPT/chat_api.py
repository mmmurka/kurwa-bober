import logging
import os

import openai
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()


class ChatGPT:
    def __init__(self, role: str = None):
        self.api_key: str = os.getenv('OPENAI_API_KEY')
        openai.api_key = self.api_key
        self.role: str = role
        self.client: AsyncOpenAI = AsyncOpenAI()

    async def get_response(self, user_message: str, temperature: float = 0.0) -> str:
        logging.info("Відправляємо запит до ChatGPT.")
        try:
            completion = await self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": self.role},
                    {"role": "user", "content": user_message},
                ],
                temperature=temperature
            )

            gpt_reply = completion.choices[0].message.content
            return gpt_reply
        except Exception as e:
            logging.error(e)
            return "Error: Unable to get a response from ChatGPT."

