name = input("Enter your name: ")
age = input("Enter your age: ")


def print_added_strings(a, b):
    added_strings = a + b
    print(added_strings)


def decades(age):
    decs = age // 10
    print("You have lived " + str(decs) + " decades")


print_added_strings(name, age)
decades(int(age))
