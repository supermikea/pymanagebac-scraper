from pymanagebac import pymanagebac as mb

# we make the mbapi object, it should automatically find your subdomain if not you can add the subdomain parameter
# automatically runs in headless if you want to see the window add hidewindow=True as argument
mbapi = mb("EMAIL", "PASSWORD")


print("logging in...")

# be sure to run this instantly because well you first need to log in
mbapi.login()
print("Successfully logged in!")

print("getting classes...")
# we get all the classes that the student has. this is used to identify the ID of the class and use that as target for
# the get_grades method
classes = mbapi.get_classes()
print("got classes!")

temp = []

print("getting grades...")

# we get all the grades for all the classes of the student using our output of the get_classes method
for i in range(0, len(classes)):
    temp.append(mbapi.get_grades(target=classes[i]))

print("got grades! parsing output...")

# sometimes the teacher will submit a non-myp grade, in that case the grade is not a dictionary but in a list
# in this block code we use the output of the get_grades method to determine if the grade is a dictionary -> myp
# or something custom. after that we print the grade for that class including its name of class and the assignment name
for item in temp:
    print(f"\n\nclass: {item.name}")
    for i in item.grades:
        grade = i.grade
        max_grade = i.max_grade
        print(f"Name Assignment: {i.name}")

        if isinstance(i.grade, dict):
            keys = i.grade.keys()
            if "A" in keys:
                print(f"criteria A: {i.grade.get('A')}")
            if "B" in keys:
                print(f"criteria B: {i.grade.get('B')}")
            if "C" in keys:
                print(f"criteria C: {i.grade.get('C')}")
            if "D" in keys:
                print(f"criteria D: {i.grade.get('D')}")
        else:
            print(f"Your Grade: {grade} out of {max_grade}")

# you NEED to call this function for the webdriver to quit
mbapi.quit()
