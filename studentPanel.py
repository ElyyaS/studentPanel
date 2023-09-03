import weakref
import pandas
import csv
import sys
import ast

class student:

    students = []

    # ******************************************************* __init__ function *******************************************************

    # Create student object

    def __init__(self,
            studentCode,
            firstName,
            lastName, 
            phoneNumber,
            numberOfCourses,
            courses = None,
            numberOfUnits = None,
            average = None
            ):
        self.__class__.students.append(weakref.proxy(self))
        self.studentCode = studentCode
        self.firstName = firstName
        self.lastName = lastName
        self.phoneNumber = phoneNumber
        self.numberOfCourses = numberOfCourses
        self.courses = courses
        self.numberOfUnits = numberOfUnits
        self.average = average
    
    # ****************************************************** getCourses function *******************************************************

    # Taking courses in the form of course name , number of units , grades

    def getCourses(studentCode):

        courses = []
        
        print("*********************************************\n" +
            "Please enter the name of the courses along with the number of units and their grades\n" +
            "as in the example below (separate with commas):\n" +
            "name of course , number of units , grade")
        
        for item in student.students:
            if item.studentCode == studentCode:
                numberOfCourses = item.numberOfCourses

        for i in range(1, int(numberOfCourses) + 1):
            # Retrieving data separated by commas
            courses.append(list(map(str, input(f'{i}. ').replace(' ', '').split(','))))

        item.courses = courses
        student.calcNumberofUnitsAndAverage(studentCode)

    # ********************************************** calcNumberofUnitsAndAverage function **********************************************

    # Calculate the number of units and grade point average

    def calcNumberofUnitsAndAverage(studentCode):
        average = 0
        numberOfUnits = 0

        for item in student.students:
            if item.studentCode == studentCode:
                # sum number of units
                numberOfCourses = item.numberOfCourses
                courses = item.courses
       
        for i in range(int(numberOfCourses)):
            # Calculation of grade point average
            average += int(courses[i][1]) * float(courses[i][2])
            numberOfUnits += int(courses[i][1])

        average /= numberOfUnits
        
        item.numberOfUnits = numberOfUnits

        # Storage of grade point average with two decimal places
        item.average = "{0:.2f}".format(average)
        
        # Apply new changes to the file
        student.refreshData('write')

        # Show number of Units and average
        print(f'Your number of units: {item.numberOfUnits}\nYour grade point average : {item.average}')
    
    # **************************************************** courseManagement function ****************************************************

    # Edit the number of courses (delete and add courses)

    def courseManagement(studentCode = None):

        # Flag variable to specify where the user called the function
        deleteAndAddFlag = False

        if studentCode == None:
            deleteAndAddFlag = True
            studentCode = input("Enter your student Code: ")
            
        for item in student.students:
            if item.studentCode == studentCode:

                if deleteAndAddFlag:
                    # Review number of courses
                    print(f"number of courses: {item.numberOfCourses}\n1. edit\n2. next")
                    select = int(input())

                    if select == 1:
                        # Edit number of courses
                        item.numberOfCourses = input(f"Enter your number of courses again: ")
                    elif select == 2:
                        student.finalMenu()
                    else:
                        print("The desired command was not found")
                        student.continueMenu()

                # Add new courses 
                if int(item.numberOfCourses) > len(item.courses):
                    print("*********************************************\n" +
                        "According to editing the number of courses, " +
                        f"you should add {int(item.numberOfCourses) - len(item.courses)} more course(s)\n"
                        "Please enter the name of the course(s) along with the number of units and their grades\n" +
                        "as in the example below (separate with commas):\n" +
                        "name of course , number of units , grade")
                    
                    item.numberOfUnits = int(item.numberOfUnits)
                    item.average = float(item.average)
                    item.average *= item.numberOfUnits

                    for i in range(len(item.courses) + 1, int(item.numberOfCourses) + 1):
                        item.courses.append(list(map(str, input(f'{i}. ').replace(' ', '').split(','))))
                        item.average += int(item.courses[len(item.courses) - 1][1]) * int(item.courses[len(item.courses) - 1][2])
                        item.numberOfUnits += int(item.courses[len(item.courses) - 1][1])

                    item.average /= item.numberOfUnits
                    item.average = "{0:.2f}".format(item.average)

                    print("*********************************************\n" +
                        "Your desired course(s) have been successfully registered")

                # Delete some courses
                elif int(item.numberOfCourses) < len(item.courses):

                    print("*********************************************\n" +
                        "Regarding editing the number of course(s), " +
                        f"you must delete {len(item.courses) - int(item.numberOfCourses)} course(s)\n" +
                        "Please enter the number of course(s) you want to delete\n" +
                        "Separate the course number(s) with commas (for example: 1 or 2 , 3)")
                    
                    for i in range(1, len(item.courses) + 1):
                        print(f"{i}. {item.courses[i - 1][0]} , {item.courses[i - 1][1]} , {item.courses[i - 1][2]}")

                    deleteIndex = list(map(int, input().replace(' ', '').split(',')))
                    item.average = float(item.average)
                    item.numberOfUnits = int(item.numberOfUnits)
                    item.average *= item.numberOfUnits
                    temp = 0

                    for index in deleteIndex:
                        temp += 1
                        item.average -= int(item.courses[index - temp][1]) * int(item.courses[index - temp][2])
                        item.numberOfUnits -= int(item.courses[index - temp][1])
                        item.courses.pop(index - temp)

                    item.average /= item.numberOfUnits
                    item.average = "{0:.2f}".format(item.average)

                    print(f'*********************************************\n' +
                        'The desired course(s) were successfully deleted')
                    
                # Show courses after making changes
                print("Your courses now:")
                student.showCourses(studentCode)
                # Display the number of units and grade point average after making changes
                print(f'Your number of units: {item.numberOfUnits}\nYour grade point average : {item.average}')
                student.refreshData('write')

                if deleteAndAddFlag:
                    student.finalMenu()
        
    # ****************************************************** refreshData function *******************************************************
    
    # Read and write to the file     

    def refreshData(status = None):

        if status == 'read':
            file = open('studentsFile.csv', newline='')
            reader = csv.reader(file)
            counter = -1
            for item in reader:

                counter += 1
                # Avoid reading the row of titles
                if counter == 0:
                    continue
                
                studentCode = item[0]
                # Reading student information from the file
                globals()[studentCode] = student(studentCode,
                                                item[1],
                                                item[2],
                                                item[3],
                                                item[4], 
                                                ast.literal_eval(item[5]),
                                                item[6],
                                                item[7])

        if status == 'write':
            file = open('studentsFile.csv', 'w', newline='', encoding='UTF8')
            writer = csv.writer(file)

            # Writing rows of titles in the file
            titleRow = 'studentCode,firstName,lastName,phoneNumber,numberOfCourses,courses,numberOfUnits,average'
            writer.writerow(titleRow.split(','))

            for item in student.students:
                # Writing student information in the file        
                data = [item.studentCode,
                        item.firstName,
                        item.lastName,
                        item.phoneNumber,
                        item.numberOfCourses,
                        item.courses,
                        item.numberOfUnits,
                        item.average]
                writer.writerow(data)

        file.close()

    # ******************************************************** mainMenu function ********************************************************    

    # Main menu

    def mainMenu():

        print("*********************************************\n" +
            "Welcome to the student panel:\n" +
            "1. Register student information\n" +
            "2. search student information\n"
            "3. Edit student information\n" +
            "4. Remove a student\n" +
            "5. remove academic probation students\n" +
            "6. Delete and add courses\n"
            "7. Class list \n" +
            "8. Show class program\n"
            "9. Show student average\n" +
            "10. Show class average\n" +
            "11. Refresh data\n"
            "0. Exit")

        select = int(input())
        
        while True:
            match select:
                case 1:
                    # Register a new student
                    student.register()
                case 2:
                    # Search a student with student code
                    student.searchStudent()
                case 3:
                    # Edit student information (studentCode, firstName, lastName, phoneNumber, numberOfCourses, courses(number of units, average))
                    student.edit()
                case 4:
                    # Delete a specific student with a student code
                    student.remove()
                case 5:
                    # Removing all academic probation students from the class
                    student.removeProbationStudents()
                case 6:
                    # Editing the number of courses along with course name, number of units and grade
                    student.courseManagement()
                case 7:
                    # Show the class list with all the details of the students
                    student.classList()
                case 8:
                    # Showing the courses and the number of units and grades of a student
                    student.showCourses()
                case 9:
                    # Show the grade point average of a student
                    student.showStudentAverage()
                case 10:
                    # Showing the grade point average of students in a class
                    student.showClassAverage()
                case 11:
                    # Reading information from the file and transferring new information to the file
                    student.refreshData('read')
                    student.mainMenu()
                case 0:
                    # Exit the program
                    sys.exit("Good luck")
                case _:
                    print("The desired command was not found")
                    student.mainMenu()

    # ******************************************************* finalMenu function ******************************************************** 
    
    # Display the final menu after doing a task to return to the main menu or exit the program  

    def finalMenu():
        print("*********************************************\n" +
            "1. Return to the main menu\n2. Exit")
        
        select = int(input())

        while True:
            match select:
                case 1:
                    student.mainMenu()
                    break
                case 2:
                    sys.exit("Good luck")
                case _:
                    print("The desired command was not found")

    # ****************************************************** continueMenu function ****************************************************** 
    
    # Show the continue menu to continue a task or return to the main menu    

    def continueMenu():

        print("*********************************************\n" +
            "1. continue\n2. Return to the main menu")
        
        select = int(input())

        while True:
            match select:
                case 1:
                    sys._getframe().f_back.f_code.co_name
                    break
                case 2:
                    student.mainMenu()
                case _:
                    print("The desired command was not found")
                    student.continueMenu()

    # ****************************************************** registerMenu function ******************************************************  
     
    #   Register menu for ...

    def registerMenu(studentCode):
        print("*********************************************\n" +
            "1. Final registration\n" + 
            "2. Review the entered information\n" +
            "3. Edit entered information\n" +
            "4. Cancel registration")
        
        select = int(input())

        while True:
            match select:
                case 1:
                    # Confirm the entered information
                    print("Information has been successfully registered")
                    student.refreshData('write')
                    student.finalMenu()
                case 2:
                    # Review the entered information
                    student.searchStudent(studentCode)
                case 3:
                    # Edit entered information (studentCode, firstName, lastName, phoneNumber, numberOfCourses, courses(number of units, average))
                    student.edit(studentCode)
                case 4:
                    # Cancel registration and delete entered information
                    student.cancel()
                case _:
                    print("The desired command was not found")
                    student.continueMenu()
    
    # ********************************************************* register function ********************************************************  
    
    # register information   

    def register():
        print("*********************************************\n" +
            "Please enter the requested information: ")
        
        studentCode = input('Enter your student code: ')
        
        studentCode = student.controlStudentCode(studentCode)

        # getting information
        globals()[studentCode] = student(studentCode,
        input("Enter your first name: "),
        input("Enter your last name: "),
        input("Enter your phone number: "),
        input("Enter number of your courses: "))
        student.getCourses(studentCode)
        # Transferring new information to the file
        student.refreshData('write')
        # Register menu to confirm, review, edit or delete entered information
        student.registerMenu(studentCode)
    
    # ***************************************************** controlStudentCode function ***************************************************    

    # control student code
    def controlStudentCode(studentCode):

        while True:
            studentCodeFlag = True

            for item in student.students:
                # Avoid entering duplicate student code
                if item.studentCode == studentCode:
                    studentCodeFlag = False
                    print(f'Student code {studentCode} is duplicate')

            if studentCodeFlag:
                break
            else:
                # Getting the student code again if the student code is duplicated in a loop
                studentCode = input('Enter another student code: ')

        return studentCode

    # ********************************************************** cancel function **********************************************************    

    # Cancel registration and delete entered information

    def cancel():
        student.students.pop()
        print("Your registration has been canceled")
        student.finalMenu()
    
    # ****************************************************** searchStudent function ******************************************************    

    # Retrieving the complete information of a student by entering the student code

    def searchStudent(studentCode = None):
        flag = True

        if studentCode == None:
            flag = False
            studentCode = input("*********************************************\n" +
                                "Enter your student Code: ")
        for item in student.students:
            if item.studentCode == studentCode:
                print("*********************************************\n" +
                    "Information: ")

                print(f"Student code: {item.studentCode}")
                print(f"First name: {item.firstName}")
                print(f"Last name: {item.lastName}")
                print(f"Phone number: {item.phoneNumber}")
                print(f"Number of courses: {item.numberOfCourses}")

                # Revision of complete course information along with the number of units and grade point average in the table
                print('Courses:\n')
                student.showCourses(studentCode)
                print()

                print(f"Number of units: {item.numberOfUnits}")
                print(f"Average: {item.average}")

                if flag:
                    student.registerMenu(studentCode)
                else:
                    student.finalMenu()

        print("The desired student code was not found")
        student.continueMenu()

    # *********************************************************** edit function ***********************************************************

    # Edit the complete information of a student by entering the student code

    def edit(studentCode = None):
        # Flag variable to indicate where the user called the function
        menuFlag = True
        # Flag variable to control data changes
        editFlag = False

        print("*********************************************\n" +
            "Please review the information and edit it if necessary: ")

        if studentCode == None:
            menuFlag = False
            studentCode = input("Enter your student Code: ")

        for item in student.students:

            if item.studentCode == studentCode:
                # Helper variable definition for possible editing of student code
                studentCodeTemp = studentCode
                # Review student code
                print(f"Student code: {item.studentCode}\n1. edit\n2. next")
                select = int(input())

                if select == 1:
                    editFlag = True
                    # Use helper variable to edit the student code and final edit the student code after editing other information
                    studentCodeTemp = input(f"Enter your student code again: ")
                    studentCodeTemp = student.controlStudentCode(studentCodeTemp)
                    
                elif select == 2:
                    pass
                else:
                    print("The desired command was not found")
                    student.continueMenu()

                # Review first name
                print(f"First name: {item.firstName}\n1. edit\n2. next")

                select = int(input())

                if select == 1:
                    editFlag = True
                    # Edit first name
                    item.firstName = input(f"Enter your first name again: ")
                elif select == 2:
                    pass
                else:
                    print("The desired command was not found")
                    student.continueMenu()

                # Review last name
                print(f"Last name: {item.lastName}\n1. edit\n2. next")

                select = int(input())

                if select == 1:
                    editFlag = True
                    # Edit last name
                    item.lastName = input(f"Enter your last name again: ")
                elif select == 2:
                    pass
                else:
                    print("The desired command was not found")
                    student.continueMenu()

                # Review phone number
                print(f"Phone number: {item.phoneNumber}\n1. edit\n2. next")

                select = int(input())

                if select == 1:
                    editFlag = True
                    # Edit phone number
                    item.phoneNumber = input(f"Enter your Phone number again: ")
                elif select == 2:
                    pass
                else:
                    print("The desired command was not found")
                    student.continueMenu()

                # Review number of courses
                print(f"number of courses: {item.numberOfCourses}\n1. edit\n2. next")

                select = int(input())

                if select == 1:
                    editFlag = True
                    # Edit number of course
                    item.numberOfCourses = input(f"Enter your number of courses again: ")
                    # Edit courses after editing the number of courses (delete or add courses)
                    student.courseManagement(studentCode)
                elif select == 2:
                    pass
                else:
                    print("The desired command was not found")
                    student.continueMenu()
                
                print("*********************************************\ncourses:")
                # Review the name of the number of units and the grade of courses for possible editing
                student.showCourses(studentCode)
                print("1. edit\n2. next")

                select = int(input())

                if select == 1:
                    editFlag = True
                    # Edit the name of the number of units and the grade of courses
                    student.editCourses(studentCode)
                elif select == 2:
                    pass
                else:
                    print("The desired command was not found")
                    student.continueMenu()

                # Edit student code after finishing editing the information
                item.studentCode = studentCodeTemp

                if editFlag:
                    # Transfer edited information to file
                    student.refreshData('write')
                    # Announcing the success of the changes
                    print("*********************************************\n" +
                        "Editing was done successfully")
                else:
                    # Declaration of not changing the information
                    print("*********************************************\n" +
                        "The information did not change")
                
                if not menuFlag:
                    student.finalMenu()
                    # Login to the menu register for the user who has edited information from the main menu
                else:
                    # Login to the register menu for the user who edited the information from the register menu
                    student.registerMenu(studentCode)


        print("The desired student code was not found")
        student.continueMenu()

    # ******************************************************* editCourses function ******************************************************* 
    
    #Edit the name of the number of units and the grade of courses    

    def editCourses(studentCode = None):
        if studentCode == None:
            studentCode = input("Enter your student Code: ")

        print("*********************************************\n" +
            "Please enter the number of course(s) you want to edit,\n" +
            "their name, number of unit and grade")
        
        print("Please enter the number of the course(s) you want to edit\n" +
            "Separate the course number(s) with commas (for example: 1 or 2 , 3)")
        
        print()

        # Revision of complete course information along with the number of units and grade point average in the table
        student.showCourses(studentCode)
        print()

        for item in student.students:
            if item.studentCode == studentCode:        
                editItems = list(map(int, input().replace(' ', '').split(',')))

                for index in editItems:

                    # Review name of course
                    select = int(input(f'name of course: {item.courses[index - 1][0]}\n1. edit\n2. next\n'))
                    if select == 1:
                        # Edit name of course
                        item.courses[index - 1][0] = input("Enter the name of course again: ")
                    elif select == 2:
                        pass
                    else:
                        student.continueMenu()

                    # Review of the number of course units
                    select = int(input(f'number of unit: {item.courses[index - 1][1]}\n1. edit\n2. next\n'))
                    if select == 1:
                        # Edit the number of course units
                        item.courses[index - 1][1] = input("Enter the number of unit again: ")
                    elif select == 2:
                        pass
                    else:
                        student.continueMenu()

                    # Review of course grade
                    select = int(input(f'grade: {item.courses[index - 1][2]}\n1. edit\n2. next\n'))
                    if select == 1:
                        # Edit course grade
                        item.courses[index - 1][2] = input("Enter the grade again: ")
                    elif select == 2:
                        pass
                    else:
                        student.continueMenu()

        print("*********************************************")
        student.showCourses(studentCode)
        student.calcNumberofUnitsAndAverage(studentCode)

    # ******************************************************** showCourses function ********************************************************

    # Display the full details of the courses in the table along with the number of units and the student's grade point average

    def showCourses(studentCode = None):
        mainMenuFlag = False

        if studentCode == None:
            mainMenuFlag = True
            studentCode = input("Enter your student Code: ")

        for item in student.students:
            if item.studentCode == studentCode:
                data = {
                        "row": [],
                        "courseName": [],
                        "numberOfUnit": [],
                        "grade": []
                        }
                counter = 0

                for item in item.courses:
                    counter += 1
                    data["row"].append(counter)
                    data["courseName"].append(item[0])
                    data["numberOfUnit"].append(item[1])
                    data["grade"].append(item[2])

                df = pandas.DataFrame(data)
                        
                print(df)

        if mainMenuFlag:
            student.finalMenu()

    # ********************************************************** remove function **********************************************************

    # Removing a student based on student code

    def remove(studentCode = None):
        
        if studentCode == None:
            studentCode = input("*********************************************\n" + 
                                "Enter your student Code: ")
        counter = 0

        for item in student.students:
            
            if item.studentCode == studentCode:
                select = int(input(f'Do you mean {item.firstName} {item.lastName} with student code {item.studentCode} ?\n' +
                                '1. Yes\n2. No\n'))
                if select == 1:
                    select = int(input("Are you sure?\n1. Yes\n2. No\n"))
                    if select == 1:
                        # Delete the student from the program list
                        student.students.pop(counter)
                        # Apply new changes to the file
                        student.refreshData('write')
                        # Announcing the successful removal of the student
                        print(f"Student {item.firstName} {item.lastName} with student code {studentCode} was successfully removed")
                    elif select == 2:
                        student.continueMenu()
                    else:
                        print("The desired command was not found")
                        student.continueMenu()

                elif select == 2:
                    student.remove()

                else:
                    print("The desired command was not found")
                    student.finalMenu()

                student.finalMenu()
            counter += 1

        print("The desired student code was not found")
        student.continueMenu()

    # ************************************************* removeProbationStudents function *************************************************

    # Removal of academically probation students from the class

    def removeProbationStudents():
        counter = 0
        probationItmes = []

        for item in student.students:
            # Find academic probation students
            if float(item.average) < 12 and item.average != 'average':
                probationItmes.append(counter)
            counter += 1

        if len(probationItmes) == 0:
            print("*********************************************\n" +
                "There are no students on academic probation in the class")
        else:
            # Registering the information of academic probation for notification of deletion
            probationStudents = [item for i, item in enumerate(student.students) if i in probationItmes]
            # Delete academic probation students
            student.students = [item for i, item in enumerate(student.students) if i not in probationItmes]  

            for item in probationStudents:
                # Announcing the removal of a student
                print("*********************************************\n" +
                    f"Student {item.firstName} {item.lastName} with student code {item.studentCode} " +
                    "was removed due to academic probation")

        # Apply new changes to the file
        student.refreshData('write')
        
        # Show new class list
        print("*********************************************\nNew list:")
        student.classList()

    # ******************************************************** classList function ********************************************************

    # Show class list with full details

    def classList():

        data = {"row": [],
            "studentCode": [],
            "firstName": [],
            "lastName": [],
            "phoneNumber": [],
            "numberOfCourses": [],
            "courses": [],
            "numberOfUnits": [],
            "average": []}

        for item in student.students:
            data["row"].append(student.students.index(item) + 1)
            data["studentCode"].append(item.studentCode)
            data["firstName"].append(item.firstName)
            data["lastName"].append(item.lastName)
            data["phoneNumber"].append(item.phoneNumber)
            data["numberOfCourses"].append(item.numberOfCourses)
            data["courses"].append(item.courses)
            data["numberOfUnits"].append(item.numberOfUnits)
            data["average"].append(item.average)

        df = pandas.DataFrame(data)
        print("*********************************************")

        # Ignore the courses column to display in the table
        if len(student.students) != 0:
            print(df.loc[:, df.columns != 'courses'])
        else:
            print("The class is empty")
        student.finalMenu()
    
    # *************************************************** showStudentAverage function **************************************************** 
    
    # Display the number of courses, the number of units and the student's grade point average    
    
    def showStudentAverage():
        
        studentCode = input("*********************************************\n" +
                            "Enter your student Code: ")

        for item in student.students:
            if item.studentCode == studentCode:
                print(f"Your number of courses: {item.numberOfCourses}\n" +
                    f"Your number of Units: {item.numberOfUnits}\n" +
                    f"Your grade point average: {item.average}")
                student.finalMenu()

        print("The desired student code was not found")
        student.continueMenu()

    # ***************************************************** showClassAverage function ****************************************************    

    # Calculation of the grade point average of the class

    def showClassAverage():

        classAverage = 0

        if len(student.students) > 0:
            for item in student.students:
                classAverage += float(item.average)
            classAverage /= len(student.students)
            classAverage = "{0:.2f}".format(classAverage)

        print("*********************************************\n" +
            f"numbr of students: {len(student.students)}\nclass average: {classAverage}")
        
        student.finalMenu()


# Retrieving basic information from the file
student.refreshData('read')
# Display the main menu and start the program
student.mainMenu()