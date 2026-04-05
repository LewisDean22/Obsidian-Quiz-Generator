"""
FIXME: I think ` symbol may break the parser!
"""
import re
from obsidian_quiz.models import Quiz, Question


def split_quiz_by_question(quiz_string: str) -> list[str]:
    # Removes leading/trailing whitespace before splitting by new lines
    question_list = re.split(r"\n\n", quiz_string.strip())
    if not question_list:
        raise ValueError("Quiz questions do not match the expected format")
    return question_list


def split_questions_and_answers(
    quiz_string: str
) -> tuple[list[str], list[str]]:

    questions = re.findall(r"(?<=Q\d:)(.*?)(?=\n+A\d+:)", quiz_string.strip(),
                           flags=re.S)
    answers = re.findall(r"(?<=A\d:)(.*?)(?=\n+|$)", quiz_string.strip(),
                         flags=re.S)
    if questions and len(questions) == len(answers):
        return (
            [question.strip() for question in questions],
            [answer.strip() for answer in answers],
        )
    raise ValueError("Either no questions found or number of questions found "
                     "differs from number of answers found.")


def create_quiz_object(
        note_name: str,
        quiz_content: str
) -> Quiz:
    questions_list, answers_list = split_questions_and_answers(quiz_content)
    questions = tuple(
        Question(text, answer) for text, answer
        in zip(questions_list, answers_list)
    )
    return Quiz(note_name, questions, quiz_content)
