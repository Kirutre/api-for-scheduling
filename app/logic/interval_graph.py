from app.schemas.request.courses_request import CourseSection

from app.utils.event_enum import Event

def create_events_timeline(course_section_list: list[CourseSection]) -> list[tuple]:
    START = Event.START
    END = Event.END
    
    events_timeline: list[tuple] = [
        (course_section.weekday, time, event_type, course_section.id)
        for course_section in course_section_list
        for time, event_type in (
            (course_section.start_time, START), (course_section.end_time, END)
        )
    ]
    
    events_timeline.sort()
    
    return events_timeline


def create_interval_graph(course_section_list: list[CourseSection]) -> dict[int, set]:
    START = Event.START
    
    events_timeline = create_events_timeline(course_section_list)
    
    active_sections: set = set()
    interval_graph: dict[int, set] = {course_section.id: set() for course_section in course_section_list}
    
    for _, _, event_type, course_section_id in events_timeline:
        if event_type == START:
            if active_sections:
                interval_graph[course_section_id].update(active_sections)
                
                for active_section_id in active_sections:
                    interval_graph[active_section_id].add(course_section_id)

            active_sections.add(course_section_id)
        
        else:
            active_sections.discard(course_section_id)
    
    return dict(
        sorted(
            interval_graph.items(),
            key=lambda value: len(value[1])
        )
    )