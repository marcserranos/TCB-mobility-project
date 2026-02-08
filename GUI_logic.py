import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *
from tkinter import messagebox

import GUI
from MobilityManager import MobilityManager

# ! /usr/bin/env python3
#  -*- coding: utf-8 -*-

import sys
import tkinter as tk
import GUI
from utilities import Utilities


def admin_editdelete(_top1, _w1, root, mobility_manager):
    uni_name = _w1.AD_uni_combobox.get()
    uni_data = mobility_manager.get_uni_by_name(uni_name)

    if not uni_data:
        tk.messagebox.showerror("Not found", f"University '{uni_name}' not found.")
        return

    _w1.AD_entries_frame.place(relx=0.244, rely=0.027, relheight=0.948, relwidth=0.741)
    _w1.AD_delete_button.config(state="normal")

    _w1.AD_city_entry.delete(0, tk.END)
    _w1.AD_city_entry.insert(0, uni_data["City"])
    _w1.AD_country_entry.delete(0, tk.END)
    _w1.AD_country_entry.insert(0, uni_data["Country"])
    _w1.AD_cutoff_entry.delete(0, tk.END)
    _w1.AD_cutoff_entry.insert(0, uni_data["Previous cutoff grade"])
    _w1.AD_weather_entry.delete(0, tk.END)
    _w1.AD_weather_entry.insert(0, uni_data["Weather"])
    _w1.AD_rank_entry.delete(0, tk.END)
    _w1.AD_rank_entry.insert(0, uni_data["University Ranking"])
    _w1.AD_engrank_entry.delete(0, tk.END)
    _w1.AD_engrank_entry.insert(0, uni_data["Engineering Ranking"])
    _w1.AD_ID_entry.configure(state="normal")
    _w1.AD_ID_entry.delete(0, tk.END)
    _w1.AD_ID_entry.insert(0, uni_data["ID"])
    _w1.AD_ID_entry.configure(state="readonly")
    _w1.AD_uniname_entry.delete(0, tk.END)
    _w1.AD_uniname_entry.insert(0, uni_data["Name"])
    _w1.AD_mingrade_entry.delete(0, tk.END)
    _w1.AD_mingrade_entry.insert(0, uni_data["Minimum grade"])
    _w1.AD_lat_entry.delete(0, tk.END)
    _w1.AD_lat_entry.insert(0, uni_data["Latitude"])
    _w1.AD_long_entry.delete(0, tk.END)
    _w1.AD_long_entry.insert(0, uni_data["Longitude"])
    _w1.AD_web_entry.delete(0, tk.END)
    _w1.AD_web_entry.insert(0, uni_data["Website"])
    _w1.AD_continent_menu.set(uni_data["Continent"])
    _w1.AD_cost_scale.set(uni_data["Cost of living"])
    _w1.AD_spots_scale.set(uni_data["Spots available"])
    _w1.AD_duration_scale.set(uni_data["Duration (months)"])
    _w1.AD_nightlife_scale.set(uni_data["Nightlife"])

def clear_admin_entries(_top1, _w1, root, mobility_manager):
    _w1.AD_delete_button.config(state="disabled")
    _w1.AD_entries_frame.place(relx=0.244, rely=0.027, relheight=0.948, relwidth=0.741)
    _w1.AD_uni_combobox.set("Select University")
    check_uni_selection()

    _w1.AD_city_entry.delete(0, tk.END)
    _w1.AD_country_entry.delete(0, tk.END)
    _w1.AD_cutoff_entry.delete(0, tk.END)
    _w1.AD_weather_entry.delete(0, tk.END)
    _w1.AD_rank_entry.delete(0, tk.END)
    _w1.AD_engrank_entry.delete(0, tk.END)
    _w1.AD_ID_entry.configure(state="normal")
    _w1.AD_ID_entry.delete(0, tk.END)
    _w1.AD_ID_entry.insert(0, "Auto-generated")
    _w1.AD_ID_entry.configure(state="readonly")
    _w1.AD_uniname_entry.delete(0, tk.END)
    _w1.AD_mingrade_entry.delete(0, tk.END)
    _w1.AD_lat_entry.delete(0, tk.END)
    _w1.AD_long_entry.delete(0, tk.END)
    _w1.AD_web_entry.delete(0, tk.END)
    _w1.AD_continent_menu.set("")
    _w1.AD_cost_scale.set(1.0)
    _w1.AD_spots_scale.set(1.0)
    _w1.AD_duration_scale.set(1.0)
    _w1.AD_nightlife_scale.set(1.0)

def get_admin_inputs_dict(_top1, _w1, root, mobility_manager):
    try:
        # Check if all required fields are filled
        name = _w1.AD_uniname_entry.get().strip()
        country = _w1.AD_country_entry.get().strip()
        city = _w1.AD_city_entry.get().strip()
        continent = _w1.AD_continent_menu.get().strip()
        mingrade = _w1.AD_mingrade_entry.get().strip()
        website = _w1.AD_web_entry.get().strip()
        latitude = _w1.AD_lat_entry.get().strip()
        longitude = _w1.AD_long_entry.get().strip()
        weather = _w1.AD_weather_entry.get().strip()
        rank = _w1.AD_rank_entry.get().strip()
        engrank = _w1.AD_engrank_entry.get().strip()
        cutoff = _w1.AD_cutoff_entry.get().strip()
        
        # Check for empty fields
        if not all([name, country, city, continent, mingrade, website, latitude, longitude, weather, rank, engrank, cutoff]):
            tk.messagebox.showerror("Missing Fields", "All fields must be filled before submission.")
            return None
        
        data = {
            "ID": _w1.AD_ID_entry.get(),
            "Name": _w1.AD_uniname_entry.get(),
            "Country": _w1.AD_country_entry.get(),
            "City": _w1.AD_city_entry.get(),
            "Continent": _w1.AD_continent_menu.get(),
            "Minimum grade": float(_w1.AD_mingrade_entry.get() or 0),
            "Website": _w1.AD_web_entry.get(),
            "Latitude": float(_w1.AD_lat_entry.get() or 0),
            "Longitude": float(_w1.AD_long_entry.get() or 0),
            "Spots available": int(_w1.AD_spots_scale.get()),
            "University Ranking": int(_w1.AD_rank_entry.get() or 0),
            "Engineering Ranking": int(_w1.AD_engrank_entry.get() or 0),
            "Weather": _w1.AD_weather_entry.get(),
            "Nightlife": int(_w1.AD_nightlife_scale.get()),
            "Cost of living": int(_w1.AD_cost_scale.get()),
            "Previous cutoff grade": float(_w1.AD_cutoff_entry.get() or 0),
            "Duration (months)": int(_w1.AD_duration_scale.get())
        }
        return data
    except ValueError as e:
        tk.messagebox.showerror("Format error", f"Numerical fields must contain valid numbers separated by a dot.")
        return None
    
def update_admin_uni_combobox(_top1, _w1, root, mobility_manager):
    _w1.AD_uni_combobox['values'] = mobility_manager.get_university_names()

def save_admin_entries(_top1, _w1, root, mobility_manager):
    if _w1.AD_uni_combobox.get() == "Select University":
        # Adding a new entry
        new_data = get_admin_inputs_dict()
        if new_data:
            # Generate a new unique ID
            new_data["ID"] = Utilities.generate_random_id()
            mobility_manager.add_entry(new_data)
            tk.messagebox.showinfo("Success", f"University '{new_data['Name']}' added with ID {new_data['ID']}.")
            update_admin_uni_combobox()

    elif _w1.AD_uni_combobox.get() != "Select University":
        # Editing an existing entry
        updated_data = get_admin_inputs_dict()
        if updated_data:
            mobility_manager.update_entry(updated_data["ID"], updated_data)
            tk.messagebox.showinfo("Success", f"University '{updated_data['Name']}' updated successfully.")
            update_admin_uni_combobox()

def delete_admin_entries(_top1, _w1, root, mobility_manager):
    uni_name = _w1.AD_uni_combobox.get()
    uni_data = mobility_manager.get_uni_by_name(uni_name)
    confirm = tk.messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete '{uni_name}'?")
    if confirm:
        mobility_manager.delete_entry(uni_data["ID"])
        tk.messagebox.showinfo("Deleted", f"University '{uni_name}' has been deleted.")
        clear_admin_entries()
        update_admin_uni_combobox()


def show_student_login(_top1, _w1, root, mobility_manager):
    """Toggle Student selection: show student buttons or deselect if already selected."""
    if _w1.auth_selection == 'student':
        # deselect: hide panel entirely
        _w1.auth_selection = None
        _w1.LG_sublabelframe.configure(text='')
        _w1.LG_sublabelframe.place_forget()
        _w1.LG_studentlogin_button.place_forget()
        _w1.LG_studentsingup_button.place_forget()
        _w1.LG_adminlogin_button.place_forget()
        _w1.LG_student_button.configure(style='Unselected.TButton')
        _w1.LG_admin_button.configure(style='Unselected.TButton')
        root.update_idletasks()
        return

    # select student
    _w1.auth_selection = 'student'
    _w1.LG_sublabelframe.place(relx=0.312, rely=0.466, relheight=0.388, relwidth=0.382)
    _w1.LG_sublabelframe.configure(text='Student')
    _w1.LG_studentlogin_button.place(relx=0.178, rely=0.772, height=56, width=125, bordermode='ignore')
    _w1.LG_studentsingup_button.place(relx=0.606, rely=0.772, height=56, width=125, bordermode='ignore')
    _w1.LG_adminlogin_button.place_forget()
    _w1.LG_student_button.configure(style='Selected.TButton')
    _w1.LG_admin_button.configure(style='Unselected.TButton')
    root.update_idletasks()

def show_admin_login(_top1, _w1, root, mobility_manager):
    """Toggle Admin selection: show admin login or deselect if already selected."""
    if _w1.auth_selection == 'admin':
        _w1.auth_selection = None
        _w1.LG_sublabelframe.configure(text='')
        _w1.LG_sublabelframe.place_forget()
        _w1.LG_adminlogin_button.place_forget()
        _w1.LG_studentlogin_button.place_forget()
        _w1.LG_studentsingup_button.place_forget()
        _w1.LG_student_button.configure(style='Unselected.TButton')
        _w1.LG_admin_button.configure(style='Unselected.TButton')
        root.update_idletasks()
        return

    # select admin
    _w1.auth_selection = 'admin'
    _w1.LG_sublabelframe.place(relx=0.312, rely=0.466, relheight=0.388, relwidth=0.382)
    _w1.LG_sublabelframe.configure(text='Admin')
    _w1.LG_adminlogin_button.place(relx=0.392, rely=0.772, height=56, width=125, bordermode='ignore')
    _w1.LG_studentlogin_button.place_forget()
    _w1.LG_studentsingup_button.place_forget()
    _w1.LG_admin_button.configure(style='Selected.TButton')
    _w1.LG_student_button.configure(style='Unselected.TButton')
    root.update_idletasks()

def show_student(_top1, _w1, root, mobility_manager):
    _w1.ST_bg.lift()

def show_admin(_top1, _w1, root, mobility_manager):
    _w1.AD_bg.lift()

def initialize_login_ui_state(_top1, _w1, root, mobility_manager):
    """Initialize auth selection state and button styles for the login screen."""
    _w1.auth_selection = None
    style = ttk.Style()
    try:
        style.configure('Unselected.TButton', background=_w1.THEME['UPF_red'], foreground='white')
        style.configure('Selected.TButton', background=_w1.THEME['BG_GREY'], foreground='black')
    except Exception:
        # Some themes ignore background; ensure foregrounds are set
        style.configure('Unselected.TButton', foreground='white')
        style.configure('Selected.TButton', foreground='black')

def show_login(_top1, _w1, root, mobility_manager):
    initialize_login_ui_state()
    _w1.LG_bg.lift()
    # Show selection buttons and form, hide all login buttons initially
    _w1.LG_student_button.place(relx=0.388, rely=0.323, height=86, width=125)
    _w1.LG_admin_button.place(relx=0.54, rely=0.323, height=86, width=125)
    # hide input panel by default (no selection)
    _w1.LG_sublabelframe.place_forget()
    _w1.LG_studentlogin_button.place_forget()
    _w1.LG_adminlogin_button.place_forget()
    _w1.LG_studentsingup_button.place_forget()
    _w1.LG_mail_entry.delete(0, tk.END)
    _w1.LG_pwd_entry.delete(0, tk.END)
    # default: no selection -> both top buttons shown as Unselected (red)
    try:
        _w1.LG_student_button.configure(style='Unselected.TButton')
        _w1.LG_admin_button.configure(style='Unselected.TButton')
    except Exception:
        pass
    root.update_idletasks()

def logout(_top1, _w1, root, mobility_manager):
    clear_admin_entries()
    _w1.AD_entries_frame.place_forget()
    _w1.AD_uni_combobox.set("Select University")
    show_login()
    check_uni_selection()

def check_uni_selection(_top1, _w1, root, mobility_manager):
    """Enable/disable Edit/Delete button based on combobox selection"""
    if _w1.AD_uni_combobox.get() == "Select University" or _w1.AD_uni_combobox.get() == "":
        _w1.AD_editdelete_button.config(state="disabled")
    else:
        _w1.AD_editdelete_button.config(state="normal")


# --- Authentication button handlers ---
def admin_login_action(_top1, _w1, root, mobility_manager):
    email = _w1.LG_mail_entry.get().strip()
    pwd = _w1.LG_pwd_entry.get().strip()
    if not email or not pwd:
        tk.messagebox.showerror("Missing fields", "Please enter email and password.")
        return
    # Prefer MobilityManager.verify_credentials if implemented
    if hasattr(mobility_manager, 'verify_credentials'):
        try:
            ok = mobility_manager.verify_credentials(email, pwd, 'admin')
        except Exception as e:
            tk.messagebox.showerror("Error", f"Error during auth: {e}")
            return
        if ok:
            show_admin()
        else:
            tk.messagebox.showerror("Authentication failed", "Invalid admin credentials.")
    else:
        # Fallback: simulate success
        tk.messagebox.showinfo("Not implemented", "verify_credentials not implemented yet — proceeding to Admin.")
        show_admin()

def student_login_action(_top1, _w1, root, mobility_manager):
    email = _w1.LG_mail_entry.get().strip()
    pwd = _w1.LG_pwd_entry.get().strip()
    if not email or not pwd:
        tk.messagebox.showerror("Missing fields", "Please enter email and password.")
        return
    if hasattr(mobility_manager, 'verify_credentials'):
        try:
            ok = mobility_manager.verify_credentials(email, pwd, 'student')
        except Exception as e:
            tk.messagebox.showerror("Error", f"Error during auth: {e}")
            return
        if ok:
            show_student()
        else:
            tk.messagebox.showerror("Authentication failed", "Invalid student credentials.")
    else:
        tk.messagebox.showinfo("Not implemented", "verify_credentials not implemented yet — proceeding to Student.")
        show_student()

def student_signup_action(_top1, _w1, root, mobility_manager):
    email = _w1.LG_mail_entry.get().strip()
    pwd = _w1.LG_pwd_entry.get().strip()
    if not email or not pwd:
        tk.messagebox.showerror("Missing fields", "Please enter email and password to sign up.")
        return
    # Check if email already exists
    if hasattr(mobility_manager, 'check_new_user_email'):
        try:
            if mobility_manager.check_new_user_email(email):
                tk.messagebox.showerror("Email exists", f"The email '{email}' is already registered.")
                return
        except Exception as e:
            tk.messagebox.showerror("Error", f"Error checking email: {e}")
            return
    # Call MobilityManager.add_user if available
    if hasattr(mobility_manager, 'add_user'):
        try:
            mobility_manager.add_user({
                'email': email,
                'password': pwd,
                'user_type': 'student'
            })
        except Exception as e:
            tk.messagebox.showerror("Error", f"Error creating user: {e}")
            return
        tk.messagebox.showinfo("Success", "Account created — proceeding to Student screen.")
        show_student()
    else:
        # Fallback: simulate user creation
        tk.messagebox.showinfo("Not implemented", "add_user not implemented yet — proceeding to Student.")
        show_student()
