import os
import atexit
from openai import OpenAI
from obsidian_quiz.utils.response_parser import (
  split_into_questions_and_answers,
)
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())
OpenAI_client = OpenAI(
  api_key=os.getenv("OPENAI_API_KEY")
)


# Messages argument is deprecated - need to use response =
# client.chat.completions.create to add system prompts more clearly?
def generate_quiz_from_note(client: OpenAI, note_content: str,
                            system_prompt: str) -> str:
    response = client.responses.create(
        model="gpt-4o-mini",
        input=f"{system_prompt}\n\n{note_content}",
        store=True
    )
    return response.output_text


def get_quiz(note_content, system_prompt) -> tuple[list[str], list[str]]:
    quiz = generate_quiz_from_note(OpenAI_client, note_content, system_prompt)
    questions, answers = split_into_questions_and_answers(quiz)
    return questions, answers


@atexit.register
def cleanup_openai():
    try:
        OpenAI_client.close()
    except Exception as e:
        print(f"OpenAI Cleanup error: {e}")
