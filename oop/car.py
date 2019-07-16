from vehicle import Vehicle

class Car(Vehicle):

    def brag(self):
        print("Look how cool my car is!")


car1 = Car()
car1.drive()

car1.add_warning("Warning")
print(car1.get_warnings())
