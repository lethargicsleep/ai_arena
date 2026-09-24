MODEL = "qwen2.5:14b"
CORRECTOR_MODEL = "qwen2.5:7b"

SUMMARY_PATH = "summary.txt"

CHAT_STEPS = 4
EPOCH_DELAY = 3
STEP_DELAY = 1
RETRY_DELAY = 1

CREATIVE = {
    "temperature": 1.2, # высокая вариативность для более безумных сюжетов
    "top_p": 0.95, # отрезаем хвост из маловероятных вариантов
    "repeat_penalty": 1.1, # штраф, чтобы агенты не зацикливались
}


CORRECTION = {
    "temperature": 0.1, # низкая вариативность для стабильных исправлений
    "top_p": 0.9, # сужаем выбор, без синонимов-фантазий
    "repeat_penalty": 1.0, # выключен, в русском языке повторы нормальны
}