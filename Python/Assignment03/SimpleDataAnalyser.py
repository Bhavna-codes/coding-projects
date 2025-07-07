# Import Necessary Libraries
import pandas as pd
import numpy as np

""" 

class to help with the analysis of data
ATTRIBUTES
----------
file_path of given csv file
currency_dict for the conversion rates to be updated as required

METHODS
------
3.2. extract_property_info()
    to read the csv file and extract data as needed in other functions

3.3. currency_exchange()
    to convert AUD into desired currency

3.5. avg_land_size()
    Return the average size of land of properties in a given suburb

3.8. locate_price()
    Identify and return if any properties are there in a given suburb for a given price range

"""

class PropertyData:

    def __init__(self, file_path, currency_dict):
        """
        Initialize class for data analysis

    PARAMETERS
    -----------
     file_path: Path to the CSV file containing property information
     currency_dict: Dictionary containing currency conversion rates
        """
        self.file_path = file_path
        self.currency_dict = currency_dict

#3.2 EXTRACT PROPERTY DATA

    def extract_property_info(self, file_path):
        """
        Method to read the CSV file and extract data as needed in other functions

    PARAMETERS
    -----------
     file_path: Path to the CSV file containing property information
     DataFrame containing property information
        """
        try:
            read = pd.read_csv(file_path)
            # Standardize capitalization of suburb names and convert them to lowercase
            read['suburb'] = read['suburb'].str.lower()
            return read
        except FileNotFoundError:
            print(f"Error: File not found at path: {file_path}")
            return None
        except pd.errors.EmptyDataError:
            print(f"Error: The file at {file_path} is empty.")
            return None
        except pd.errors.ParserError:
            print(f"Error: Unable to parse the file at {file_path}. Please check the file format.")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

#3.3 CURRENCY EXCHANGE

    def currency_exchange(self, target_currency, dataframe):
        """
        Method to convert property prices to the target currency

        PARAMETERS
        -----------
        target_currency: Target currency code
        dataframe: DataFrame containing property information

        RETURNS
        -------
        Numpy array of transformed property prices
        """
        try:
            if 'price' not in dataframe.columns:
                raise ValueError("Error: 'price' column not found in the DataFrame.")

            if target_currency.lower() in self.currency_dict:
                exchange_rate = self.currency_dict[target_currency.lower()]
            else:
                print(f"Error: Target currency '{target_currency}' not found in the currency dictionary.")
                return None

            # Convert property prices to the target currency using the exchange rate
            transformed_prices = dataframe['price'] * exchange_rate

            return np.array(transformed_prices)
        except Exception as e:
            print(f"An error occurred during currency exchange: {e}")
            return None


#3.5 AVERAGE LAND SIZE
    def avg_land_size(self, target_suburb, dataframe):
        """
        Method to calculate the average size of land of properties in a given suburb

         PARAMETERS
         -----------
         target_suburb: Target suburb for which to calculate the average land size ('all' for all suburbs)
         dataframe: DataFrame containing property information

         RETURNS
         -------
        Average land size in the target suburb
        """
        try:
            if 'land_size' not in dataframe.columns:
                raise ValueError("Error: 'land_size' column not found in the DataFrame.")

            if target_suburb.lower() == "all":
                filtered_data = dataframe  # Show data for all suburbs
            else:
                filtered_data = dataframe[dataframe['suburb'].str.lower() == target_suburb.lower()]

                if filtered_data.empty:
                    print(f"Error: Suburb '{target_suburb}' not found in the dataframe.")
                    return None

            # Convert 'land_size' column to numeric values and exclude negative values and NaN
            valid_land_sizes = pd.to_numeric(filtered_data['land_size'], errors='coerce')
            valid_land_sizes = valid_land_sizes[(valid_land_sizes > 0) & (~np.isnan(valid_land_sizes))]

            if not valid_land_sizes.empty:
                average_land_size = valid_land_sizes.mean()
                return average_land_size
            else:
                print(f"No valid land size data available in '{target_suburb}'.")
                return None

        except Exception as e:
            print(f"An error occurred: {e}")
#3.8 LOCATE PRICE
    def locate_price(self, target_price_range, target_suburb, dataframe):
        """
        Method to identify and return properties in a given suburb within the specified price range
     PARAMETERS
     -----------
     target_price_range: Price range selection ('a', 'b', or 'c')
     target_suburb: Target suburb in which to search the property
     dataframe: DataFrame containing property information
    RETURNS
    -------
    Filtered DataFrame with properties within the specified price range in the target suburb
        """
        try:
            if 'price' not in dataframe.columns or 'suburb' not in dataframe.columns:
                raise ValueError("Error: 'price' or 'suburb' column not found in the DataFrame.")

            # Clean and convert the 'price' column to numeric values
            dataframe['price'] = dataframe['price'].replace('[\$,]', '', regex=True).astype(float)

            if target_price_range == 'a':
                filtered_data = dataframe[(dataframe['suburb'].str.lower() == target_suburb.lower()) &
                                          (dataframe['price'] < 100000)]
            elif target_price_range == 'b':
                filtered_data = dataframe[(dataframe['suburb'].str.lower() == target_suburb.lower()) &
                                          ((dataframe['price'] >= 100000) & (dataframe['price'] <= 150000))]
            elif target_price_range == 'c':
                filtered_data = dataframe[(dataframe['suburb'].str.lower() == target_suburb.lower()) &
                                          (dataframe['price'] > 150000)]
            else:
                print("Invalid price range selection.")
                return None

            if not filtered_data.empty:
                return filtered_data
            else:
                print(f"No properties found in '{target_suburb}' within the specified price range.")
                return None

        except Exception as e:
            print(f"An error occurred during price search: {e}")
            return None


# # TEST
# # Define currency dictionary
# currency_dict = {
#     "AUD": 1, "USD": 0.66, "INR": 54.25, "CNY": 4.72, "JPY": 93.87,
#     "HKD": 5.12, "KRW": 860.92, "GBP": 0.51, "EUR": 0.60, "SGD": 0.88
# }
#
# # Specify the file path
# file_path = "property_information.csv"
#
# # Create an instance of PropertyData and extract property information
# property_data = PropertyData(file_path, currency_dict)
# property_dataframe = property_data.extract_property_info(file_path)
# # Extract property information from the CSV file
# property_dataframe = property_data.extract_property_info(file_path)
#
# # Specify the target price range and target suburb
# target_price_range = 'a'  # Example price range selection ('b' for 100000-150000)
# target_suburb = "Mount Waverley"  # Example target suburb
#
# # Locate properties in the specified suburb within the specified price range
# property_found = property_data.locate_price(target_price_range, target_suburb, property_dataframe)
#
# # Check if properties are found within the specified price range
# if property_found is not None and not property_found.empty:
#     print(f"Properties found in '{target_suburb}' within the specified price range:")
#     print(property_found)
# else:
#     print(f"No properties found in '{target_suburb}' within the specified price range.")
#
# # Calculate average land size in the specified suburb
# average_land_size = property_data.avg_land_size(target_suburb, property_dataframe)
# if average_land_size is not None:
#     print(f"Average land size in '{target_suburb}': {average_land_size} square meters")
# else:
#     print(f"No data available to calculate average land size in '{target_suburb}'.")
