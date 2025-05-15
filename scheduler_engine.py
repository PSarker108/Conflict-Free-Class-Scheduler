from collections import defaultdict

class SchedulerEngine:
    def __init__(self, courses, rooms, timeslots, teachers, conflict_graph):
        self.courses = courses
        self.rooms = rooms
        self.timeslots = timeslots
        self.teachers = {t.id: t for t in teachers}
        self.conflict_graph = conflict_graph

        self.schedule = {} 
        self.teacher_load = defaultdict(int)
        self.room_usage = defaultdict(set)  

    def get_available_teacher(self, possible_ids, slot_id):
        for tid in possible_ids:
            teacher = self.teachers.get(tid)
            if teacher and slot_id in teacher.available_times:
                if self.teacher_load[tid] < teacher.max_load:
                    return tid 
        return None

    def is_valid_assignment(self, course, slot, room):
        possible_teachers = [tid.strip() for tid in course.teacher_id.split(',')]

        assigned_teacher = self.get_available_teacher(possible_teachers, slot.id)
        if not assigned_teacher:
            return None 

        if course.course_type != room.type:
            return None

        if room.capacity < course.capacity_required:
            return None

        if (room.id, slot.id) in self.room_usage:
            return None

        for conflict_id in self.conflict_graph.get(course.id, []):
            if conflict_id in self.schedule and self.schedule[conflict_id][0].id == slot.id:
                return None

        return assigned_teacher

    def backtrack(self, course_index):
        if course_index == len(self.courses):
            return True  

        course = self.courses[course_index]

        for slot in self.timeslots:
            for room in self.rooms:
                assigned_teacher = self.is_valid_assignment(course, slot, room)

                if assigned_teacher:
                    
                    self.schedule[course.id] = (slot, room, assigned_teacher)
                    self.teacher_load[assigned_teacher] += 1
                    self.room_usage[(room.id, slot.id)].add(course.id)

                    if self.backtrack(course_index + 1):
                        return True

                  
                    del self.schedule[course.id]
                    self.teacher_load[assigned_teacher] -= 1
                    self.room_usage[(room.id, slot.id)].remove(course.id)

        return False

    def generate_schedule(self):
        success = self.backtrack(0)
        if success:
            return self.schedule
        else:
            return None
