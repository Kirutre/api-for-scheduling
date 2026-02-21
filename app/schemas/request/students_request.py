from pydantic import BaseModel


class Student(BaseModel):
    id: int
    name: str | None = None
    courses: list[str]


class StudentsRequest(BaseModel):
    students: list[Student]