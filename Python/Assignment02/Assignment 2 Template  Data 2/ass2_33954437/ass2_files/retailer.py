#Import re and random libraries to use necessary functions:


import random

class Retailer:

#2.2.1. initialize the retailer class:
    def __init__(self, retailer_id, retailer_name):
        self.retailer_id = retailer_id
        self.retailer_name = retailer_name

#2.2.2. Return the retailer information as a formatted string.
    def __str__(self):
        ret_det = "ID: " + self.retailer_id + ", Name: " + self.retailer_name
        return ret_det

#2.2.3. Generate a randomly generated unique retailer ID that is different from the existing retailer IDs and set it as the retailer_id (8 digits number)
def generate_retailer_id(list_retailer):
    while True:
        # Generate a random 8-digit ID
        new_id = str(random.randint(10000000, 99999999))

        # Check if the generated ID is unique
        if all(new_id != retailer.retailer_id for retailer in list_retailer):
            return new_id


# Test for 2.2.3. new id generation
existing_retailers = [Retailer("12345678", "Retailer1"), Retailer("98765432", "Retailer2")]
new_id = generate_retailer_id(existing_retailers)
print("Generated unique retailer ID:", new_id)