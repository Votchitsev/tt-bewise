import requests

from .db import Questions


class QuestionsAPI:
    def __init__(self, url) -> None:
        self.url = url
        self.previous_questions = []
        self.current_questions = []

    def _turn_questions(self):
        result = self.previous_questions
        self.previous_questions = self.current_questions
        self.current_questions = []

        if len(result) > 0:
            return {
                'count': len(result),
                'questions': result,
            }
        
        return {}

    async def get_questions(self, count):
        questions_from_api = requests.get(f"{self.url}?count={count}").json()

        not_created_count = 0

        for question in questions_from_api:
            model, created = await Questions.objects.get_or_create(
                id=question['id'],
                question_text=question['question'],
                answer_text=question['answer'],
                created_at=question['created_at']
            )

            if not created:
                not_created_count += 1
            else:
                self.current_questions.append(model)

        if not_created_count > 0:
            return await self.get_questions(not_created_count)

        return self._turn_questions()
