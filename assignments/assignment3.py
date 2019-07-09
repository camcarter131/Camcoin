'''
1) Create a list of “person” dictionaries with a name, age and list of hobbies for each person. Fill in any data you want.

2) Use a list comprehension to convert this list of persons into a list of names (of the persons).

3) Use a list comprehension to check whether all persons are older than 20.

4) Copy the person list such that you can safely edit the name of the first person (without changing the original list).

5) Unpack the persons of the original list into different variables and output these variables.

'''

#1

people = [
    {"name": "Cam", "age": 25, "hobbies": ["ball", "ski", "bowl"]}, 
    {"name": "Joe", "age": 21, "hobbies": ["ball", "ski", "bowl"]}, 
    {"name": "Noah", "age": 22, "hobbies": ["jump", "snowboard", "box", "dive"]}, 
    {"name": "Kev", "age": 43, "hobbies": ["ball", "ski", "bowl", "birdwatch"]}, 
]

#2

names = [person["name"] for person in people]
print("Names:")
print(names)

#3
all_over_20 = all([person["age"] > 20 for person in people])
print("All over 20?:")
print(all_over_20)

#4
people_copy = people[:]
for i in range(len(people)):
    people_copy[i] = people[i].copy()

#5
p1, p2, p3, p4 = people
print(p1)
print(p2)
print(p3)
print(p4)
