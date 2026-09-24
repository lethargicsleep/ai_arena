"""Сохранение и чтение эпох."""


class FileStorage:

    def __init__(self, path):
        self.path = path

    def append_epoch(self, epoch, event, verdict):
        entry = f"ЭПОХА: {epoch}\nСОБЫТИЕ: {event}\n{verdict}\n\n"
        with open(self.path, "a", encoding="utf-8") as file:
            file.write(entry)

    def read_all(self): # в будущем для аналитика
        with open(self.path, "r", encoding="utf-8") as file:
            return file.read()