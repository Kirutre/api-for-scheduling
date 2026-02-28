import pytest

from datetime import time

from app.schemas.request.courses_request import CourseSection

from app.utils.weekday_enum import Weekday
from app.utils.event_enum import Event

from app.logic.interval_graph import create_events_timeline, create_interval_graph


@pytest.fixture
def course_section_list():
    return [
        CourseSection(id=1, course_id=101, weekday=Weekday.MONDAY, start_time=time(8, 0), end_time=time(10, 0)),
        CourseSection(id=2, course_id=102, weekday=Weekday.MONDAY, start_time=time(8, 0), end_time=time(10, 0)),

        CourseSection(id=3, course_id=103, weekday=Weekday.MONDAY, start_time=time(10, 0), end_time=time(12, 0)),

        CourseSection(id=4, course_id=104, weekday=Weekday.TUESDAY, start_time=time(14, 0), end_time=time(18, 0)),
        CourseSection(id=5, course_id=105, weekday=Weekday.TUESDAY, start_time=time(15, 0), end_time=time(17, 0)),

        CourseSection(id=6, course_id=106, weekday=Weekday.WEDNESDAY, start_time=time(9, 0), end_time=time(10, 30)),
        CourseSection(id=7, course_id=107, weekday=Weekday.WEDNESDAY, start_time=time(10, 0), end_time=time(11, 0)),
        CourseSection(id=8, course_id=108, weekday=Weekday.WEDNESDAY, start_time=time(10, 45), end_time=time(12, 0)),
        
        CourseSection(id=9, course_id=109, weekday=Weekday.THURSDAY, start_time=time(8, 0), end_time=time(20, 0)),
        CourseSection(id=10, course_id=110, weekday=Weekday.THURSDAY, start_time=time(9, 0), end_time=time(10, 0)),
        CourseSection(id=11, course_id=111, weekday=Weekday.THURSDAY, start_time=time(13, 0), end_time=time(14, 0)),
        CourseSection(id=12, course_id=112, weekday=Weekday.THURSDAY, start_time=time(18, 0), end_time=time(19, 0)),

        CourseSection(id=13, course_id=113, weekday=Weekday.FRIDAY, start_time=time(7, 0), end_time=time(8, 0)),
    ]

def test_create_events_timeline_with_empty_list():
    assert create_events_timeline([]) == []


def test_create_events_timeline_with_invalid_list():
    with pytest.raises(AttributeError):
        create_events_timeline([1, 2, 3, 4])


def test_create_events_timeline_successful(course_section_list):
    events_timeline = create_events_timeline(course_section_list)
    
    assert len(events_timeline) == len(course_section_list) * 2
    
    assert events_timeline[0][2] == Event.START
    
    assert events_timeline[-1] == (Weekday.FRIDAY, time(8, 0), Event.END, 13)
    
    for i in range(len(events_timeline) - 1):
        assert events_timeline[i] <= events_timeline[i+1], f'Order error in index: {i}'
        
    events_monday_at_10 = [event for event in events_timeline if event[1] == time(10, 0) and event[0] == Weekday.MONDAY]
    
    assert events_monday_at_10[0][2] == Event.END
    assert events_monday_at_10[1][2] == Event.END
    assert events_monday_at_10[2][2] == Event.START


def test_create_interval_graph_with_empty_list():
    assert create_interval_graph([]) == {}


def test_create_interval_graph_with_invalid_list():
    with pytest.raises(AttributeError):
        create_interval_graph([1, 2, 3, 4])


def test_create_interval_graph_successful(course_section_list):
    interval_graph = create_interval_graph(course_section_list)
    
    assert len(interval_graph) == len(course_section_list)
    
    assert 2 in interval_graph[1]
    assert 1 in interval_graph[2]
       
    assert {10, 11, 12}.issubset(interval_graph[9]) == True
    for neighbor in [10, 11, 12]:
        assert 9 in interval_graph[neighbor]
    
    assert 1 not in interval_graph[9]
    
    assert 3 not in interval_graph[1]
    assert 3 not in interval_graph[2]
    
    assert interval_graph[13] == set()


def test_create_interval_graph_sorting(course_section_list):
    interval_graph = create_interval_graph(course_section_list)
    
    first_key = list(interval_graph.keys())[0]
    last_key = list(interval_graph.keys())[-1]
    
    assert len(interval_graph[first_key]) <= len(interval_graph[last_key])
    
    assert first_key == 3