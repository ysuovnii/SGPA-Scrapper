import requests
from bs4 import BeautifulSoup

branchList = ['b', 'c', 'e', 'i', 'm', 't', 'v']
sem = 2
filename = f'Sem_{sem}_Result.txt'

students = []

roll_ranges = [(sem*1000+1, sem*1000+99), (sem*1000+101, sem*1000+199)]

for branch in branchList:
    for start, end in roll_ranges:
        for roll in range(start, end):
            url = f"http://results.ietdavv.edu.in/DisplayStudentResult?rollno=24{branch}{roll}&typeOfStudent=Regular"

            response = requests.get(url)
            data = response.text
            soup = BeautifulSoup(data, 'html.parser')

            nameTag = soup.find(text="Student Name")
            sgpaTag = soup.find(text='SGPA')
            rollNumberTag = soup.find(text='Roll Number')

            if nameTag and sgpaTag and rollNumberTag:
                name = nameTag.find_next('td').text.strip()
                sgpa = float(sgpaTag.find_next('td').text.strip())
                rollNumber = rollNumberTag.find_next('td').text.strip()
                students.append({"roll_name": f"{rollNumber} {name}", "sgpa": sgpa})
                print(f"Saved: {rollNumber} {name} : {sgpa}")
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

with open(filename, "w") as f:
    for student in students_sorted:
        f.write(f"{student['rank']}. {student['roll_name']} : {student['sgpa']}\n")

print("File updated with sorted ranks!")
