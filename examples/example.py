from mbapi import mbapi

mbapi = mbapi("YOUR_MAILl", "YOUR_PASSWORD", hide_window=True)
mbapi.login()
print("Successfully logged in!")

classes = mbapi.get_classes()

temp = []

for i in range(0, len(classes)):
    print(classes[i].name)
    temp.append(mbapi.get_grades(target=classes[i]))

for item in temp:
    print(f"\n\nclass: {item.name}\n\n")
    for i in item.grades:
        print(f"Name Assignment: {i.name}")
        print(f"Your Grade: {i.grade} / {i.max_grade}\n")

mbapi.quit()
