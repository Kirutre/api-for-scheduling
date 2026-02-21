from datetime import time
from pydantic import BaseModel

from utils.weekday_enum import Weekday


class Course(BaseModel):
    id: int
    name: str
    section: str
    weekday: Weekday
    start_time: time
    end_time: time
    

class CoursesRequest(BaseModel):
    courses: list[Course]