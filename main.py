# main.py
# This is the main entry point for the application. It initializes the GUI and links the button handlers to the appropriate functions in GUI_logic.py.
# It also initializes the mobilityManager which loads the university and user data, so that the GUI can display the relevant information when needed.

import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *
from tkinter import messagebox

import GUI
from mobilityManager import mobilityManager
from GUI_logic import *

def main(*args):
    '''Main entry point for the application.'''
    global root, _top1, _w1
    root = tk.Tk()
    root.protocol('WM_DELETE_WINDOW', root.destroy)

    # Initialize the GUI class
    _top1 = root
    _w1 = GUI.FrameBP(_top1)

    mobility_manager = mobilityManager("data/entries.csv")
    mobility_manager.load_universities()
    mobility_manager.load_users()
    _w1.AD_uni_combobox['values'] = mobility_manager.get_university_names()

    _w1.AD_editdelete_button.configure(command=lambda: admin_editdelete(_w1=_w1, mobility_manager=mobility_manager))    
    _w1.AD_add_button.configure(command=lambda: clear_admin_entries(_w1=_w1))

    _w1.AD_save_button.configure(command=lambda: save_admin_entries(_w1=_w1, mobility_manager=mobility_manager))
    _w1.AD_delete_button.configure(command=lambda: delete_admin_entries(_w1=_w1, mobility_manager=mobility_manager))

    _w1.AD_uni_combobox.bind('<<ComboboxSelected>>', lambda e: check_uni_selection(_w1=_w1))

    # Link Login Screen Buttons
    _w1.LG_student_button.configure(command=lambda: show_student_login(_w1=_w1, root=root))
    _w1.LG_admin_button.configure(command=lambda: show_admin_login(_w1=_w1, root=root))

    #________________________________________AUTHENTICATION BUTTON HANDLERS________________________________________________

    # Bind the auth button handlers
    _w1.LG_adminlogin_button.configure(command=lambda: admin_login_action(_w1=_w1, mobility_manager=mobility_manager))
    _w1.LG_studentlogin_button.configure(command=lambda: student_login_action(_w1=_w1, mobility_manager=mobility_manager))
    _w1.LG_studentsingup_button.configure(command=lambda: student_signup_action(_w1=_w1, mobility_manager=mobility_manager))

    # Link Logout Buttons
    _w1.ST_logout_button.configure(command=lambda: logout(_w1=_w1, root=root))
    _w1.AD_logout_button.configure(command=lambda: logout(_w1=_w1, root=root))

    # Student page Buttons
    _w1.ST_lang_button.configure(command=lambda: add_language_row(_w1=_w1))
    # Link Preference Buttons
    _w1.pref_down1.configure(command=lambda: move_pref_down(_w1, 1))
    _w1.pref_up2.configure(command=lambda: move_pref_up(_w1, 2))
    _w1.pref_down2.configure(command=lambda: move_pref_down(_w1, 2))
    _w1.pref_up3.configure(command=lambda: move_pref_up(_w1, 3))
    _w1.pref_down3.configure(command=lambda: move_pref_down(_w1, 3))
    _w1.pref_up4.configure(command=lambda: move_pref_up(_w1, 4))

    # Set the initial view to the Login screen
    show_login(_w1=_w1, root=root)
    check_uni_selection(_w1=_w1)

    root.mainloop()

if __name__ == '__main__':
    GUI.start_up()
    
