import json
import os
import datetime


class Highscores:
    def __init__(self):
        self.filename = "highscores.json"
        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as f:
                json.dump([], f)

    def load(self):
        with open(self.filename, 'r') as f:
            return json.load(f)

    def save(self, data):
        with open(self.filename, 'w') as f:
            json.dump(data, f)

    def add_score(self, name, score):
        """Добавляет новый рекорд с валидацией"""
        if not name or not name.strip():
            raise ValueError("Имя не может быть пустым")

        name = name.strip()[:15]

        try:
            score = int(score)
            if score < 0:
                raise ValueError("Счет не может быть отрицательным")
        except (TypeError, ValueError):
            raise ValueError("Некорректное значение счета")

        scores = self.load()
        scores.append({
            "name": name,
            "score": score,
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        })

        scores.sort(key=lambda x: x["score"], reverse=True)
        self.save(scores[:10])