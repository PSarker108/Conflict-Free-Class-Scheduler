import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from collections import defaultdict
import os

from data_loader import DataLoader
from scheduler_engine import SchedulerEngine

csv_paths = {
    'courses': None,
    'rooms': None,
    'teachers': None,
    'timeslots': None
}

root = tk.Tk()
root.title("📚 Conflict-Free Class Scheduler")
root.geometry("960x600")
root.configure(bg="#f0f8ff")


title_label = tk.Label(root, text="Conflict-Free Class Scheduler", font=("Helvetica", 20, "bold"), bg="#f0f8ff", fg="#2c3e50")
title_label.pack(pady=10)

label_frame = tk.Frame(root, bg="#f0f8ff")
label_frame.pack(pady=5)

label_map = {}

style = ttk.Style()
style.configure("Treeview.Heading", font=("Arial", 11, "bold"), background="#2980b9", foreground="white")
style.configure("Treeview", font=("Arial", 10), rowheight=26)


button_colors = {"courses": "#aed6f1", "rooms": "#fad7a0", "teachers": "#a9dfbf", "timeslots": "#f5b7b1"}

def load_file(key):
    path = filedialog.askopenfilename(title=f"Select {key}.csv", filetypes=[("CSV Files", "*.csv")])
    if path:
        csv_paths[key] = path
        label_map[key].config(text=os.path.basename(path), fg="#117864")

for key in csv_paths.keys():
    frame = tk.Frame(root, bg="#f0f8ff")
    frame.pack(pady=3)
    btn = tk.Button(frame, text=f"📂 Load {key}.csv", command=lambda k=key: load_file(k), bg=button_colors[key], font=("Arial", 10, "bold"))
    btn.pack(side="left", padx=4)
    lbl = tk.Label(frame, text="No file selected", fg="gray", bg="#f0f8ff", font=("Arial", 9))
    lbl.pack(side="left")
    label_map[key] = lbl

cols = ("Course", "Room", "Day", "Time", "Teacher")
tree = ttk.Treeview(root, columns=cols, show='headings')
for col in cols:
    tree.heading(col, text=col)
    tree.column(col, width=150)
tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

style = ttk.Style()
style.theme_use("default")

style.configure("Treeview.Heading",
                background="#2c3e50", foreground="white",
                font=("Arial", 11, "bold"))

scroll = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
tree.configure(yscroll=scroll.set)
scroll.pack(side='right', fill='y')

def generate_schedule():
    if not all(csv_paths.values()):
        messagebox.showwarning("Missing Files", "Please select all required CSV files.")
        return

    try:
        data = DataLoader.load_all_custom(csv_paths)

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

        for row in tree.get_children():
            tree.delete(row)

        if final_schedule:
            for cid, (slot, room, teacher_id) in final_schedule.items():
                tree.insert("", "end", values=(cid, room.id, slot.day, f"{slot.start}-{slot.end}", teacher_id), tags=('generated',))
            tree.tag_configure('generated', background="#d4efdf")
        else:
            messagebox.showerror("Failed", "❌ Could not generate schedule.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

btn = tk.Button(root, text="🧠 Generate Schedule", command=generate_schedule, font=("Arial", 12, "bold"), bg="#27ae60", fg="white")
btn.pack(pady=10)

root.mainloop()
