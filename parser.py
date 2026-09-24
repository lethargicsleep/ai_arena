"""Парсинг XML-тегов из ответов модели."""


def _extract_tag(text: str, tag_name: str) -> str | None:
    """Достаёт содержимое тега <tag_name>...</tag_name>. None, если тега нет."""
    start_tag = f"<{tag_name}>"
    end_tag = f"</{tag_name}>"

    start_pos = text.find(start_tag)
    end_pos = text.find(end_tag)

    if start_pos != -1 and end_pos != -1:
        return text[start_pos + len(start_tag):end_pos].strip()
    return None


def parse_director_event(text: str) -> dict | None:
    """Парсит ответ директора. Возвращает словарь или None, если чего-то не хватает."""
    event = _extract_tag(text, "event_text")
    name_a = _extract_tag(text, "agent_a_name")
    prompt_a = _extract_tag(text, "agent_a_prompt")
    name_b = _extract_tag(text, "agent_b_name")
    prompt_b = _extract_tag(text, "agent_b_prompt")

    if not all([event, name_a, prompt_a, name_b, prompt_b]):
        return None

    return {
        "event": event,
        "name_a": name_a,
        "prompt_a": prompt_a,
        "name_b": name_b,
        "prompt_b": prompt_b,
    }