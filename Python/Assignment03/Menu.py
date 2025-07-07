#Import classes
from SimpleDataAnalyser import PropertyData
from DataVisualiser import Visual

"""
A class for an interactive menu
"""

class Investor_Menu:

    def __init__(self):
        self.currency_dict = {
            "AUD": 1, "USD": 0.66, "INR": 54.25, "CNY": 4.72,
            "JPY": 93.87, "HKD": 5.12, "KRW": 860.92, "GBP": 0.51,
            "EUR": 0.60, "SGD": 0.88
        }
        self.property_data = PropertyData("property_information.csv", self.currency_dict)
        self.visual = Visual("property_information.csv", self.currency_dict)

    def display_menu(self):
        property_dataframe = self.property_data.extract_property_info(self.property_data.file_path)


        while True:
            print("\nInvestor Menu:")
            print("1. View Property Summary in a Suburb")
            print("2. View Property Price Distribution in a Suburb")
            print("3. View Average Land Size in a Suburb")
            print("4. Locate Properties within a Price Range in a Suburb")
            print("5. View Sales Trend")
            print("6. Exit")

            choice = input("Enter your choice: ").strip().lower()

            if choice == '1':
                suburb = input("Enter the suburb name (or 'all' for all suburbs): ").strip()
                if suburb.lower() == 'all':
                    suburb = suburb.lower()  # Keep suburb as 'all'
                self.visual.suburb_summary(suburb, property_dataframe)
            elif choice == '2':
                suburb = input("Enter the suburb name (or 'all' for all suburbs): ").strip()
                currency = input("Enter the target currency (e.g., AUD,USD,INR,CNY,JPY,HKD,KRW,GBP,EUR,SGD): ").strip().upper()
                if suburb.lower() == 'all':
                    suburb = suburb.lower()  # Keep suburb as 'all'
                self.visual.prop_val_distribution(suburb, currency, property_dataframe)
            elif choice == '3':
                suburb = input("Enter the suburb name: ")
                average_land_size = self.property_data.avg_land_size(suburb, property_dataframe)
                if average_land_size is not None:
                    print(f"Average land size in '{suburb}': {average_land_size:.2f} square meters")
                else:
                    print(f"No data available to calculate average land size in '{suburb}'.")
            elif choice == '4':
                print("Price Range Options:")
                print("a. Less than 100000")
                print("b. 100000-150000")
                print("c. More than 150000")
                price_range_choice = input("Enter your price range choice: ").strip().lower()

                if price_range_choice in ['a', 'b', 'c']:
                    if price_range_choice == 'a':
                        price_range_label = "less than 100000"
                    elif price_range_choice == 'b':
                        price_range_label = "100000-150000"
                    else:
                        price_range_label = "more than 150000"

                    suburb = input("Enter the suburb name: ")
                    properties = self.property_data.locate_price(price_range_choice, suburb, property_dataframe)
                    if properties is not None and not properties.empty:
                        print(f"Properties in '{suburb}' within the specified price range ({price_range_label}):")
                        print(properties)
                    else:
                        print(f"No properties found in '{suburb}' within the specified price range.")
                else:
                    print("Invalid price range choice. Please try again.")
            elif choice == '5':
                self.visual.sales_trend(property_dataframe)
            elif choice == '6':
                print("Exiting the menu. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    menu = Investor_Menu()
    menu.display_menu()


"""
REFERENCES
----------
(n.d.). NumPy: The absolute basics for beginners. https://numpy.org/doc/1.26/user/absolute_beginners.html
(n.d.). Re — Regular expression operations. https://docs.python.org/3/library/re.html
(n.d.). Working with missing data. https://pandas.pydata.org/pandas-docs/stable/user_guide/missing_data.html
(n.d.). Pandas documentation. https://pandas.pydata.org/pandas-docs/stable/
(n.d.). Using Matplotlib. https://matplotlib.org/stable/users/index.html
(n.d.). Object-Oriented Programming in Python (OOP): Tutorial. https://www.datacamp.com/tutorial/python-oop-tutorial

"""