# SGPA-Scrapper 

This Python script scrapes SGPA data for a range of student roll numbers from a publicly available college result website.

# Features
- Generates a list of roll numbers
- Fetches SGPA from each student's result page
- Saves data in `sgpa.txt`

# Modify for Your Own Use
- You can change the roll number prefix from '24i' to something else.
- Adjust the start and end roll numbers.
- If your college website is different, change the url and parsing logic in get_sgpa().
