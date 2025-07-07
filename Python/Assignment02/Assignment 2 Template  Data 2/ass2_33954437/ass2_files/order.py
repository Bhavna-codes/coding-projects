import random
import string
import time

class Order:

    def __init__(self, order_id, order_car, order_retailer):
        self.order_id = order_id
        self.order_car = order_car
        self.order_retailer = order_retailer
        self.order_creation_time = int(time.time())  # UNIX timestamp in seconds

    def __str__(self):
        return f"Order ID: {self.order_id}, Car: {self.order_car['name']}, Retailer: {self.order_retailer}, Creation Time: {self.order_creation_time}"

    def generate_order_id(self):
        # Step 1: Generate a random string of 6 lowercase alphabetic characters
        random_chars = ''.join(random.choice(string.ascii_lowercase) for _ in range(6))

        # Step 2: Convert every second character to uppercase
        random_chars = ''.join(
            random_chars[i].upper() if i % 2 == 1 else random_chars[i] for i in range(len(random_chars))
        )

        # Step 3: Get ASCII code of each character in Step 2
        ascii_codes = [ord(char) for char in random_chars]

        # Step 4: Calculate ASCII code to the power of 2 and get remainder
        length = len(random_chars)
        powered_remainders = [(code ** 2) % length for code in ascii_codes]

        # Step 5: Obtain corresponding character from str_1 for each character in Step 2
        str_1 = string.ascii_lowercase + string.ascii_uppercase
        final_chars = [str_1[remainder] for remainder in powered_remainders]

        # Step 6: Append each character n times to the string updated in Step 2
        result = ''
        for i, char in enumerate(final_chars):
            n = i + 1  # n is the index of the character in the string from Step 2
            result += char * n

        # Step 7: Append the car_code from the order_car attribute and the order creation time
        current_time = int(time.time())
        order_id = result + self.order_car['name'] + str(current_time)

        return order_id

# Usage example:
car_code = "MB123456"
order_car = {"name": car_code}  # Replace this with the actual car object
order = Order("12345", order_car, "Retailer1")
order_id = order.generate_order_id()
print("Generated order ID:", order_id)
