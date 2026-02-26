# user.py
# This module defines the User class hierarchy, including the base User class and the Admin and Student subclasses.


from utilities import Utilities

class User:
    def __init__(self, user_id, mail, pwd):
        # Protected attributes (#) for inheritance
        self._ID = user_id
        self._mail = mail
        self._pwd = pwd

    def create_user(self, user_id, mail, pwd):
        pass

    def verify_credentials(self, email, pwd):
        return self._mail == email and self._pwd == pwd

    def logout(self):
        print(f"User {self._mail} logged out.")

    def change_pwd(self, user_id, new_pwd):
        self._pwd = new_pwd

    def change_mail(self, new_mail):
        self._mail = new_mail

class Admin(User):
    def __init__(self, user_id, mail, pwd):
        super().__init__(user_id, mail, pwd)
        # Private attribute (-)
        self.__usertype = "admin"

    def login_retrieve_info(self, user_id):

        
        pass

    def add_university(self): 
        
        pass

    def edit_university(self): 
        
        pass

    def delete_university(self): 
        
        pass

class Student(User):
    def __init__(self, user_id, mail, pwd):
        super().__init__(user_id, mail, pwd)
        # Private attributes (-)
        self.__usertype = "student"
        self.__degree = ""
        self.__grade = 0.0
        self.__lang = []
        self.__continents = []
        self.__preferences = []

    def login_retrieve_info(self, user_id):
        
        pass

    def new_student(self, user_id, mail, pwd):
        new_user_id = "U" + Utilities.generate_random_id()
        print(new_user_id)
        pass

    def get_stud_att(self, attribute: str):
        return getattr(self, f"_Student__{attribute}", None)

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
