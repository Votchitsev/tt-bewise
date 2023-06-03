import requests
import typing

from .db import Questions


class QuestionsAPI:
    def __init__(self, url: str) -> None:
        self.url = url
        self.questions_from_db = None

    def _return_questions(self) -> typing.Dict:
        if not self.questions_from_db:
            return {}

        response = {
            'count': len(self.questions_from_db),
            'questions': self.questions_from_db,
        }

        self.questions_from_db = None

        return response
    
    async def _get_questions_from_db(self):
        questions = await Questions.objects.filter(
            forResponse=True
        ).all()

        for question in questions:
            await question.update(forResponse=False)

        return questions

    async def get_questions(self, count: int) -> typing.Callable:

        try:
            questions_from_api = requests.get(f"{self.url}?count={count}").json()
        except:
            return False

        if not self.questions_from_db:
            self.questions_from_db = await self._get_questions_from_db()

        not_created_count = 0

        for question in questions_from_api:
            _, created = await Questions.objects.get_or_create(
                id=question['id'],
                question_text=question['question'],
                answer_text=question['answer'],
                created_at=question['created_at']
            )

            if not created:
                not_created_count += 1

        if not_created_count > 0:
            return await self.get_questions(not_created_count)

        return self._return_questions()
