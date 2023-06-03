import databases
import ormar
import sqlalchemy

from .config import settings


database = databases.Database(settings.db_url)
metadata = sqlalchemy.MetaData()


class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


class Questions(ormar.Model):
    class Meta(BaseMeta):
        tablename = "questions"

    id: int = ormar.Integer(primary_key=True)
    question_text: str = ormar.String(max_length=255)
    answer_text: str = ormar.String(max_length=255)
    created_at: str = ormar.String(max_length=50)
    forResponse: bool = ormar.Boolean(default=True)


engine = sqlalchemy.create_engine(settings.db_url)
metadata.create_all(engine)
