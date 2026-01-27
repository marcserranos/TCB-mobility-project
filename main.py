import pandas as pd
import random
import mobility_manager as mm

# This is a simple test to retrieve university data using the MobilityManager class.
if __name__ == "__main__":
    # Initialize the MobilityManager with the path to the CSV file
    mobility_manager = mm.MobilityManager("data/entries.csv")
    
    # Load data from the CSV file
    mobility_manager.load_data()
    
    # Retrieve and print all university names
    university_names = mobility_manager.get_university_names()
    print("University Names:")
    for name in university_names:
        print(f"- {name}")
    
    # Retrieve and print all entries as a list of dictionaries
    all_entries = mobility_manager.get_all_entries_as_list()
    print("\nAll University Entries:")
    for entry in all_entries:
        print(entry)