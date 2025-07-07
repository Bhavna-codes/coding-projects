# Import the regular expression module 're'.
import re


# Define a class called 'Car' to represent car objects.
class Car:
    # 2.1.1. Initialize the 'Car' class with various attributes, providing default values.
    def __init__(self, name, car_code="MB123456", car_name="Suzuki", car_capacity=5, car_horsepower=150,
                 car_weight=1075,
                 car_type="FWD", car_prob_lic="true", licence_type="FULL"):
        self.name = name  # Assign the 'name' attribute.

        # Validate and set the 'car_code' attribute using a regular expression.
        if not re.match(r'^[A-Z]{2}\d{6}$', car_code):
            raise ValueError(
                "Invalid car_no format. It must be two uppercase letters followed by six digits (e.g., MB123456).")
        self.car_code = car_code

        self.car_name = car_name  # Assign the 'car_name' attribute.
        self.car_capacity = car_capacity  # Assign the 'car_capacity' attribute.
        self.car_horsepower = car_horsepower  # Assign the 'car_horsepower' attribute.
        self.car_weight = car_weight  # Assign the 'car_weight' attribute.

        # Convert 'car_type' to lowercase and assign it.
        car_type = car_type.lower()
        # Check if 'car_type' is valid (must be 'fwd', 'rwd', or 'awd').
        if car_type not in ["fwd", "rwd", "awd"]:
            raise ValueError("Invalid car_type. Must be one of 'FWD', 'RWD', or 'AWD' (case-insensitive).")
        self.car_type = car_type

        # Convert 'car_prob_lic' to lowercase and assign it.
        car_prob_lic = car_prob_lic.lower()
        # Check if 'car_prob_lic' is valid (must be 'true' or 'false').
        if car_prob_lic not in ["true", "false"]:
            raise ValueError("Invalid car_prob_lic. Must be 'true' or 'false' (case-insensitive).")
        self.car_prob_lic = car_prob_lic

        # Convert 'licence_type' to uppercase for consistency and assign it.
        licence_type = licence_type.upper()
        # Check if 'licence_type' is valid ('L', 'P', or 'FULL').
        if licence_type not in ["L", "P", "FULL"]:
            raise ValueError(
                "Invalid licence_type. Must be one of 'L' (Learner Licence), 'P' (Probationary Licence), or 'FULL' (Full Licence).")
        self.licence_type = licence_type

    # 2.1.2. Define a method to return a formatted string of car details.
    def __str__(self):
        car_details = "code: " + self.car_code + ", name: " + self.car_name + ", capacity: " + str(self.car_capacity) + \
                      ", horsepower: " + str(self.car_horsepower) + ", weight: " + str(self.car_weight) + \
                      ", type: " + self.car_type
        return car_details

    # Define a method to calculate and return the power-to-mass ratio.
    def power_to_mass_ratio(self):
        return (self.car_horsepower / self.car_weight) * 1000

    # 2.1.3. Define a method to check if the vehicle is a prohibited vehicle for probationary licence drivers.
    def probationary_licence_prohibited_vehicle(self):
        # Check if the licence_type is "P" (Probationary Licence)
        if self.licence_type == "P":
            return True
        ratio = self.power_to_mass_ratio()
        # Check if the power-to-mass ratio exceeds 130.
        return ratio > 130

    #2.1.4. Define a method to check if the provided car code matches the car's code.
    def found_matching_car(self, test_code):
        return self.car_code == test_code

    #2.1.5. Define a method to get the car's type.
    def get_car_type(self):
        return self.car_type


# Test for checking if the vehicle is prohibited for probationary licence drivers.
car1 = Car(name="Toyota", car_horsepower=150, car_weight=1075)
test_prohibited = car1.probationary_licence_prohibited_vehicle()
print("Is the vehicle prohibited for probationary licence drivers?", test_prohibited)

# Test for finding a matching car code.
car2 = Car(name="Hyundai", car_code="MB123457", car_horsepower=150, car_weight=1075)
test_code = "MB123457"
found_match = car2.found_matching_car(test_code)
print("Vehicle currently with us?", found_match)

# Running tests for probationary licence and licence type.
car1 = Car(name="Toyota", licence_type="L", car_horsepower=100, car_weight=800)
test_prohibited1 = car1.probationary_licence_prohibited_vehicle()  # Should be False

car2 = Car(name="Honda", licence_type="P", car_horsepower=150, car_weight=1000)
test_prohibited2 = car2.probationary_licence_prohibited_vehicle()  # Should be True

car3 = Car(name="Ford", licence_type="FULL", car_horsepower=200, car_weight=1500)
test_prohibited3 = car3.probationary_licence_prohibited_vehicle()  # Should be True

car4 = Car(name="Chevrolet", licence_type="FULL", car_horsepower=120, car_weight=1100)
test_prohibited4 = car4.probationary_licence_prohibited_vehicle()  # Should be False

# Print the results
print("Test 1: Is the vehicle prohibited for Learner Licence drivers?", test_prohibited1)
print("Test 2: Is the vehicle prohibited for Probationary Licence drivers?", test_prohibited2)
print("Test 3: Is the vehicle prohibited for Full Licence drivers?", test_prohibited3)
print("Test 4: Is the vehicle prohibited for Full Licence drivers?", test_prohibited4)
