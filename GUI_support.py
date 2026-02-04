# Import necessary libraries and modules
import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *
from tkinter import messagebox
import GUI
from MobilityManager import MobilityManager
import sys
import tkinter as tk
import GUI
import logic

def main(*args):
    '''Main entry point for the application.'''
    global root, _top1, _w1
    root = tk.Tk()
    root.protocol('WM_DELETE_WINDOW', root.destroy)

    # Initialize the GUI class
    _top1 = root
    _w1 = GUI.FrameBP(_top1)
    mobility_manager = MobilityManager("data/entries.csv") # Initialize MobilityManager with the data file
    mobility_manager.load_data()
    _w1.AD_uni_combobox['values'] = mobility_manager.get_university_names()

    def admin_editdelete():
        '''Function to edit or delete an existing university entry in the admin panel.'''
        uni_name = _w1.AD_uni_combobox.get() # Gets the selected university name from the combobox
        uni_data = mobility_manager.get_uni_by_name(uni_name) # Retrieves the university data (dict) based on the selected name

        if not uni_data: # Handles case where combobox selection is invalid (buggy behavior)
            tk.messagebox.showerror("Not found", f"University '{uni_name}' not found.")
            return

        # Places the entries frame and enables the delete button for editing/deleting
        _w1.AD_entries_frame.place(relx=0.244, rely=0.027, relheight=0.948, relwidth=0.741)
        _w1.AD_delete_button.config(state="normal")

        # Empty and then populate the admin entries with the selected university's data
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
    
    def clear_admin_entries():
        '''Function to clear all admin entries, used for ADD new university operation.'''
        _w1.AD_delete_button.config(state="disabled") # Disable delete button when adding new entry
        _w1.AD_entries_frame.place(relx=0.244, rely=0.027, relheight=0.948, relwidth=0.741)
        _w1.AD_uni_combobox.set("Select University")
        check_uni_selection() # Disables edit/delete button (forces to reselect university if needed) [KEY for Save button]

        # Clear all admin entry fields
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

    # Command assigments for Edit/Delete and Add buttons
    _w1.AD_editdelete_button.configure(command=admin_editdelete)    
    _w1.AD_add_button.configure(command=clear_admin_entries)

    def get_admin_inputs_dict():
        '''Function to retrieve admin input data as a dictionary. Validates required fields.'''
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
            
            # Data dictionary to return with proper datatype
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
        except ValueError as e: # Raises conversion errors for numerical fields and prevents submission
            tk.messagebox.showerror("Format error", f"Numerical fields must contain valid numbers separated by a dot.")
            return None
        
    def update_admin_uni_combobox():
        '''Function to refresh the admin university combobox values after add/edit/delete operations.'''
        _w1.AD_uni_combobox['values'] = mobility_manager.get_university_names()

    def save_admin_entries():
        '''Function to save admin entries, either adding a new entry or updating an existing one.'''
        if _w1.AD_uni_combobox.get() == "Select University": # If no university is selected, we are adding a new entry
            # Adding a new entry
            new_data = get_admin_inputs_dict()
            if new_data:
                # Generate a new unique ID
                new_data["ID"] = logic.Utilities.generate_random_id()
                mobility_manager.add_entry(new_data) # Calls data handler to add the new entry to database
                tk.messagebox.showinfo("Success", f"University '{new_data['Name']}' added with ID {new_data['ID']}.")
                update_admin_uni_combobox()

        elif _w1.AD_uni_combobox.get() != "Select University": # If a university is selected, we are editing an existing entry
            # Editing an existing entry
            updated_data = get_admin_inputs_dict()
            if updated_data:
                mobility_manager.update_entry(updated_data["ID"], updated_data) # Calls data handler to update the existing entry in database
                tk.messagebox.showinfo("Success", f"University '{updated_data['Name']}' updated successfully.")
                update_admin_uni_combobox()

    def delete_admin_entries():
        '''Function to delete the selected university entry in the admin panel.'''
        uni_name = _w1.AD_uni_combobox.get()
        uni_data = mobility_manager.get_uni_by_name(uni_name)
        confirm = tk.messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete '{uni_name}'?") # Asks for confirmation
        if confirm:
            mobility_manager.delete_entry(uni_data["ID"]) # Calls data handler to delete the entry from database
            tk.messagebox.showinfo("Deleted", f"University '{uni_name}' has been deleted.")
            clear_admin_entries()
            update_admin_uni_combobox()

    # Assign commands to Save and Delete buttons
    _w1.AD_save_button.configure(command=save_admin_entries)
    _w1.AD_delete_button.configure(command=delete_admin_entries)

    def add_language():
        lang = _w1.lang_var.get()
        
        if lang == "Select Language" or lang == "" or lang in _w1.added_languages:
            return
        
        # Limit to 8 languages total (4 rows x 2 columns)
        count = len(_w1.added_languages)
        if count >= 8:
            tk.messagebox.showwarning("Limit Reached", "You can only add up to 8 languages.")
            return

        # Calculate Grid Position: 0-3 rows, 0-1 columns
        grid_row = count % 4
        grid_col = count // 4

        # Container for this specific language entry
        row_frame = tk.Frame(_w1.ST_lang_frame, background=_w1.THEME["BG_GREY"])
        row_frame.grid(row=grid_row, column=grid_col, sticky="nsew", padx=2, pady=1)

        # 1. Language Name (Smaller width to fit 2 columns)
        lbl = tk.Label(row_frame, text=lang, background=_w1.THEME["BG_GREY"], 
                       foreground=_w1.THEME["TEXT_DARK"], width=8, anchor="w")
        lbl.pack(side="left", padx=2)

        # 2. Level Selector
        level_var = tk.StringVar(value="B1")
        cb = ttk.Combobox(row_frame, values=["B1", "B2", "C1", "C2"], 
                          textvariable=level_var, width=4, state="readonly")
        cb.pack(side="left", padx=2)

        # 3. Remove Button
        btn_remove = tk.Button(row_frame, text="x", fg="red", relief="flat", 
                               background=_w1.THEME["BG_GREY"], font=("Arial", 8),
                               command=lambda l=lang, r=row_frame: remove_language(l, r))
        btn_remove.pack(side="right", padx=2)

        _w1.added_languages[lang] = [row_frame, cb]

    def remove_language(lang, row_frame):
        row_frame.destroy()
        del _w1.added_languages[lang]
        # Optional: Redraw remaining to fill gaps (if you want them to shift back)
        # But for simplicity, leaving a gap is fine in a grid.

    # Link the existing Add button from GUI.py to our function
    _w1.ST_lang_button.configure(command=add_language)

    # Navigation logic
    def show_student():
        '''Function to show the Student screen.'''
        _w1.ST_bg.lift()

    def show_admin():
        '''Function to show the Admin screen.'''
        _w1.AD_bg.lift()

    def show_login():
        '''Function to show the Login screen.'''
        _w1.LG_bg.lift()

    def logout(): # MUST BE COMPLETED
        """Function to handle logout from Student or Admin screens."""
        clear_admin_entries()
        _w1.AD_entries_frame.place_forget()
        _w1.AD_uni_combobox.set("Select University")
        show_login()
        check_uni_selection()

    def check_uni_selection():
        """Enable/disable Edit/Delete button based on combobox selection"""
        if _w1.AD_uni_combobox.get() == "Select University" or _w1.AD_uni_combobox.get() == "":
            _w1.AD_editdelete_button.config(state="disabled")
        else:
            _w1.AD_editdelete_button.config(state="normal")

    # --- PREFERENCES LOGIC (4 ENTRIES) ---
    # Omitted "Engineering Rank"
    preferences_data = ["Cost of Living", "Nightlife", "Weather", "Academic Rank"]

    def update_pref_ui():
        """Updates the text and button states for the 4 existing rows."""
        for i in range(4):
            # Update Label text
            _w1.pref_labels[i].config(text=f"{i+1}. {preferences_data[i]}")
            
            # Update Down button: disabled if at index 3 (the new bottom)
            _w1.pref_down_btns[i].config(
                command=lambda idx=i: move_pref(idx, 1),
                state="disabled" if i == 3 else "normal"
            )
            
            # Update Up button: disabled if at index 0
            _w1.pref_up_btns[i].config(
                command=lambda idx=i: move_pref(idx, -1),
                state="disabled" if i == 0 else "normal"
            )

    def move_pref(index, direction):
        """Swaps the data and refreshes the UI labels."""
        new_index = index + direction
        preferences_data[index], preferences_data[new_index] = preferences_data[new_index], preferences_data[index]
        update_pref_ui()

    # Initial call to populate the 4 items
    update_pref_ui()
    
    # Links combobox selection to check function to enable edit/delete button
    _w1.AD_uni_combobox.bind('<<ComboboxSelected>>', lambda e: check_uni_selection())

    # Link Login Screen Buttons
    _w1.LG_student_button.configure(command=show_student)
    _w1.LG_admin_button.configure(command=show_admin)

    # Link Logout Buttons
    _w1.ST_logout_button.configure(command=logout)
    _w1.AD_logout_button.configure(command=logout)

    # Set the initial view to the Login screen
    show_login()
    check_uni_selection()

    root.mainloop()

if __name__ == '__main__':
    GUI.start_up()
    