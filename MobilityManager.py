# mobilityManager.py

# This is the principal class of the application.
# It is responsible for managing the university and user data,
# including loading from and saving to a CSV file, as well as Create, Read,
# Update, and Delete (CRUD) operations on university entries.

import pandas as pd
import GUI
from utilities import Utilities

class mobilityManager:
    def __init__(self, uni_file_path="data/entries.csv", users_file_path="data/users.csv"):
        
        self.__file_path = uni_file_path
        self.__users_file_path = users_file_path
        self.__uni_df = pd.DataFrame()
        self.__users_df = pd.DataFrame()

    def load_universities(self):
        """Extracts information from the CSV into a Pandas DataFrame."""
        try:
            self.__uni_df = pd.read_csv(self.__file_path)
        except FileNotFoundError:
            self.__uni_df = pd.DataFrame()

    def save_data(self):
        """Persists the in-memory DataFrame back into the CSV file."""
        # index=False prevents Pandas from adding an extra column for the row numbers
        self.__uni_df.to_csv(self.__file_path, index=False)

    def get_university_names(self):
        """Returns a simple list of names for GUI dropdowns or lists."""
        if self.__uni_df.empty:
            return []
        return self.__uni_df['Name'].tolist()

    def get_all_entries_as_list(self):
        """Returns all universities as a list of dictionaries"""
        # 'records' format: [{col1: val1, col2: val2}, ...]
        return self.__uni_df.to_dict('records')

    def get_uni_by_id(self, uni_id):
        """Retrieves a single dictionary entry based on the University ID."""
        entry = self.__uni_df[self.__uni_df['ID'] == uni_id]
        if not entry.empty:
            return entry.iloc[0].to_dict()
        return None
    
    def get_uni_by_name(self, uni_name):
        """Retrieves a single dictionary entry based on the University Name."""
        entry = self.__uni_df[self.__uni_df['Name'] == uni_name]
        if not entry.empty:
            return entry.iloc[0].to_dict()
        return None

    def add_entry(self, new_data_dict):
        """Appends a new dictionary entry to the DataFrame and saves it."""
        # Convert the dictionary to a DataFrame row and concatenate
        new_row = pd.DataFrame([new_data_dict])
        self.__uni_df = pd.concat([self.__uni_df, new_row], ignore_index=True)
        self.save_data()

    def update_entry(self, uni_id, updated_data_dict):
        """Locates an entry by ID and updates its fields with new dictionary values."""
        if uni_id in self.__uni_df['ID'].values:
            # Find row index where ID matches
            idx = self.__uni_df.index[self.__uni_df['ID'] == uni_id][0]
            # Update values using .loc
            for key, value in updated_data_dict.items():
                self.__uni_df.at[idx, key] = value
            self.save_data()
            return True
        return False

    def delete_entry(self, uni_id):
        """Removes a university entry from the DataFrame based on its ID."""
        self.__uni_df = self.__uni_df[self.__uni_df['ID'] != uni_id]
        self.save_data()

    def load_users(self):
        """Loads user data from the users CSV file."""
        try:
            self.__users_df = pd.read_csv(self.__users_file_path)
        except FileNotFoundError:
            self.__users_df = pd.DataFrame()

    def save_users(self):
        """Saves the current user DataFrame back to the users CSV file."""
        self.__users_df.to_csv(self.__users_file_path, index=False)
    
    def verify_credentials(self, email, pwd, user_type):
        """Checks if the provided email and password match any user in the users DataFrame."""
        if self.__users_df.empty:
            return False
        user = self.__users_df[(self.__users_df['email'] == email) & (self.__users_df['password'] == pwd) & (self.__users_df['user_type'] == user_type)]
        return not user.empty
    
    def get_user_by_credentials(self, email, pwd, user_type):
        """Retrieves user data (as a dictionary) by email, password, and user_type."""
        if self.__users_df.empty:
            return None
        user = self.__users_df[(self.__users_df['email'] == email) & (self.__users_df['password'] == pwd) & (self.__users_df['user_type'] == user_type)]
        if not user.empty:
            return user.iloc[0].to_dict()
        return None
    
    def add_user(self, user_data_dict):
        """Adds a new user to the users DataFrame and saves it."""
        # Generate random ID for the new user
        user_data_dict['UID'] = "U" + Utilities.generate_random_id()
        # Convert the dictionary to a DataFrame row and concatenate
        new_user_row = pd.DataFrame([user_data_dict])
        self.__users_df = pd.concat([self.__users_df, new_user_row], ignore_index=True)
        self.save_users()
        return user_data_dict['UID']

    def check_new_user_email(self, email):
        """Checks if the provided email already exists in the users DataFrame."""
        if self.__users_df.empty:
            return False
        return not self.__users_df[self.__users_df['email'] == email].empty