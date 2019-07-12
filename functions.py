def unlimited_arguments(*args, **kwargs):
        print (kwargs)
        for k, v in kwargs.items():
                print(k)
                print(v)


unlimited_arguments(1, 2, 3, 4, 5, 6, name="Cam", age=25)
# unlimited_arguments(*[1, 2, 3, 4, 5, 6])

# a = [1,2,3]
# print("Some text: {}, {}, {}".format(*a))