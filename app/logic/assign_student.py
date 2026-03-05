from collections import defaultdict
from functools import lru_cache

from app.schemas.request.students_request import Student
from app.schemas.request.courses_request import CourseSection


def get_sections_by_courses(course_section_list: list[CourseSection]) -> dict[int, list]:
    sections_by_courses: defaultdict[int, list] = defaultdict(list)
    
    for section in course_section_list:
        sections_by_courses[section.course_id].append(section.id)
        
    return sections_by_courses

def count_valid_schedules(course_ids: list[int], sections_by_courses: dict[int, list], interval_graph: dict[int, set]):    
    def backtrack(course_idx: int, current_schedule_sections: set):
        if course_idx == len(course_ids):
            return 1
        
        count: int = 0
        current_course_id: int = course_ids[course_idx]
        available_sections: list[int] = sections_by_courses.get(current_course_id, [])
        
        for section_id in available_sections:
            collisions: set[int] = interval_graph.get(section_id, set())
            
            if not (collisions & current_schedule_sections):
                current_schedule_sections.add(section_id)
                
                count += backtrack(course_idx + 1, current_schedule_sections)
                
                current_schedule_sections.remove(section_id)
                
        return count
    
    return backtrack(0, set())


def get_priority_list(student_list: list[Student], course_section_list: list[CourseSection],
        interval_graph: dict[int, set]) -> dict[int, int]:
    sections_by_courses: dict[int, list] = get_sections_by_courses(course_section_list)

    results: dict[int, int] = {}
    
    @lru_cache(None)
    def count_valid_cached(course_ids_tuple: tuple[int, ...]):
        return count_valid_schedules(list(course_ids_tuple), sections_by_courses, interval_graph)

    for student in student_list:
        course_key = tuple(sorted(student.courses))

        results[student.id] = count_valid_cached(course_key)

    return dict(
        sorted(
            results.items(),
            key=lambda item: item[1]
        )
    )


def assign_students_by_priority(student_list: list[Student]):
    pass