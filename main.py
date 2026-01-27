import pandas as pd
import random
import MobilityManager as mm
import logic 

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

    # Generate 20 random IDs with Utilities class
    for i in range(20):
        random_id = logic.Utilities.generate_random_id()
        print(f"Generated Random ID {i+1}: {random_id}")

    # Retrieve a specific university by name
    university_to_find = "Universitat Pompeu Fabra"
    university = mobility_manager.get_uni_by_name(university_to_find)
    print(f"\nID of '{university_to_find}':")
    print(university["ID"])
    print(f"Length of ID: {len(university['ID'])}")
