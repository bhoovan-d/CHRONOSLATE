import json
import mysql.connector
import random
import matplotlib.pyplot as plt
import pandas as pd
from dotenv import load_dotenv
import os






load_dotenv(dotenv_path=".env file path here")

db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')
db_port = os.getenv('DB_PORT')

with open("C:/Users/bhoov/Downloads/timetable.json") as f:
    data = json.load(f)


conn = mysql.connector.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    database=db_name,
    port=db_port
)
cursor = conn.cursor()

N = int(input("Enter group number= "))
groups = {
    '2': ["MATH F111", "CHEM F111", "EEE F111", "CHEM F110", "PHY F111", "PHY F110", "ME F112"],
    '1': ["BIO F111", "BIO F110", "BITS F110", "BITS F111", "BITS F112", "CS F111", "MATH F111"]
}

for course_code in groups[str(N)]:
    if course_code in data['courses']:
        course_info = data['courses'][course_code]
        sections = course_info.get('sections')

        for section_name, section_info in sections.items():
            instructors = ', '.join(section_info.get('instructor'))
            for sched in section_info.get('schedule'):
                room = sched.get('room')
                days = ', '.join(sched.get('days'))
                hours = ', '.join(map(str, sched.get('hours')))

                cursor.execute("""
                    INSERT INTO course_schedule (course_code, section, instructors, room, days, hours)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (course_code, section_name, instructors, room, days, hours))

conn.commit()

cursor = conn.cursor(dictionary=True)

cursor.execute("SELECT DISTINCT * FROM course_schedule")
rows = cursor.fetchall()

courses = {}
subject_data = set()

lecture_dict = {}
tutorial_dict = {}
practical_dict = {}

for row in rows:
    if row['course_code'] in groups[str(N)]:

        course_code = row['course_code']
        section_type = row['section'][0]
        course_code_transformed = row['course_code'].replace(" ", "_")
        subject_data.add(course_code_transformed)
        for i in subject_data:
            lecture_dict[i] = []
            tutorial_dict[i] = []
            practical_dict[i] = []

        if course_code not in courses:
            courses[course_code] = {}

        if section_type not in courses[course_code]:
            courses[course_code][section_type] = []

        section_info = {
            "course code": row['course_code'],
            "section": row['section'],
            "instructors": row['instructors'],
            "room": row['room'],
            "days": row['days'],
            "hours": row['hours']
        }

        if section_info not in courses[course_code][section_type]:
            courses[course_code][section_type].append(section_info)

g = [lecture_dict, tutorial_dict, practical_dict]

for j in g:
    for h in j:

        for course in courses:
            for section in courses[course]:
                for v in courses[course][section]:

                    if course == h.replace('_', " "):

                        if section == 'L' and v not in lecture_dict[h]:
                            lecture_dict[h].append(v)
                        elif section == 'T' and v not in tutorial_dict[h]:
                            tutorial_dict[h].append(v)
                        elif section == 'P' and v not in practical_dict[h]:
                            practical_dict[h].append(v)

lecture_dict = {k: v for k, v in lecture_dict.items() if v != []}
tutorial_dict = {k: v for k, v in tutorial_dict.items() if v != []}
practical_dict = {k: v for k, v in practical_dict.items() if v != []}

tutorial_dict = {"T" + key: value for key, value in tutorial_dict.items()}
practical_dict = {"P" + key: value for key, value in practical_dict.items()}

all_dict = {}
all_dict.update(lecture_dict)
all_dict.update(tutorial_dict)
all_dict.update(practical_dict)


def select_slots(subject_list, RSUBS):
    selected_slots = []
    preselected_subjects = set()

    for course_code, slots in RSUBS.items():
        selected_slots.extend(slots)
        preselected_subjects.add(course_code)

    while True:
        for subject, slots in subject_list.items():
            if subject in preselected_subjects:
                continue

            if not slots:
                print(f"Error: No available slots for {subject}")
                return None

            sections = {}
            for slot in slots:
                section_name = slot['section']
                if section_name not in sections:
                    sections[section_name] = []
                sections[section_name].append(slot)

            chosen_section = random.choice(list(sections.keys()))

            selected_slots.extend(sections[chosen_section])

        if not check_conflict(selected_slots):
            return selected_slots
        else:

            selected_slots = [slot for slots in RSUBS.values() for slot in slots]


def check_conflict(selected_slots):
    slots = set()
    for slot in selected_slots:
        for day in slot['days'].split(', '):
            for hour in slot['hours'].split(', '):
                if (day, hour) in slots:
                    return True  # CONFLICT
                slots.add((day, hour))
    return False  # No conflict


def input_sub(dicts):
    num_entries = int(input("Enter the number of entries you want to add:"))

    for i in range(num_entries):
        key = input("Enter course name(eg : MATH F111): ")
        value = input("Enter section code(eg : L1 OR T5 etc): ")
        single_dict = {key: value}

        dicts.append(single_dict)

    return dicts


def making_rem_data(rdict, dictionaries):
    for i in dictionaries:
        for key in i:
            for s in all_dict:

                for t in all_dict[s][:]:

                    if t['course code'] == key and t['section'] == i[key]:
                        rdict[s].remove(t)

    return rdict


def making_fix_data(removed_subs, dictionary):
    slot_checking = []

    for s in dictionary:
        for y in s:
            for i in all_dict:
                for k in all_dict[i][:]:
                    if k['course code'] == y and k['section'] == s[y]:
                        slot_checking.append(k)

    print(slot_checking)

    if check_conflict(slot_checking):
        print("slots clashing")
        return
    else:
        for slot in slot_checking:
            slot_checking_new = []
            for k in all_dict:
                for t in all_dict[k][:]:
                    if t['course code'] == slot['course code'] and t['section'] == slot['section']:
                        slot_checking_new.append(t)

                        removed_subs[k] = slot_checking_new
    return removed_subs


new_dict = all_dict.copy()
rem_dict = all_dict.copy()

REMOVED_SUBS = {}
dictionaries = []
fix_dictionaries = []
print("CHOOSE THE UNAVAILABLE SLOTS")
input_sub(dictionaries)
making_rem_data(rem_dict, dictionaries)
print("CHOOSE THE FIXED SLOTS")
input_sub(fix_dictionaries)
making_fix_data(REMOVED_SUBS, fix_dictionaries)
selected_slots = select_slots(rem_dict, REMOVED_SUBS)

if selected_slots:
    for slot in selected_slots:
        print(
            f"Subject: {slot['course code']},section:{slot['section']}, Teacher: {slot['instructors']}, Day: {slot['days']}, Time: {slot['hours']}")
else:
    print("No valid schedule could be generated.")

days_map = {
    "M": "Mon", "T": "Tue", "W": "Wed", "Th": "Thu",
    "F": "Fri"
}

hours_map = {
    "1": "8-9 AM", "2": "9-10 AM", "3": "10-11 AM", "4": "11 AM-12 PM",
    "5": "12-1 PM", "6": "1-2 PM", "7": "2-3 PM", "8": "3-4 PM",
    "9": "4-5 PM", "10": "5-6 PM"
}

timetable = pd.DataFrame("", index=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"], columns=hours_map.values())

for slot in selected_slots:
    days = slot['days'].split(', ')
    hours = slot['hours'].split(', ')

    for day in days:
        full_day = days_map[day]
        for hour in hours:
            hour_label = hours_map[hour]
            content = f"{slot['course code']} ({slot['section']})"
            if timetable.at[full_day, hour_label] == "":
                timetable.at[full_day, hour_label] = content
            else:
                timetable.at[full_day, hour_label] += f"\n{content}"

fig, ax = plt.subplots(figsize=(15, 10))
ax.axis('tight')
ax.axis('off')

table = ax.table(cellText=timetable.values, rowLabels=timetable.index, colLabels=timetable.columns, cellLoc='center',
                 loc='center')

table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1.2, 1.2)

for (i, j), cell in table.get_celld().items():
    cell.set_edgecolor('black')
    cell.set_linewidth(0.5)

plt.title('Weekly Timetable', fontsize=16)
plt.show()
