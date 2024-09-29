import json
import random
import matplotlib.pyplot as plt
import pandas as pd
import sys






with open("C:/Users/bhoov/Downloads/timetable.json") as f:
    data = json.load(f)


lecture_dict = {}
tutorial_dict = {}
practical_dict = {}


N = int(input("Enter group number= "))
groups = {
    '2': ["MATH F111", "CHEM F111", "EEE F111", "CHEM F110", "PHY F111", "PHY F110", "ME F112"],
    '1': ["BIO F111", "BIO F110", "BITS F110", "BITS F111", "BITS F112", "CS F111", "MATH F111"]
}

total_subs= []
for h in groups:
    total_subs.extend(groups[h])

def check_naming(inp):
    if inp in total_subs:
        pass
    else:
        print("user input wrong")
        sys.exit()

for course_code in groups[str(N)]:
    if course_code in data['courses']:
        course_info = data['courses'][course_code]
        sections = course_info.get('sections', {})


        course_code_transformed = course_code.replace(" ", "_")
        lecture_dict[course_code_transformed] = []
        tutorial_dict[course_code_transformed] = []
        practical_dict[course_code_transformed] = []

        for section_name, section_info in sections.items():
            section_type = section_name[0]  # 'L', 'T', 'P' etc.
            instructors = ', '.join(section_info.get('instructor', []))
            for sched in section_info.get('schedule', []):
                section_info_obj = {
                    "course code": course_code,
                    "section": section_name,
                    "instructors": instructors,
                    "room": sched.get('room'),
                    "days": ', '.join(sched.get('days', [])),
                    "hours": ', '.join(map(str, sched.get('hours', [])))
                }


                if section_type == 'L':
                    lecture_dict[course_code_transformed].append(section_info_obj)
                elif section_type == 'T':
                    tutorial_dict[course_code_transformed].append(section_info_obj)
                elif section_type == 'P':
                    practical_dict[course_code_transformed].append(section_info_obj)


lecture_dict = {k: v for k, v in lecture_dict.items() if v}
tutorial_dict = {k: v for k, v in tutorial_dict.items() if v}
practical_dict = {k: v for k, v in practical_dict.items() if v}


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

        slot_combinations = set((day, hour) for day in slot['days'].split(', ') for hour in slot['hours'].split(', '))


        if not slots.isdisjoint(slot_combinations):
            return True  # Conflict found


        slots.update(slot_combinations)

    return False  # No conflict

def input_sub(dicts):
    num_entries = int(input("Enter the number of entries you want to add:"))

    for i in range(num_entries):
        key = input("Enter course name(eg : MATH F111): ").upper().strip()
        check_naming(key)
        value = input("Enter section code(eg : L1 OR T5 etc): ").upper().strip()
        single_dict = {key: value}

        dicts.append(single_dict)

    return dicts


def making_remaining_data(rdict, dictionaries):
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
remaining_dict = all_dict.copy()

REMOVED_SUBS = {}
dictionaries = []
fix_dictionaries = []
print("CHOOSE THE UNAVAILABLE SLOTS")
input_sub(dictionaries)
making_remaining_data(remaining_dict, dictionaries)

print("CHOOSE THE FIXED SLOTS")
input_sub(fix_dictionaries)


common_list = []
if dictionaries==[] and fix_dictionaries == []:
    pass
else:
    for item in dictionaries:
        if item in fix_dictionaries:
            common_list.append(item)
    print("subjects removed=",common_list)





making_fix_data(REMOVED_SUBS, fix_dictionaries)
selected_slots = select_slots(remaining_dict, REMOVED_SUBS)

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

timetable = pd.DataFrame("", index=["Mon", "Tue", "Wed", "Thu", "Fri"], columns=hours_map.values())

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



table = ax.table(cellText=timetable.values, rowLabels=timetable.index, colLabels=timetable.columns,
                 cellLoc='center',
                 loc='center')

table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1.2, 1.2)


for (i, j), cell in table.get_celld().items():
    cell.set_edgecolor('black')
    cell.set_linewidth(0.5)

plt.title('Weekly Timetable', fontsize=16)
plt.savefig("timetable.png")
