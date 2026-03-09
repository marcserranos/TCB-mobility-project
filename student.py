# Student.py
# This module defines the Student subclass.

import pandas as pd
from utilities import Utilities
from user import User

class Student(User):
    def __init__(self, user_id, mail, pwd):
        super().__init__(user_id, mail, pwd)
        # Private attributes (-)
        self.__usertype = "student"
        self.__degree = ""
        self.__grade = 0.0
        self.__lang = {}
        self.__continents = []
        self.__preferences = []
        # Languages available
        self.__available_languages = ["English", "Spanish", "French", "German", "Italian", "Portuguese", "Chinese", "Japanese"]
        # Continents available
        self.__available_continents = ["Europe", "South America", "Asia", "Africa", "North America", "Oceania"]
        # Path to student info CSV
        self.__student_info_file = "data/student_info.csv"

    def load_from_csv(self, filepath="data/student_info.csv"):
        """
        Load student information from the student_info.csv file based on UID.
        This method reads the CSV and populates the student's attributes.
        """
        try:
            df = pd.read_csv(filepath, dtype=str)
            # find the row matching this student's UID
            student_row = df[df['UID'] == self._ID]
            
            if student_row.empty:
                # no existing data for this student, will initialize on first save
                print(f"No existing data found for student {self._ID}. Data will be initialized on save.")
                return False
            
            # extract and set attributes
            row = student_row.iloc[0]
            
            # load degree
            if pd.notna(row.get('degree')) and row.get('degree') != '':
                self.__degree = str(row['degree'])
            
            # load grade
            try:
                grade_val = row.get('grade')
                if pd.notna(grade_val) and grade_val != '':
                    self.__grade = float(grade_val)
            except (ValueError, TypeError):
                self.__grade = 0.0
            
            # load languages
            langs = {}
            for lang in self.__available_languages:
                if lang in row.index:
                    lang_val = row.get(lang)
                    if pd.notna(lang_val) and lang_val != '':
                        langs[lang] = str(lang_val)
            self.__lang = langs
            
            # Load continents
            continents = []
            for continent in self.__available_continents:
                if continent in row.index:
                    cont_val = row.get(continent)
                    if pd.notna(cont_val) and cont_val != '':
                        continents.append(continent)
            self.__continents = continents
            
            # load preferences - they are stored as priority numbers, reconstruct the list
            prefs = []
            pref_fields = ['Cost of Living', 'Weather', 'Nightlife', 'Academic Rank']
            # get priorities and sort by them
            pref_priorities = {}
            for pref in pref_fields:
                if pref in row.index:
                    pref_val = row.get(pref)
                    if pd.notna(pref_val) and pref_val != '':
                        try:
                            priority = int(float(pref_val))
                            pref_priorities[pref] = priority
                        except (ValueError, TypeError):
                            pass
            
            # sort by priority and extract the preference names
            if pref_priorities:
                sorted_prefs = sorted(pref_priorities.items(), key=lambda x: x[1])
                prefs = [pref_name for pref_name, _ in sorted_prefs]
            
            self.__preferences = prefs
            
            print(f"Successfully loaded student data for {self._ID}")
            return True
            
        except FileNotFoundError:
            print(f"student_info.csv not found at {filepath}")
            return False
        except Exception as e:
            print(f"Error loading student data: {e}")
            return False

    def save_to_csv(self, filepath="data/student_info.csv"):
        """
        Save the student's current attributes back to the student_info.csv file.
        This method updates or creates a row based on the student's UID.
        Preferences are stored as priority numbers (1, 2, 3, 4) based on their order in the list.
        """
        try:
            # try to load existing CSV
            try:
                df = pd.read_csv(filepath, dtype=str)
            except FileNotFoundError:
                # create new DataFrame with headers if file doesn't exist
                df = pd.DataFrame()
            
            # define all expected columns in order
            all_columns = ['UID', 'degree', 'grade']
            all_columns.extend(self.__available_languages)
            all_columns.extend(self.__available_continents)
            all_columns.extend(['Cost of Living', 'Weather', 'Nightlife', 'Academic Rank'])
            
            # prepare the data dictionary for this student
            student_data = {
                'UID': self._ID,
                'degree': str(self.__degree),
                'grade': str(self.__grade),
            }
            
            # Add language columns with their levels
            for lang in self.__available_languages:
                student_data[lang] = self.__lang.get(lang, '')
            
            # add continent columns - store the continent name if selected, empty otherwise
            for continent in self.__available_continents:
                student_data[continent] = continent if continent in self.__continents else ''
            
            # Add preference columns - store priority numbers based on list order
            # The preferences list is already in priority order (index 0 = highest priority = 1)
            pref_fields = ['Cost of Living', 'Weather', 'Nightlife', 'Academic Rank']
            for i, pref_field in enumerate(pref_fields):
                # Find the priority of this preference (1-based index)
                if pref_field in self.__preferences:
                    priority = self.__preferences.index(pref_field) + 1
                    student_data[pref_field] = str(priority)
                else:
                    student_data[pref_field] = ''
            
            # Check if student already exists in the dataframe
            if not df.empty and 'UID' in df.columns and self._ID in df['UID'].values:
                # Update existing row
                idx = df.index[df['UID'] == self._ID][0]
                for key, value in student_data.items():
                    df.at[idx, key] = value
            else:
                # Add new row - ensure all columns exist
                if df.empty:
                    # Create new dataframe with all columns
                    df = pd.DataFrame(columns=all_columns)
                else:
                    # Add missing columns to existing dataframe
                    for col in all_columns:
                        if col not in df.columns:
                            df[col] = ''
                
                # Add the new student row
                new_row = pd.DataFrame([student_data])
                df = pd.concat([df, new_row], ignore_index=True)
            
            # Ensure all columns are present in the final dataframe
            for col in all_columns:
                if col not in df.columns:
                    df[col] = ''
            
            # Reorder columns to match expected order
            df = df[all_columns]
            
            # Save back to CSV
            df.to_csv(filepath, index=False)
            print(f"Successfully saved student data for {self._ID}")
            return True
            
        except Exception as e:
            print(f"Error saving student data: {e}")
            import traceback
            traceback.print_exc()
            return False

    def login_retrieve_info(self, user_id):
        pass

    def new_student(self, user_id, mail, pwd):
        new_user_id = "U" + Utilities.generate_random_id()
        print(new_user_id)
        pass

    def get_stud_att(self, attribute: str):
        return getattr(self, f"_Student__{attribute}", None)

    # Getter methods for GUI and other components
    def get_degree(self):
        return self.__degree
    
    def set_degree(self, degree):
        self.__degree = degree
    
    def get_grade(self):
        return self.__grade
    
    def set_grade(self, grade):
        try:
            self.__grade = float(grade)
        except (ValueError, TypeError):
            self.__grade = 0.0
    
    def get_languages(self):
        return self.__lang
    
    def set_languages(self, languages_dict):
        self.__lang = languages_dict
    
    def get_continents(self):
        return self.__continents
    
    def set_continents(self, continents_list):
        self.__continents = continents_list
    
    def get_preferences(self):
        return self.__preferences
    
    def set_preferences(self, preferences_list):
        self.__preferences = preferences_list

    def load_from_gui(self, gui_frame):
        """Populate this student's data from a FrameBP instance.

        The frame should be the object created in `GUI.FrameBP` which
        exposes the widgets used in the student page (degree_var,
        ST_grade_entry, added_languages, continent variables and the
        pref_label1..pref_label4 labels). After calling this method the
        student's private attributes will reflect the values chosen by
        the user.
        """
        # degree & grade
        self.__degree = gui_frame.degree_var.get()
        try:
            self.__grade = float(gui_frame.ST_grade_entry.get())
        except Exception:
            self.__grade = 0.0

        # languages
        langs = {}
        for lang, (frm, level_var) in gui_frame.added_languages.items():
            langs[lang] = level_var.get()
        self.__lang = langs

        # continents based on IntVar flags
        continents = []
        mapping = {
            "Europe": gui_frame.var_EU,
            "North America": gui_frame.var_NA,
            "Asia": gui_frame.var_AS,
            "South America": gui_frame.var_SA,
            "Oceania": gui_frame.var_OC,
            "Africa": gui_frame.var_AF,
        }
        for name, var in mapping.items():
            if var.get():
                continents.append(name)
        self.__continents = continents

        # preferences from pref_label1..pref_label4
        prefs = []
        for i in range(1, 5):
            lbl = getattr(gui_frame, f"pref_label{i}", None)
            if lbl is not None:
                txt = lbl.cget("text")
                if ". " in txt:
                    prefs.append(txt.split(". ", 1)[1])
                else:
                    prefs.append(txt)
        self.__preferences = prefs