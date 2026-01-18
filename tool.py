import requests
from bs4 import BeautifulSoup
import csv
import time 

student_pass = []
student_fail = []

branch_list = ['c', 'i', 'b', 't', 'e', 'm', 'v']
sem = 1
roll_range = [(sem*1000+1, sem*1000+99), (sem*1001+101, sem*1000+199)]

branch_map = {
    'c': 'Computer Science',
    'i': 'Information Technology',
    'b': 'Computer Science Business Studies',
    't': 'Electronics and Telecommunication',
    'e': 'Electronics and Instrumentation',
    'm': 'Mechanical',
    'v': 'Civil',
}

def fetch(URL, branch):

    try:
        res = requests.get(URL, timeout=5)
        soup = BeautifulSoup(res.text, 'html.parser')

        nameTag = soup.find(string="Student Name")
        rollTag = soup.find(string="Roll Number")
        verdictTag = soup.find(string="Result")
        cgTag = soup.find(string="SGPA")

        if nameTag and rollTag and verdictTag and cgTag:
            name = nameTag.find_next('td').text.strip()
            roll = rollTag.find_next('td').text.strip()
            verdict = verdictTag.find_next('td').text.strip()
            cg = float(cgTag.find_next('td').text.strip())

            record = {
                "branch" : branch, 
                "name": name,
                "roll": roll,
                "verdict": verdict,
                "cg": cg
            }

            if verdict == "Fail":
                student_fail.append(record)
            else :
                student_pass.append(record)
            
            # print(record)

    except requests.exceptions.Timeout:
        print(f"Timeout: {URL}")

    except Exception as e:
        print(f"Error: {e}")


    
def generateURL():
    total = len(branch_list) * sum(end - start for start, end in roll_range)
    done = 0
    for branch in branch_list:
        branchName = branch_map.get(branch, 'Unknown Branch')
        for start, end in roll_range:
            for roll in range(start, end):
                url = f"https://results.ietdavv.edu.in/DisplayStudentResult?rollno=24{branch}{roll}&typeOfStudent=Regular"

                fetch(url, branchName)
                done += 1
                print(f"[{done}/{total}] fetched", end="\r")
                time.sleep(0.3)

def rank_students():
    all_students = student_pass + student_fail

    all_students.sort(
        key=lambda x: (x["verdict"] == "Fail", -x["cg"])
    )

    rank = 1
    prev_key = None  

    for idx, student in enumerate(all_students):
        current_key = (student["verdict"], student["cg"])

        if current_key != prev_key:
            rank = idx + 1

        student["rank"] = rank
        prev_key = current_key

    return all_students

def write_csv(all_students):
    with open(f"Sem_{sem}_Result.csv", "w", newline="") as f:
        fieldnames = ["rank", "branch", "name", "roll", "cg", "verdict"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        writer.writeheader()
        for s in all_students:
            writer.writerow(s)

if __name__ == "__main__":
    start_time = time.time()
    generateURL()
    print()

    all_students = rank_students()

    print(f"\nTotal students: {len(all_students)}")
    print(f"Pass: {len(student_pass)}")
    print(f"Fail: {len(student_fail)}")

    write_csv(all_students)

    print(f"\nExecution Time: {time.time() - start_time:.2f} seconds")

     

