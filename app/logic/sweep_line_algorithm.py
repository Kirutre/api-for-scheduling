from collections import defaultdict

from schemas.request.courses_request import Course

from utils.event_enum import Event


def sweep_line(courses: list[Course]) -> dict[Course, set[Course]]:
    events: list[tuple] = [
        (course.weekday, time, event_type, course)
        for course in courses
        for time, event_type in [(course.start_time, Event.START), (course.end_time, Event.END)]
    ]
    
#    for course in courses:
#        events.append((course.weekday, course.start_time, Event.START, course))
#        events.append((course.weekday, course.end_time, Event.END, course))
    
    events.sort()
    
    active_courses: set[Course] = set()
    #* {} is faster than dict() (at least twice)
    interval_graph: defaultdict[Course, set[Course]] = defaultdict(set)
    
    for _, _, event_type, section in events:
        if event_type == Event.START:
            if active_courses:
                #* .setdefault return the existing value for the key, if the key don't exist it inserts the key and the default_value (set in this case
                #* .update add items form another set to the current set
                interval_graph.setdefault(section, set()).update(active_courses)
                
                for active in active_courses:
                    interval_graph.setdefault(active, set()).add(section)
                
            active_courses.add(section)

        else:
            active_courses.remove(section)
        
    return interval_graph

#TODO acces by list indexes instead of dictionary keys