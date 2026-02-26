from pydantic import BaseModel


class Student(BaseModel):
    id: int
    courses: list[int]


class StudentRequest(BaseModel):
    students: list[Student]