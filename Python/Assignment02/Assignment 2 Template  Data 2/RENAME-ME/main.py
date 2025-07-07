#STUDENT ID : 33954437
# Import necessary classes and functions
from car import Car
from car_retailer import CarRetailer
from order import Order
import random
import re
import time

# Function to generate random car details for Toyota, Suzuki, Honda, and MG
# Function to generate 12 unique car objects with random car names
def generate_random_cars():
#Initialize an empty car list to store test data that will be generated
    cars = []
#Create list of car names that i want to be seen under the retailers
    car_names = ["Toyota", "Suzuki", "MG", "Honda"]
#Initialize empty set to track that car codes are unique
    used_car_codes = set()  # To track used car codes
#Logic to generate test data for 12 cars
    while len(cars) < 12:
#Choose name randomly from car_list
        name = random.choice(car_names)
#Initialize car_code to none to store unique values
        car_code = None

        # Generate a unique car code
        while car_code is None or car_code in used_car_codes:
            manufacturer_code = random.choice(["TM", "SZ", "MG", "HN"])
            serial_number = random.randint(100000, 999999)  # Random serial number between 100000 and 999999
            car_code = f"{manufacturer_code}{serial_number}"

        # Create a Car object and add it to the list
        car = Car(
            name=name,
            car_code=car_code,
            car_horsepower=random.randint(100, 300),
            car_weight=random.randint(800, 1500)
        )
        cars.append(car)
        used_car_codes.add(car_code)

    return cars

# Function to load stock data from "stock.txt" file
def load_stock_from_file():
#using try and error incase file not found
    try:
        with open("stock.txt", "r") as file:
#read all the lines
            lines = file.readlines()
#list comprehension with cleaned lines
            return [line.strip() for line in lines]
    except FileNotFoundError:
        print("stock.txt file not found. Please generate test data first (Option 1).")
        return []

# Function to save stock data to "stock.txt" file
def save_stock_to_file(stock_data):
    try:
        with open("stock.txt", "w") as file:
            for car_code in stock_data:
                file.write(car_code + "\n")
        print("Stock data saved successfully.")
    except FileNotFoundError:
        print("stock.txt file not found. Unable to save stock data.")

# Function to load order data from "order.txt" file
def load_orders_from_file():
    try:
        with open("order.txt", "r") as file:
            lines = file.readlines()
            return [line.strip() for line in lines]
    except FileNotFoundError:
        print("order.txt file not found.")
        return []

# Function to save an order to "order.txt" file
def save_order_to_file(order_id, car_code, retailer_name):
    try:
        with open("order.txt", "a") as file:
            file.write(f"{order_id}, {car_code}, {retailer_name}\n")
        print(f"Order no #{order_id} successfully placed at retailer {retailer_name} ({retailer_id}).")  # Display the order ID and retailer ID
    except FileNotFoundError:
        print("order.txt file not found. Unable to save order data.")

# Function to calculate postcode difference
def get_postcode_distance(retailer, user_postcode):
#r'\d{4}$' is a regular expression pattern that matches four consecutive digits at the end of a string to match with the retailer address
    car_postcode_match = re.search(r'\d{4}$', retailer.retailer_address)
    if car_postcode_match:
        car_postcode = int(car_postcode_match.group())
        return abs(car_postcode - user_postcode)
    else:
        return None

# Function to find the nearest car retailer and ensure they only eneter 4 digits
def find_nearest_retailer(retailers, user_postcode):
    if not isinstance(user_postcode, int) or not (1000 <= user_postcode <= 9999):
        print("Invalid postcode. Please enter a 4-digit postcode.")
        return None

    nearest_retailer = None
    min_distance = float('inf')

    for retailer in retailers:
        distance = get_postcode_distance(retailer, user_postcode)
        if distance is not None and distance < min_distance:
            min_distance = distance
            nearest_retailer = retailer

    if nearest_retailer:
        print(f"The nearest car retailer is {nearest_retailer.retailer_name} located at {nearest_retailer.retailer_address}.")
    else:
        print("No car retailers found in the area.")

    return nearest_retailer

# Function to display a submenu for car purchase advice
def car_purchase_advice_submenu(selected_retailer, cars):
    while True:
        print(f"\nCar Purchase Advice for {selected_retailer.retailer_name}:")
        print("1. Recommend a Car")
        print("2. Get All Cars in Stock")
        print("3. Get Cars by Car Types")
        print("4. Get Probationary Licence Permitted Cars in Stock")
        print("5. Go Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == "1":
            if selected_retailer.carretailer_stock:
                # Filter cars that belong to the selected retailer's stock
                available_cars = [car for car in cars if car.car_code in selected_retailer.carretailer_stock]

                if available_cars:
                    random_car = random.choice(available_cars)
                    print(f"Recommended Car: {random_car.name}")
                    print("Car Details:")
                    print(f"Car Code: {random_car.car_code}")
                    print(f"Horsepower: {random_car.car_horsepower}")
                    print(f"Weight: {random_car.car_weight}")
                else:
                    print(f"No cars available in stock for {selected_retailer.retailer_name}.")
            else:
                print(f"No cars available in stock for {selected_retailer.retailer_name}.")


        elif choice == "2":
            if selected_retailer.carretailer_stock:
                print(f"Cars in Stock for {selected_retailer.retailer_name}:")
                car_info = []
                for car_code in selected_retailer.carretailer_stock:
                    car = get_car_by_code(car_code, cars)
                    car_info.append(f"{car.name} ({car.car_code})")
                print(
                    f"Available cars under {selected_retailer.retailer_id} {selected_retailer.retailer_name} are: {', '.join(car_info)}")
            else:
                print(f"No cars available in stock for {selected_retailer.retailer_name}.")


        elif choice == "3":
            car_type = input("Enter car type (e.g., AWD, RWD, FWD): ").strip().lower()
            matching_cars = []
            for car_code in selected_retailer.carretailer_stock:
                car = get_car_by_code(car_code, cars)
                if car.get_car_type() == car_type:
                    matching_cars.append(car)
            if matching_cars:
                print(f"Cars in Stock for {selected_retailer.retailer_name} (Car Type: {car_type}):")
                for car in matching_cars:
                    print(f"{car.name} ({car.car_code})")
            else:
                print(f"No {car_type} cars available in stock for {selected_retailer.retailer_name}.")

        elif choice == "4":
            probationary_permitted_cars = []
            for car_code in selected_retailer.carretailer_stock:
                car = get_car_by_code(car_code, cars)
                if not car.probationary_licence_prohibited_vehicle():
                    probationary_permitted_cars.append(car)
            if probationary_permitted_cars:
                print(f"Probationary Licence Permitted Cars in Stock for {selected_retailer.retailer_name}:")
                for car in probationary_permitted_cars:
                    print(f"{car.name} ({car.car_code})")
            else:
                print(f"No probationary licence permitted cars available in stock for {selected_retailer.retailer_name}.")

        elif choice == "5":
            break

        else:
            print("Invalid choice. Please select a valid option (1-5).")

# Function to create and place a car order
def create_and_place_order(retailers, cars):
    print("\nPlace a Car Order:")

    retailer_id = input("Enter Retailer ID: ")
    car_code = input("Enter Car Code: ")
    order_time = time.localtime()

    retailer = next((r for r in retailers if r.retailer_id == retailer_id), None)
    car = get_car_by_code(car_code, cars)

    if retailer and car:
        current_hour = order_time.tm_hour + order_time.tm_min / 60
        if retailer.is_operating(current_hour):
            if car_code in retailer.carretailer_stock:  # Check if the car is in the retailer's stock
                order_id = car_code  # Use the car code as the order ID
                order = Order(order_id, car, retailer.retailer_name)
                save_order_to_file(order_id, car_code, retailer.retailer_name)  # Save the order details
            else:
                print(f"Invalid car code. Car with code {car_code} is not available in stock for {retailer.retailer_name}.")
        else:
            print("Retailer is closed at the current time. Order placement failed.")
    else:
        print("Invalid retailer ID or car code. Order placement failed.")

# Function to get a Car object by car code
def get_car_by_code(car_code, cars):
    for car in cars:
        if car.car_code == car_code:
            return car
    return None

# Main program
if __name__ == "__main__":
    # Generate random car details
    cars = generate_random_cars()

    # Load stock data from "stock.txt" file
    stock_data = load_stock_from_file()

    # Load order data from "order.txt" file
    orders = load_orders_from_file()

    # Create three fixed car retailers with assigned cars
    retailer1_cars = cars[:4]
    retailer2_cars = cars[4:8]
    retailer3_cars = cars[8:12]

    retailer1_stock = [car.car_code for car in retailer1_cars]
    retailer2_stock = [car.car_code for car in retailer2_cars]
    retailer3_stock = [car.car_code for car in retailer3_cars]

    retailers = [
        CarRetailer("1", "Hondauto", "123 Sarto Rd, VIC 3168", (8.5, 17.5), retailer1_stock),
        CarRetailer("2", "Melbourne Quality Cars", "668 South Rd, VIC 3189", (8.5, 17.5), retailer2_stock),
        CarRetailer("3", "3 Point Motors", "484 Heidelberg Rd, VIC 3078", (8.5, 17.5), retailer3_stock),
    ]

    while True:
        print("\nCar Purchase Advisor System")
        print("1. Generate Test Data")
        print("2. Look for the Nearest Car Retailer")
        print("3. Get Car Purchase Advice")
        print("4. Place a Car Order")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            # Generate test data and save it to "stock.txt" file
            stock_data = [car.car_code for car in cars]
            save_stock_to_file(stock_data)

        elif choice == "2":
            # Look for the nearest car retailer
            user_postcode = input("Enter your postcode (4 digits): ")
            try:
                user_postcode = int(user_postcode)
                nearest_retailer = find_nearest_retailer(retailers, user_postcode)
            except ValueError:
                print("Invalid postcode. Please enter a 4-digit postcode.")

        elif choice == "3":
            # Get car purchase advice
            if not retailers:
                print("Please add retailers and stock data before getting car purchase advice.")
                continue

            print("\nCar Retailers:")
            for retailer in retailers:
                print(f"{retailer.retailer_id}. {retailer.retailer_name}")

            retailer_id = input("Select a retailer by entering their Retailer ID: ")
            selected_retailer = next((r for r in retailers if r.retailer_id == retailer_id), None)

            if selected_retailer:
                car_purchase_advice_submenu(selected_retailer, cars)
            else:
                print("Retailer not found. Please select a valid Retailer ID.")

        elif choice == "4":
            # Place a car order
            if not retailers:
                print("Please add retailers and stock data before placing an order.")
                continue

            create_and_place_order(retailers, cars)

        elif choice == "5":
            # Exit the program
            print("Exiting the program.")
            break

        else:
            print("Invalid choice. Please select a valid option (1-5).")


