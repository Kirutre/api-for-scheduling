import pytest
from datetime import time

from app.schemas.request.courses_request import CourseSection

from app.utils.weekday_enum import Weekday
from app.utils.event_enum import Event

from app.logic.interval_graph import create_events_timeline


@pytest.fixture
def course_section_list():
    return [
        CourseSection(id=1, course_id=1, weekday=Weekday.MONDAY, start_time=time(8, 0, 0), end_time=time(10, 0, 0)),
        CourseSection(id=2, course_id=1, weekday=Weekday.MONDAY, start_time=time(8, 0, 0), end_time=time(10, 0, 0)),
        CourseSection(id=3, course_id=1, weekday=Weekday.MONDAY, start_time=time(10, 0, 0), end_time=time(12, 0, 0)),
        CourseSection(id=4, course_id=2, weekday=Weekday.MONDAY, start_time=time(9, 0, 0), end_time=time(11, 0, 0)),
        CourseSection(id=5, course_id=3, weekday=Weekday.MONDAY, start_time=time(8, 0, 0), end_time=time(12, 0, 0)),
        CourseSection(id=6, course_id=3, weekday=Weekday.THURSDAY, start_time=time(8, 0, 0), end_time=time(10, 0, 0)),
        CourseSection(id=7, course_id=4, weekday=Weekday.MONDAY, start_time=time(8, 30, 0), end_time=time(9, 0, 0)),
    ]

def test_create_events_timeline_with_empty_list():
    assert create_events_timeline([]) == []


def test_create_events_timeline_with_invalid_list():
    with pytest.raises(AttributeError):
        create_events_timeline([1, 2, 3, 4])
        

def test_create_events_timeline_successful(course_section_list):
    assert len(create_events_timeline(course_section_list)) == 14
    assert create_events_timeline(course_section_list)[0][2] == Event.START
    assert create_events_timeline(course_section_list)[-1] == (Weekday.THURSDAY, time(10, 0, 0), Event.END, 6)