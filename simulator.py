"""Симуляция эпох: событие → диалог → вердикт → коррекция → запись."""

import time

from config import CHAT_STEPS, STEP_DELAY, EPOCH_DELAY, RETRY_DELAY
from llm import generate_creative, generate_correction
from parser import parse_director_event
from prompts import PROMPT_DIRECTOR, PROMPT_JUDGE, PROMPT_CORRECTOR


class Simulator:
    def __init__(self, storage, steps=CHAT_STEPS):
        self.storage = storage
        self.steps = steps
        self.epoch_counter = 1

    def run_epoch(self):
        director_event = generate_creative(PROMPT_DIRECTOR, "старт")
        event_data = parse_director_event(director_event)

        if event_data is None:
            return False

        current_context = f"Глобальное событие: {event_data['event']}\n"

        for _ in range(self.steps):
            query_a = f"<context>\n{current_context}\n</context>"
            reply_a = generate_creative(event_data["prompt_a"], query_a)
            current_context += f"{event_data['name_a']}: {reply_a}\n"

            query_b = f"<context>\n{current_context}\n</context>"
            reply_b = generate_creative(event_data["prompt_b"], query_b)
            current_context += f"{event_data['name_b']}: {reply_b}\n"

            time.sleep(STEP_DELAY)

        judge_query = f"<context>\n{current_context}\n</context>"
        verdict = generate_creative(PROMPT_JUDGE, judge_query)
        corrected = generate_correction(PROMPT_CORRECTOR, verdict)

        self.storage.append_epoch(self.epoch_counter, event_data["event"], corrected)
        self.epoch_counter += 1
        return True

    def run_forever(self):
        try:
            while True:
                success = self.run_epoch()

                if not success:
                    time.sleep(RETRY_DELAY)
                    continue

                time.sleep(EPOCH_DELAY)
        except KeyboardInterrupt:
            pass