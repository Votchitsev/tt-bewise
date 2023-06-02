from pydantic import BaseModel, validator
from fastapi import HTTPException


class QuestionsQuery(BaseModel):
    questions_num: int

    @validator('questions_num')
    def question_num_validate(cls, value):
        if value <= 0:
            detail = {
                "detail": [
                    {
                        "loc": [
                            "body",
                            "questions_num"
                        ],
                        "msg": "questions_num should be more than 0",
                        "type": ""
                    }
                ]
            }

            raise HTTPException(status_code=400, detail=detail)

        return value
