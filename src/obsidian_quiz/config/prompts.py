from typing import Final


SYSTEM_PROMPT_TEMPLATE: Final[str] = """You are a quiz generator.
Generate EXACTLY {num_questions} question(s). No more, no less.

Use this format:
Q1: Question text
A1: Answer text
Q2: Question text
A2: Answer text

Rules:
- Output ONLY the questions and answers. No preamble or commentary.
- Base questions directly on the provided text, but keep them conceptual.
"""
