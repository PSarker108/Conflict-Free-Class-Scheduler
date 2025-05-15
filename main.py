from data_loader import DataLoader
from scheduler_engine import SchedulerEngine
from collections import defaultdict


data_dir = "data"  
data = DataLoader.load_all(data_dir)

courses = data['courses']
rooms = data['rooms']
timeslots = data['timeslots']
teachers = data['teachers']


conflict_graph = defaultdict(set)

course_map = {c.id: c for c in courses}
for course in courses:

    for prereq in course.prerequisites:
        if prereq in course_map:
            conflict_graph[course.id].add(prereq)
            conflict_graph[prereq].add(course.id)

    for other in courses:
        if other != course and other.department == course.department:
            conflict_graph[course.id].add(other.id)


engine = SchedulerEngine(courses, rooms, timeslots, teachers, conflict_graph)
final_schedule = engine.generate_schedule()


if final_schedule:
    print("✅ Schedule generated successfully:\n")
    for course_id, (slot, room, teacher_id) in final_schedule.items():
        print(f"{course_id} ➤ Room: {room.id}, Time: {slot.id} ({slot.day} {slot.start}-{slot.end}), Teacher: {teacher_id}")
else:
    print("❌ Could not generate a conflict-free schedule. Try adjusting room or teacher availability.")
