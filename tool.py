import requests
from bs4 import BeautifulSoup
import csv

branchList = ['c', 'i', 'b', 't', 'e', 'm', 'v']
sem = 2
filename = f'./Result/Sem_{sem}_Result.csv'

students = []

roll_ranges = [(sem*1000+1, sem*1000+99), (sem*1000+101, sem*1000+199)]

branch_map = {
    'c': 'Computer Science',
    'i': 'Information Technology',
    'b': 'Computer Science Business Studies',
    't': 'Electronics and Telecommunication',
    'e': 'Electronics and Instrumentation',
    'm': 'Mechanical',
    'v': 'Civil',
}

for branch in branchList:
    branchName = branch_map.get(branch, 'Unknown Branch')

    for start, end in roll_ranges:
        for roll in range(start, end):
            url = f"http://results.ietdavv.edu.in/DisplayStudentResult?rollno=24{branch}{roll}&typeOfStudent=Regular"

            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            nameTag = soup.find(text="Student Name")
            sgpaTag = soup.find(text='SGPA')
            rollNumberTag = soup.find(text='Roll Number')

            if nameTag and sgpaTag and rollNumberTag:
                name = nameTag.find_next('td').text.strip()
                sgpa = float(sgpaTag.find_next('td').text.strip())
                rollNumber = rollNumberTag.find_next('td').text.strip()

                students.append({
                    "branch": branchName,
                    "roll": rollNumber,
                    "name": name,
                    "sgpa": sgpa
                })

                print(f"Saved: {branchName} {rollNumber} {name} : {sgpa}")
            else:
                print(f"Result not found for roll: 24{branch}{roll}")

students_sorted = sorted(students, key=lambda x: x['sgpa'], reverse=True)

rank = 1
prev_sgpa = None
for i, student in enumerate(students_sorted):
    if prev_sgpa is None or student['sgpa'] < prev_sgpa:
        rank = i + 1
    student['rank'] = rank
    prev_sgpa = student['sgpa']

with open(filename, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Rank", "Branch", "Roll Number", "Name", "SGPA"])

    for s in students_sorted:
        writer.writerow([
            s['rank'],
            s['branch'],
            s['roll'],
            s['name'],
            s['sgpa']
        ])

print("CSV file created successfully!")
