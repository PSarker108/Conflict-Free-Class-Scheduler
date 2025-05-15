import csv
from collections import namedtuple

Room = namedtuple('Room', ['id', 'building', 'type', 'capacity', 'availability'])
TimeSlot = namedtuple('TimeSlot', ['id', 'day', 'start', 'end'])
Course = namedtuple('Course', ['id', 'teacher_id', 'department', 'prerequisites', 'course_type', 'capacity_required'])
Teacher = namedtuple('Teacher', ['id', 'max_load', 'available_times'])

def parse_list(value):
    if '|' in value:
        return [v.strip() for v in value.split('|')]
    return [v.strip() for v in value.split(';')] if value else []


class DataLoader:
    @staticmethod
    def load_rooms(path):
        with open(path, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            return [Room(
                id=row['id'],
                building=row['building'],
                type=row['type'].lower(),
                capacity=int(row['capacity']),
               
                availability=parse_list(row['availability'])
            ) for row in reader]

    @staticmethod
    def load_timeslots(path):
        with open(path, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            return [TimeSlot(
                id=row['id'],
                day=row['day'],
                start=row['start'],
                end=row['end']
            ) for row in reader]

    @staticmethod
    def load_courses(path):
        with open(path, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            return [Course(
                id=row['id'],
                teacher_id=row['teacher_id'],
                department=row['department'],
                prerequisites=parse_list(row['prerequisites']),
                course_type=row['course_type'].lower(),
                capacity_required=int(row['capacity_required'])
            ) for row in reader]

    @staticmethod
    def load_teachers(path):
        with open(path, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            return [Teacher(
                id=row['id'],
                max_load=int(row['max_load']),
                available_times=parse_list(row['available_times'])
            ) for row in reader]

    @staticmethod
    def load_all_custom(paths):
        return {
            'courses': DataLoader.load_courses(paths['courses']),
            'rooms': DataLoader.load_rooms(paths['rooms']),
            'teachers': DataLoader.load_teachers(paths['teachers']),
            'timeslots': DataLoader.load_timeslots(paths['timeslots'])
        }
@staticmethod
def load_all_custom(paths):
    return {
        'courses': DataLoader.load_courses(paths['courses']),
        'rooms': DataLoader.load_rooms(paths['rooms']),
        'teachers': DataLoader.load_teachers(paths['teachers']),
        'timeslots': DataLoader.load_timeslots(paths['timeslots'])
    }

