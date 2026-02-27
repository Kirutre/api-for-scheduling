from datetime import time
from pydantic import BaseModel

from app.utils.weekday_enum import Weekday


class CourseSection(BaseModel):
    id: int
    course_id: int 
    weekday: Weekday
    start_time: time
    end_time: time
    

class CourseSectionRequest(BaseModel):
    courses: list[CourseSection]