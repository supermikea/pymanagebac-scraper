# NOTE install it or put it in the same directory as the example.py
import mbapi

# first we make a mbapi object and insert all required information (optional: implicit wait of selenium)
mbapi = mbapi(mail="mail", password="password")

# first we login
mbapi.login()

# we get the schedule in a lists nested in a list
print(mbapi.get_schedule())

# we get the classes in a list
print(mbapi.get_classes())

# we are done with gathering information so we quit
mbapi.quit()