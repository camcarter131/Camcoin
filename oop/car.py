class Car:

    def __init__(self, starting_top_speed=100):
        self.top_speed = starting_top_speed
        self.warnings = []

    def __repr__(self):
        print("Printing...")
        return "Top speed: {}, warnings: {}".format(self.top_speed, len(self.warnings))

    def drive(self):
        print("I am driving but certainly not faster than {}".format(self.top_speed))

car1 = Car()
# car1.drive()
car1.warnings.append("New warning")
print(car1)
