"""работа с ollama: отправка промптов и получение ответов"""

import ollama
from config import MODEL, CORRECTOR_MODEL, CREATIVE, CORRECTION


def _call_model(system_prompt, user_content, model=MODEL, **options):
    try:
        response = ollama.chat(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content},
            ],
            options=options,
        )
        return response["message"]["content"].strip()
    except Exception as error:
        return f"[Системная ошибка ИИ-модуля: {error}. Действие пропущено]."


def generate_creative(system_prompt, user_content):
    return _call_model(system_prompt, user_content, model=MODEL, **CREATIVE)


def generate_correction(system_prompt, user_content):
    return _call_model(system_prompt, user_content, model=CORRECTOR_MODEL, **CORRECTION)