import csv

from flask import render_template, request

from app import app

def load_students():
    # A utility function to load the students' grades from the csv file
    students = []
    with open('students.csv') as file:
        reader = csv.DictReader(file)
        for row in reader:
            students.append(row)
    return students

@app.route('/')
def index():
    # Load the students from the CSV file for the table
    students = load_students()
    # Return the index view with the list of students for display
    return render_template('index.html', students = students)

@app.route('/add_student', methods = ['GET', 'POST'])
def add_student():
    # Check if the form has been submitted (is a POST request)
    if request.method == 'POST':
        # Get data from the form and put in dictionary
        student = {}
        student['name'] = request.form.get('student_name')
        student['english_mark'] = request.form.get('english_mark')
        student['science_mark'] = request.form.get('science_mark')
        student['mathematics_mark'] = request.form.get('mathematics_mark')
        student['does_homework'] = request.form.get('does_homework') == 'on'
        student['stays_on_task'] = request.form.get('stays_on_task') == 'on'

        # Load the students from the CSV file and add the new student
        students = load_students()
        students.append(student)

        # Open up the csv file and overwrite the contents
        with open('students.csv', 'w', newline='') as file:
            fieldnames = ['name', 'english_mark', 'science_mark', 'mathematics_mark', 'does_homework', 'stays_on_task']
            writer = csv.DictWriter(file, fieldnames = fieldnames)
            writer.writeheader()
            writer.writerows(students)
        
        # Returns the view with a message that the student has been added
        return render_template('add_success.html', student = student)

    # When there is a GET request, the view with the form is returned
    return render_template('add_student.html')