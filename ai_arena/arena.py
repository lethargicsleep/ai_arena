import time
import ollama
from prompts import PROMPT_DIRECTOR, PROMPT_JUDGE, PROMPT_CORRECTOR


def generate_response(system_prompt, user_content, temperature=1.2, top_p=0.95, repeat_penalty=1.1):
    try:
        response = ollama.chat(
            model="qwen2.5:14b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content},
            ],
            options={
                "temperature": temperature,
                "top_p": top_p,
                "repeat_penalty": repeat_penalty,
            },
        )
        return response["message"]["content"].strip()
    except Exception as error:
        return f"[Системная ошибка ИИ-модуля: {error}. Действие пропущено]."


def extract_tag(text, tag_name):
    start_tag = f"<{tag_name}>"
    end_tag = f"</{tag_name}>"

    start_pos = text.find(start_tag)
    end_pos = text.find(end_tag)

    if start_pos != -1 and end_pos != -1:
        return text[start_pos + len(start_tag):end_pos].strip()
    return None




def main():
    epoch_counter = 1
    try:
        while True:
            director_event = generate_response(PROMPT_DIRECTOR, "старт")

            name_a = extract_tag(director_event, "agent_a_name")
            prompt_a = extract_tag(director_event, "agent_a_prompt")
            name_b = extract_tag(director_event, "agent_b_name")
            prompt_b = extract_tag(director_event, "agent_b_prompt")
            clean_event = extract_tag(director_event, "event_text")
            print(1)
            if not all([name_a, prompt_a, name_b, prompt_b, clean_event]):
                print(name_a, prompt_a, name_b, prompt_b, clean_event)
                continue



            current_context = f"Глобальное событие: {clean_event}\n"

            for chat_step in range(4):
                query_a = f"<context>\n{current_context}\n</context>"
                reply_a = generate_response(prompt_a, query_a)
                current_context += f"{name_a}: {reply_a}\n"

                query_b = f"<context>\n{current_context}\n</context>"
                reply_b = generate_response(prompt_b, query_b)
                current_context += f"{name_b}: {reply_b}\n"

                time.sleep(1)

            judge_query = f"<context>\n{current_context}\n</context>"
            verdict = generate_response(PROMPT_JUDGE, judge_query)

            corrected_verdict = generate_response(PROMPT_CORRECTOR, verdict, temperature=0.1, top_p=0.9, repeat_penalty=1.1)
            final_entry = (
                f"ЭПОХА: {epoch_counter}\n"
                f"СОБЫТИЕ: {clean_event}\n"
                f"{corrected_verdict}\n\n"
            )

            with open("summary.txt", "a", encoding="utf-8") as file:
                file.write(final_entry)

            epoch_counter += 1
            time.sleep(3)

    except KeyboardInterrupt:
        exit()

if __name__ == "__main__":
    main()