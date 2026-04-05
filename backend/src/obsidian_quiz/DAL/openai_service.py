import os
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI, OpenAIError
from obsidian_quiz.DAL.interfaces import LLMService
from obsidian_quiz.utils.quiz_parser import create_quiz_object
from obsidian_quiz.models import Note, Quiz
from obsidian_quiz.config.prompts import SYSTEM_PROMPT_TEMPLATE


class OpenAIService(LLMService):

    def __init__(self, system_prompt_template=SYSTEM_PROMPT_TEMPLATE):
        load_dotenv(find_dotenv())
        self._client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self._system_prompt_template = system_prompt_template

    def generate_quiz(self, note: Note, num_questions: int) -> Quiz:
        try:
            system_prompt = self._system_prompt_template.format(
                num_questions=num_questions
            )
            response = self._client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": note.content}
                ]
            )
            quiz_content = response.choices[0].message.content
            return create_quiz_object(note.name, quiz_content)
        except OpenAIError as e:
            raise RuntimeError(f"Quiz generation failed: {e}") from e
