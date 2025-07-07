# Import the Retailer class from retailer module
from retailer import Retailer

# Import re library for necessary functions
import re
import random

# Initialize the CarRetailer child class
class CarRetailer(Retailer):
    # 2.3.1. Construct objects
    def __init__(self, retailer_id, retailer_name, retailer_address, carretailer_business_hours, carretailer_stock=None):
        # Call the constructor of the parent class (Retailer) to initialize retailer_id and retailer_name
        super().__init__(retailer_id, retailer_name)

        if not re.match(r'^[A-Za-z0-9\s,]+,\s*[A-Za-z]+\s+\d{4}$', retailer_address):
            raise ValueError(
                "Invalid retailer_address format. It must follow the format 'street address, state postcode' (e.g., '123 Main St, CA 1234').")
        self.retailer_address = retailer_address

        if not (6.0 <= carretailer_business_hours[0] <= 23.0) or not (6.0 <= carretailer_business_hours[1] <= 23.0):
            raise ValueError("Invalid business hours. Business hours must be within the range of 6:00 AM to 11:00 PM.")
        self.carretailer_business_hours = carretailer_business_hours

        self.carretailer_stock = carretailer_stock if carretailer_stock is not None else []

    # 2.3.2. Return the car retailer details
    def __str__(self):
        # Create a string representation using the format of get_car_retailer_info
        ret_det = f"{self.retailer_id}, {self.retailer_name}, {self.retailer_address}, {self.carretailer_business_hours[0]} - {self.carretailer_business_hours[1]}, {', '.join(self.carretailer_stock)}"
        return ret_det

    # 2.3.3. Load current stock from stock.txt file
    def load_current_stock(self):
        try:
            with open("stock.txt", "r") as file:
                self.carretailer_stock = [line.strip() for line in file]
        except FileNotFoundError:
            print("stock.txt file not found. Unable to load current stock.")

    # 2.3.4. Check if the car retailer is operating based on current hour
    def is_operating(self, cur_hour):
        start_hour, end_hour = self.carretailer_business_hours
        return start_hour <= cur_hour <= end_hour

    # 2.3.5. Get information of all available cars currently in stock

    def get_all_stock(self):
        # Sort the car retailer stock by retailer id
        sorted_stock = sorted(self.carretailer_stock, key=lambda car: car.split(',')[0])

        return sorted_stock

    #2.3.6. Postcode difference
    def get_postcode_distance(self, postcode):
        # Extract the postcode from the car retailer's address using a regular expression
        car_postcode_match = re.search(r'\d{4}$', self.retailer_address)
        if car_postcode_match:
            car_postcode = int(car_postcode_match.group())
            # Calculate and return the absolute difference between the postcodes
            return abs(car_postcode - postcode)
        else:
            # Return None or raise an exception if the postcode cannot be extracted
            return None

 # 2.3.7. Remove a car from the current stock

    def remove_from_stock(self, car_code):
        # Check if the car code is in the current stock
        if car_code in self.carretailer_stock:
            # Remove the car code from the stock
            self.carretailer_stock.remove(car_code)

            # Update the stock.txt file to reflect the change
            try:
                with open("stock.txt", "w") as file:
                    file.write("\n".join(self.carretailer_stock))
            except FileNotFoundError:
                # Handle the case where the file is not found
                print("stock.txt file not found. Unable to update stock.")
                return False

            return True  # Successful removal
        else:
            return False  # Car code not found in stock

 # 2.3.8. Add a car to the current stock
    def add_to_stock(self, car_code):
        # Check if the car code is already in the current stock
        if car_code in self.carretailer_stock:
            return False  # Car code already exists in stock, no need to add it again
        else:
            # Add the car code to the stock
            self.carretailer_stock.append(car_code)

            # Update the stock.txt file to reflect the change
            try:
                with open("stock.txt", "a") as file:
                    file.write("\n" + car_code)
            except FileNotFoundError:
                # Handle the case where the file is not found
                print("stock.txt file not found. Unable to update stock.")
                return False

            return True  # Successful addition

        # 2.3.9. Get stock by car_type
        def get_stock_by_car_type(self, car_type):
            # Create a list to store cars with the specified car_type
            cars_with_type = []

            # Iterate through the current stock
            for car_code in self.carretailer_stock:
                # Find the corresponding Car object based on the car_code
                car = get_car_by_code(car_code)  # You need to implement this function

                # Check if the car's car_type matches the specified car_type
                if car.get_car_type() == car_type:
                    cars_with_type.append(car)

            return cars_with_type

        # 2.3.10. Get stock by licence_type
        def get_stock_by_licence_type(self, licence_type):
            # Create a list to store cars that are allowed by the specified licence_type
            allowed_cars = []

            # Iterate through the current stock
            for car_code in self.carretailer_stock:
                # Find the corresponding Car object based on the car_code
                car = get_car_by_code(car_code)  # You need to implement this function

                # Check if the car is allowed by the licence_type
                if licence_type == "L" and not car.probationary_licence_prohibited_vehicle():
                    allowed_cars.append(car)
                elif licence_type == "P" and car.probationary_licence_prohibited_vehicle():
                    allowed_cars.append(car)
                elif licence_type == "Full":
                    allowed_cars.append(car)

            return allowed_cars

            # 2.3.11. Car recommendation

        def car_recommendation(self):
            if self.carretailer_stock:
                random_car_code = random.choice(self.carretailer_stock)
                return Car(random_car_code)
            else:
                return None

            # 2.3.12. Create an order
        def create_order(self, customer_name, customer_phone, licence_type):
            # Check if there are cars in stock
            if not self.carretailer_stock:
                return "No cars available in stock. Order creation failed."

            # Randomly select a car from the current stock
            random_car_code = random.choice(self.carretailer_stock)

            # Find the corresponding Car object based on the selected car code
            car = get_car_by_code(random_car_code)  # You need to implement this function

            # Remove the selected car from the current stock
            self.remove_from_stock(random_car_code)

            # Generate a unique order ID (you can use a similar approach as in generate_retailer_id)
            order_id = generate_unique_order_id()  # You need to implement this function

            # Create an Order object
            order = Order(order_id, customer_name, customer_phone, car, licence_type)

            # Append the order to the order.txt file
            with open("order.txt", "a") as order_file:
                order_file.write(order.to_string() + "\n")

            return order


# Test the actual CarRetailer Class
car_retailer = CarRetailer("12345", "Bhavna", "123 Main St, VIC 1234", (8.5, 17.5), ["MB123456", "MB123457"])
print(car_retailer)
# Test for getting the car retailer details
car_retailer = CarRetailer("12345", "Bhavna", "123 Main St, CA 1234", (8.5, 17.5), ["MB123456", "MB123457"])
print(str(car_retailer))  # Now the default string representation matches the format of get_car_retailer_info
# Test for the stock file in 2.3.3.
car_retailer = CarRetailer("321", "X", "123 Albert St, VIC 1235", (8.5, 17.5))
car_retailer.load_current_stock()
print(car_retailer.carretailer_stock)

# Test for operating hours in 2.3.4.:
car_retailer = CarRetailer("12345", "Jim", "101 Wellington,VIC 1235", (8.5, 17.5))
car_retailer.load_current_stock()
current_hour = 12.5  # Example current hour (12:30 PM)
print("Is the car retailer operating?", car_retailer.is_operating(current_hour))

# Test for getting all stock in 2.3.5.:
# Create an instance of CarRetailer
car_retailer = CarRetailer("001", "Cara", "123 Wellington, VIC 1234", (6.0, 20.0))

# Load current stock from stock.txt
car_retailer.load_current_stock()

# Get all available cars in stock and print the result
all_stock_info = car_retailer.get_all_stock()
for car_info in all_stock_info:
    print(car_info)


#Test 2.3.6.
car_retailer = CarRetailer("1345", "Hans", "123 St Kilda, VIC 1345", (8.5, 17.5), ["MB123456", "MB123457"])
user_postcode = 54321  # Replace with the user's postcode
postcode_distance = car_retailer.get_postcode_distance(user_postcode)
print(f"Postcode difference: {postcode_distance}")

#Test 2.3.7.
car_retailer = CarRetailer("1245", "Car Retailers", "123 Main St, CLA 1234", (8.5, 17.5), ["MB123456", "MB123457"])
car_code_to_remove = "MB123456"  # Replace with the car code you want to remove
removal_success = car_retailer.remove_from_stock(car_code_to_remove)

if removal_success:
    print(f"Successfully removed {car_code_to_remove} from stock.")
else:
    print(f"Failed to remove {car_code_to_remove} from stock.")





