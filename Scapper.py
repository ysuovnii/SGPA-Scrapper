import requests
from bs4 import BeautifulSoup
import re

def gen_roll(pre='24i', start=1001, end=1081):
    return [ f"{pre}{str(i).zfill(3)}" for i in range(start, end+1) ]


def get_sgpa(roll_number):  
    url = f'https://college.edu/results?roll={roll_number}'  

    try:
        response = requests.get(url, timeout=5)
        if response.status_code != 200:
            return None  

        soup = BeautifulSoup(response.content, 'html.parser')

        match = soup.find(string=re.compile('SGPA', re.IGNORECASE))
        if match:
            sgpa_td = match.find_parent('td')
            value_td = sgpa_td.find_next_sibling('td')
            if value_td:
                return value_td.get_text(strip=True)

    except Exception as e:
        print(f"Error for {roll_number}: {e}")
        return None

    return None


def save_file(filename='sgpa.txt'):
    rolls = gen_roll()
    with open(filename, 'w') as file:
        file.write('RollNumber -> SGPA\n')  
        for roll in rolls:
            sgpa = get_sgpa(roll)
            if sgpa:
                print(f"{roll} -> {sgpa}")
                file.write(f"{roll} -> {sgpa}\n")
            else:
                print(f"{roll} -> SGPA not found")
                file.write(f"{roll} -> Not Found\n")

save_file()
