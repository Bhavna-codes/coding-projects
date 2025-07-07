# Import Necessary Libraries
import pandas as pd
from SimpleDataAnalyser import PropertyData
import matplotlib.pyplot as plt
import os

""" 

class to help with the creating summary and visualisation  of data
ATTRIBUTES
----------
file_path of given csv file
currency_dict for the conversion rates to be updated as required

METHODS
------

3.4. suburb_summary()
    Return the summary of properties in a suburb
    
3.6. prop_val_distribution()
    Return Histogram with Property Value Distibution

3.7. sales_trend()
    Return the sales trend for properties

"""
class Visual(PropertyData):

    def __init__(self, file_path="property_information.csv", currency_dict=None):
        super().__init__(file_path, currency_dict)

#3.4 PROPERTY SUMMARY
    def suburb_summary(self, target_suburb, dataframe=None):
        """
        Method to get the summary of properties in a suburb

        PARAMETERS
        -----------
        target_suburb: The suburb in which we want to search
        dataframe: DataFrame containing property information

        """

        if dataframe is None:
            dataframe = self.extract_property_info(self.file_path)

        try:
            if target_suburb.lower() == 'all':
                filtered_data = dataframe  # Show data for all suburbs
            else:
                filtered_data = dataframe[dataframe['suburb'].str.lower() == target_suburb.lower()]

            if filtered_data.empty:
                print(f"No properties found in '{target_suburb}'.")
                return

            print("\nSummary of Properties in", target_suburb.capitalize())
            print(filtered_data[['id', 'badge', 'price', 'bedrooms', 'bathrooms', 'parking_spaces']])
        except Exception as e:
            print(f"An error occurred: {e}")

#3.6 PROPERTY DISTRIBUTION
    def prop_val_distribution(self, suburb, target_currency="AUD", dataframe=None):
        """
        Method to plot property price distribution for a given suburb

        PARAMETERS
        -----------
        suburb: The suburb for which property prices will be plotted ('all' for all suburbs)
        target_currency: Target currency code (default is AUD)
        dataframe: DataFrame containing property information

        """
        if dataframe is None:
            dataframe = self.extract_property_info(self.file_path)

        try:
            if suburb.lower() == 'all':
                filtered_data = dataframe  # Show data for all suburbs
            else:
                filtered_data = dataframe[dataframe['suburb'].str.lower() == suburb.lower()]

            if filtered_data.empty:
                print(f"No properties found in '{suburb}'.")
                return

            valid_property_prices = pd.to_numeric(filtered_data['price'], errors='coerce').dropna()

            if target_currency.upper() in self.currency_dict:
                exchange_rate = self.currency_dict[target_currency.upper()]
                converted_property_prices = valid_property_prices * exchange_rate
                currency_label = f"({target_currency})"
            else:
                print(f"Warning: Target currency '{target_currency}' not found in the currency_dict. Using AUD.")
                converted_property_prices = valid_property_prices
                currency_label = "(AUD)"

            plt.hist(converted_property_prices, bins=30, color='blue', alpha=0.7)
            plt.xlabel(f'Property Price {currency_label}')
            plt.ylabel('Frequency')
            plt.title(f'Property Price Distribution in {suburb.capitalize()}')
            plt.grid(True)
            plt.show()

        except Exception as e:
            print(f"An error occurred: {e}")
#3.7 SALES TREND
    def sales_trend(self, dataframe=None):
        """
                          Method to return a line graph sales trend

                      PARAMETERS
                      -----------
                       dataframe containing property information


        """

        if dataframe is None:
            dataframe = self.extract_property_info(self.file_path)
        try:
            if 'sold_date' not in dataframe.columns:
                raise ValueError("Error: 'sold_date' column not found in the DataFrame.")

            dataframe['sold_date'] = pd.to_datetime(dataframe['sold_date'], format='%d/%m/%Y')
            dataframe['year_sold'] = dataframe['sold_date'].dt.year

            sales_count_by_year = dataframe['year_sold'].value_counts().sort_index()

            plt.figure(figsize=(10, 6))
            plt.plot(sales_count_by_year.index, sales_count_by_year.values, marker='o', color='b', linestyle='-',
                     linewidth=2)
            plt.xlabel("Year")
            plt.ylabel("Number of Properties Sold")
            plt.title("Sales Trend")
            plt.grid(True)
            plt.ion()  # Activate interactive mode
            plt.savefig(os.path.join(os.path.dirname(__file__), 'sales_trend.png'))
            plt.show()
        except Exception as e:
            print(f"An error occurred during sales trend visualization: {e}")

#     #TEST
#
#
# if __name__ == "__main__":
#     # Define dictionary
#     currency_dict = {
#         "AUD": 1, "USD": 0.66, "INR": 54.25, "CNY": 4.72, "JPY": 93.87,
#         "HKD": 5.12, "KRW": 860.92, "GBP": 0.51, "EUR": 0.60, "SGD": 0.88
#     }
#
#     try:
#         # Specify the file path for the property information CSV file
#         file_path = "property_information.csv"
#
#         # Create an instance of the Visual class with file path and currency dictionary
#         visual = Visual(file_path=file_path, currency_dict=currency_dict)
#
#         # Call the suburb_summary method
#         target_suburb = "Mount Waverley"
#         visual.suburb_summary(target_suburb)
#
#         # Call the prop_val_distribution method
#         suburb_for_distribution = "Mount Waverley"
#         target_currency_for_distribution = "INR"
#         visual.prop_val_distribution(suburb_for_distribution, target_currency_for_distribution)
#
#         # Call the sales_trend method
#         visual.sales_trend()
#
#     except Exception as e:
#         print(f"Error: {e}")
