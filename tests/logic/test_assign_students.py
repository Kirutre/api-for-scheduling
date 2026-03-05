import time as tm
import pytest

from datetime import time

from app.schemas.request.students_request import Student
from app.schemas.request.courses_request import CourseSection

from app.utils.weekday_enum import Weekday

from app.logic.assign_student import get_priority_list, assign_students_by_priority
from app.logic.interval_graph import create_interval_graph


@pytest.fixture
def student_list():
    return [
        Student(id=1, courses=[104, 105]),

        Student(id=2, courses=[101, 102, 103]),

        Student(id=3, courses=[111, 112, 113]),
        Student(id=4, courses=[111, 112, 113]),

        Student(id=5, courses=[101, 104]),

        Student(id=6, courses=[101]),
        
        Student(id=7, courses=[101, 111, 112, 113, 104])
    ]

@pytest.fixture
def course_section_list():
    return [
        CourseSection(id=1, course_id=101, weekday=Weekday.MONDAY, start_time=time(8, 0), end_time=time(10, 0)),
        CourseSection(id=14, course_id=101, weekday=Weekday.MONDAY, start_time=time(14, 0), end_time=time(16, 0)),
        CourseSection(id=15, course_id=101, weekday=Weekday.TUESDAY, start_time=time(8, 0), end_time=time(10, 0)),

        CourseSection(id=2, course_id=102, weekday=Weekday.MONDAY, start_time=time(8, 0), end_time=time(10, 0)),
        CourseSection(id=16, course_id=102, weekday=Weekday.TUESDAY, start_time=time(9, 0), end_time=time(11, 0)),

        CourseSection(id=3, course_id=103, weekday=Weekday.MONDAY, start_time=time(10, 0), end_time=time(12, 0)),

        CourseSection(id=4, course_id=104, weekday=Weekday.TUESDAY, start_time=time(14, 0), end_time=time(18, 0)),
        CourseSection(id=17, course_id=104, weekday=Weekday.WEDNESDAY, start_time=time(14, 0), end_time=time(18, 0)),

        CourseSection(id=5, course_id=105, weekday=Weekday.TUESDAY, start_time=time(15, 0), end_time=time(17, 0)),

        CourseSection(id=11, course_id=111, weekday=Weekday.THURSDAY, start_time=time(13, 0), end_time=time(14, 0)),
        CourseSection(id=12, course_id=112, weekday=Weekday.THURSDAY, start_time=time(18, 0), end_time=time(19, 0)),
        CourseSection(id=13, course_id=113, weekday=Weekday.FRIDAY, start_time=time(7, 0), end_time=time(8, 0)),
    ]


def test_get_priority_list_empty_case():
    assert get_priority_list([], [], {}) == {}
    
    s = [Student(id=99, courses=[999])]
    res = get_priority_list(s, [], {})
    assert res[99] == 0

def test_get_priority_list_successful(student_list, course_section_list):
    interval_graph = create_interval_graph(course_section_list)
    priority_list = get_priority_list(student_list, course_section_list, interval_graph)
    
    assert len(priority_list) == len(student_list)
    
    priorities = list(priority_list.values())
    assert priorities == sorted(priorities)
    
    first_student_id = list(priority_list.keys())[0]
    assert priority_list[first_student_id] >= 0
    
    same_course_students = [s for s in student_list if s.courses == [111, 112, 113]]
    if len(same_course_students) >= 2:
        id1, id2 = same_course_students[0].id, same_course_students[1].id
        assert priority_list[id1] == priority_list[id2]

def test_get_priority_list_performance(course_section_list):
    import random

    course_pool = list(set(s.course_id for s in course_section_list))

    stress_students = [
        Student(id=i, courses=random.sample(course_pool, k=min(len(course_pool), 5)))
        for i in range(1000)
    ]

    graph = create_interval_graph(course_section_list)

    start_time = tm.time()
    results = get_priority_list(stress_students, course_section_list, graph)
    end_time = tm.time()

    duration = end_time - start_time
    print(f"\nBenchmark: 1000 students processed in {duration:.4f} seconds")
    
    assert duration < 2.0