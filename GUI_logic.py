# GUI_logic.py
# This module contains the logic for handling GUI interactions, such as button clicks and form submissions.
# That way, the main.py file can focus on initializing the GUI and linking the logic, while this module focuses on the actual behavior of the application.

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from utilities import Utilities
from user import Student
# we need university catalog and scoring engine for ranking; imported here to avoid circular imports
from university import Catalog
from scoringEngine import ScoringEngine
from scoringEngine import ScoringEngine

# For image handling
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

# For map display
try:
    import tkintermapview
    MAP_AVAILABLE = True
except ImportError:
    MAP_AVAILABLE = False

# For opening websites
import webbrowser

# Global variable to store the current logged-in student instance
current_student = None
# Global variable to store the current displayed university for the "More Info" section
current_university = None
current_photo = None  # Keep reference to prevent garbage collection
# Store ranked universities for the "More Info" buttons
ranked_universities_display = {}  # Maps row number (1-10) to (university, score) tuple


def display_university_info(_w1, university_obj):
    """Display university information in the ST_facts_frame section.
    
    Updates all the GUI labels with information from the university object,
    including name, city, country, and various statistics.
    """
    global current_university, current_photo
    
    if university_obj is None:
        return
    
    # Show the stats frame
    _w1.ST_facts_frame.place(relx=0.319, rely=0.683, relheight=0.281, relwidth=0.668)
    
    current_university = university_obj
    
    # Get university information
    uni_name = university_obj.get_uni_att('name') or "N/A"
    location = university_obj.get_uni_att('location')
    city = ""
    country = ""
    continent = ""
    if location and hasattr(location, 'get_city'):
        city = location.get_city() or ""
        country = location.get_country() or ""
        continent = location.get_continent() or ""
    
    # Update university name and location
    uni_display = f"{uni_name}, {city}, {country}"
    _w1.ST_uniname_label.configure(text=uni_display)
    
    # Get and display statistics using available attributes
    ranking = university_obj.get_uni_att('ranking')
    cost = university_obj.get_uni_att('cost_of_living')
    nightlife = university_obj.get_uni_att('nightlife')
    cutoff = university_obj.get_uni_att('cutoff_grade')
    weather = university_obj.get_uni_att('weather')
    min_grade = university_obj.get_uni_att('grade')
    spots = university_obj.get_uni_att('spots')
    
    _w1.ST_stat11_label.configure(text=f"Academic Ranking\n{ranking or 'N/A'}")
    _w1.ST_stat12_label.configure(text=f"Cost of Living\n{cost or 'N/A'}")
    _w1.ST_stat13_label.configure(text=f"Nightlife\n{nightlife or 'N/A'}")
    _w1.ST_stat23_label.configure(text=f"Cutoff Grade\n{cutoff or 'N/A'}")
    
    # Use available fields for the remaining labels
    _w1.ST_stat21_label.configure(text=f"Minimum Grade\n{min_grade or 'N/A'}")
    _w1.ST_stat14_label.configure(text=f"Spots\n{spots or 'N/A'}")
    _w1.ST_stat24_label.configure(text=f"Continent\n{continent or 'N/A'}")
    _w1.ST_stat22_label.configure(text=f"Weather\n{weather or 'N/A'}")
    
    # Load and display logo
    logo_path = university_obj.get_logo_path()
    if PIL_AVAILABLE and logo_path:
        try:
            img = Image.open(logo_path)
            img.thumbnail((160, 160), Image.Resampling.LANCZOS)
            current_photo = ImageTk.PhotoImage(img)
            _w1.ST_logo_label.configure(image=current_photo, text="")
        except Exception as e:
            print(f"Could not load logo from {logo_path}: {e}")
            _w1.ST_logo_label.configure(image="", text="Logo not found")
    else:
        _w1.ST_logo_label.configure(image="", text="Logo not available")


def show_university_map():
    """Display a map popup showing the currently selected university's location.
    
    Creates a new window with a TkinterMapView centered on the Mediterranean,
    with a marker at the university's coordinates.
    """
    global current_university
    
    if current_university is None:
        messagebox.showwarning("No Selection", "Please select a university first using the More Info button.")
        return
    
    if not MAP_AVAILABLE:
        messagebox.showerror("Map Not Available", "TkinterMapView library is not installed.")
        return
    
    # Get university location
    location = current_university.get_uni_att('location')
    if not location:
        messagebox.showerror("No Location", "University location data not available.")
        return
    
    # Extract coordinates
    if isinstance(location, dict):
        coords = location.get('coords', [None, None])
        uni_name = current_university.get_uni_att('name') or "University"
    elif hasattr(location, 'get_coords'):
        coords = location.get_coords()
        uni_name = current_university.get_uni_att('name') or "University"
    else:
        messagebox.showerror("No Coordinates", "Location coordinates not available.")
        return
    
    lat, lon = coords if coords else [None, None]
    
    if lat is None or lon is None:
        messagebox.showerror("Invalid Coordinates", "University coordinates are not valid.")
        return
    
    # Create popup window
    map_window = tk.Toplevel()
    map_window.title(f"Map - {uni_name}")
    map_window.geometry("800x600")
    
    try:
        # Create map widget
        map_widget = tkintermapview.TkinterMapView(map_window)
        map_widget.pack(fill="both", expand=True)
        
        # Center on Mediterranean (zoom out view)
        map_widget.set_position(35, 15)
        map_widget.set_zoom(2)
        
        # Add marker at university location
        try:
            lat = float(lat)
            lon = float(lon)
            map_widget.set_marker(lat, lon, text=uni_name)
        except (ValueError, TypeError):
            messagebox.showerror("Invalid Coordinates", f"Cannot plot coordinates: {lat}, {lon}")
            map_window.destroy()
            return
            
    except Exception as e:
        messagebox.showerror("Map Error", f"Error displaying map: {e}")
        map_window.destroy()
        return


def open_university_website():
    """Open the currently selected university's website in the default browser."""
    global current_university
    
    if current_university is None:
        messagebox.showwarning("No Selection", "Please select a university first using the More Info button.")
        return
    
    # Get university website URL
    website_url = current_university.get_uni_att('website_url')
    print(f"Raw website URL: {website_url}")
    
    if not website_url or website_url.strip() == "":
        messagebox.showerror("No Website", "Website URL not available for this university.")
        return
    
    # Clean and ensure URL has proper protocol
    website_url = website_url.strip()
    if not website_url.startswith(('http://', 'https://')):
        website_url = 'https://' + website_url
    
    print(f"Opening website: {website_url}")
    try:
        result = webbrowser.open(website_url)
        print(f"Webbrowser open result: {result}")
        if not result:
            messagebox.showwarning("Warning", "Could not open browser. Please check your default browser settings.")
    except Exception as e:
        messagebox.showerror("Error", f"Could not open website: {e}")
        print(f"Error opening website: {e}")


def export_rankings_pdf(_w1, catalog: Catalog | None = None, engine: ScoringEngine | None = None):
    """Handler for the Export button.  Prompts for save location and
    writes a minimal PDF containing the top‑10 ranked universities."""
    global current_student
    from tkinter.filedialog import asksaveasfilename

    if current_student is None:
        messagebox.showwarning("No Student", "No student is logged in.")
        return
    if catalog is None or engine is None:
        messagebox.showwarning("Unavailable", "Catalog/engine not provided.")
        return

    # ensure student info up to date
    current_student.save_to_csv()

    catalog.load()
    ranked = catalog.rank(current_student, engine)
    if not ranked:
        messagebox.showinfo("Empty", "No universities to export.")
        return

    path = asksaveasfilename(defaultextension=".pdf",
                             filetypes=[("PDF files", "*.pdf")],
                             title="Save ranking as PDF")
    if not path:
        return

    try:
        Utilities.export_ranking_pdf(ranked, path)
        messagebox.showinfo("Exported", f"Ranking exported to {path}")
    except Exception as e:
        messagebox.showerror("Export Error", f"Failed to create PDF: {e}")



def admin_editdelete(_w1, mobility_manager):
    '''Inputs the selected university data into the admin fields so the admin can edit them or delete the entry.'''
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
    _w1.AD_english_combobox.set(uni_data["English"])
    _w1.AD_spanish_combobox.set(uni_data["Spanish"])
    _w1.AD_french_combobox.set(uni_data["French"])
    _w1.AD_german_combobox.set(uni_data["German"])
    _w1.AD_portuguese_combobox.set(uni_data["Portuguese"])
    _w1.AD_chinese_combobox.set(uni_data["Chinese"])
    _w1.AD_japanese_combobox.set(uni_data["Japanese"])
    _w1.AD_italian_combobox.set(uni_data["Italian"])

def clear_admin_entries(_w1):
    '''Clears the admin entries so the admin can add a new university from scratch.'''
    _w1.AD_delete_button.config(state="disabled")
    _w1.AD_entries_frame.place(relx=0.244, rely=0.027, relheight=0.948, relwidth=0.741)
    _w1.AD_uni_combobox.set("Select University")
    check_uni_selection(_w1)

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
    _w1.AD_english_combobox.set("")
    _w1.AD_spanish_combobox.set("")
    _w1.AD_french_combobox.set("")
    _w1.AD_german_combobox.set("")
    _w1.AD_portuguese_combobox.set("")
    _w1.AD_chinese_combobox.set("")
    _w1.AD_japanese_combobox.set("")
    _w1.AD_italian_combobox.set("")

def get_admin_inputs_dict(_w1):
    '''Gets the admin inputs as a dictionary'''
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
            "Duration (months)": int(_w1.AD_duration_scale.get()),
            "English": _w1.AD_english_combobox.get(),
            "Spanish": _w1.AD_spanish_combobox.get(),
            "French": _w1.AD_french_combobox.get(),
            "German": _w1.AD_german_combobox.get(),
            "Portuguese": _w1.AD_portuguese_combobox.get(),
            "Chinese": _w1.AD_chinese_combobox.get(),
            "Japanese": _w1.AD_japanese_combobox.get(),
            "Italian": _w1.AD_italian_combobox.get()
        }
        return data
    except ValueError as e:
        tk.messagebox.showerror("Format error", f"Numerical fields must contain valid numbers separated by a dot.")
        return None
    
def update_admin_uni_combobox(_w1, mobility_manager):
    '''Updates the combobox for universities after adding/editing/deleting entries'''
    _w1.AD_uni_combobox['values'] = mobility_manager.get_university_names()

def save_admin_entries(_w1, mobility_manager):
    if _w1.AD_uni_combobox.get() == "Select University":
        # Adding a new entry
        new_data = get_admin_inputs_dict(_w1)
        if new_data:
            # Generate a new unique ID
            new_data["ID"] = Utilities.generate_random_id()
            mobility_manager.add_entry(new_data)
            tk.messagebox.showinfo("Success", f"University '{new_data['Name']}' added with ID {new_data['ID']}.")
            update_admin_uni_combobox(_w1, mobility_manager)

    elif _w1.AD_uni_combobox.get() != "Select University":
        # Editing an existing entry
        updated_data = get_admin_inputs_dict(_w1)
        if updated_data:
            mobility_manager.update_entry(updated_data["ID"], updated_data)
            tk.messagebox.showinfo("Success", f"University '{updated_data['Name']}' updated successfully.")
            update_admin_uni_combobox(_w1, mobility_manager)

def delete_admin_entries(_w1, mobility_manager):
    uni_name = _w1.AD_uni_combobox.get()
    uni_data = mobility_manager.get_uni_by_name(uni_name)
    confirm = tk.messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete '{uni_name}'?")
    if confirm:
        mobility_manager.delete_entry(uni_data["ID"])
        tk.messagebox.showinfo("Deleted", f"University '{uni_name}' has been deleted.")
        clear_admin_entries(_w1)
        update_admin_uni_combobox(_w1, mobility_manager)

#______________________________________________STUDENT PAGE LOGIC_____________________________________________________

def add_language_row(_w1, language=None):
    '''
    Handles adding languages in the student languages frame dynamically.
    If ``language`` is provided it is used directly, otherwise the current
    value of ``_w1.lang_var`` (the combobox) is read.  A label for the
    language, a combobox for the certification level and a delete button are
    placed.  The layout uses two columns to avoid scrolling when several
    languages are present (maximum eight supported).
    '''
    # determine which language to add
    selected_lang = language if language is not None else _w1.lang_var.get()
    if selected_lang == "Select Language" or selected_lang in _w1.added_languages:
        return
    current_count = len(_w1.added_languages)
    if current_count >= 8:
        return
    row_frame = tk.Frame(_w1.ST_lang_frame, background=_w1.THEME["BG_GREY"])
    if current_count < 4:
        target_column = 0
        target_row = current_count
    else:
        target_column = 1
        target_row = current_count - 4
    row_frame.grid(row=target_row, column=target_column, sticky="w", padx=5, pady=2)

    tk.Label(row_frame, text=selected_lang, width=8, anchor="w", 
             background=_w1.THEME["BG_GREY"]).pack(side="left")
    level_var = tk.StringVar(value="B2")
    ttk.Combobox(row_frame, values=["B1", "B2", "C1", "C2"], 
                 textvariable=level_var, state="readonly", width=4).pack(side="left", padx=2)
    tk.Button(row_frame, text="X", bg="#ff4d4d", fg="white", bd=0,
              command=lambda: remove_language_row(_w1, selected_lang)).pack(side="left", padx=5)
    _w1.added_languages[selected_lang] = [row_frame, level_var]
    # reset the language selector for convenience
    try:
        _w1.lang_var.set('Select Language')
    except Exception:
        # some callers may not want to modify the combobox state
        pass
    # additionally clear any visual selection and move focus away so the
    # combobox does not stay highlighted (blue box)
    try:
        _w1.ST_lang_menu.selection_clear()
        _w1.ST_grade_entry.focus_set()
    except Exception:
        pass

def remove_language_row(_w1, lang_name):
    '''Deletes a language'''
    # Simply find the frame in our dictionary and destroy it
    if lang_name in _w1.added_languages:
        widgets = _w1.added_languages.pop(lang_name)
        widgets[0].destroy()

def move_pref_up(_w1, row_num):
    '''Moves a preference up in the hierearchy (only changing the visual labels)'''
    # We can only move up if we aren't at the top (Row 1)
    if row_num <= 1:
        return
    current_label = getattr(_w1, f"pref_label{row_num}")
    above_label = getattr(_w1, f"pref_label{row_num-1}")
    current_text = current_label.cget("text")
    above_text = above_label.cget("text")

    # Swap their texts (but not numbers)
    name_current = current_text.split(". ")[1]
    name_above = above_text.split(". ")[1]
    current_label.configure(text=f"{row_num}. {name_above}")
    above_label.configure(text=f"{row_num-1}. {name_current}")

def move_pref_down(_w1, row_num):
    '''Moves a preference down in the hierearchy (only changing the visual labels)'''
    # We can only move down if we aren't at the bottom (Row 4)
    if row_num >= 4:
        return
    current_label = getattr(_w1, f"pref_label{row_num}")
    below_label = getattr(_w1, f"pref_label{row_num+1}")
    current_text = current_label.cget("text")
    below_text = below_label.cget("text")

    # swap the descriptive portion but keep the numbers attached to the rows
    name_current = current_text.split(". ")[1]
    name_below = below_text.split(". ")[1]
    current_label.configure(text=f"{row_num}. {name_below}")
    below_label.configure(text=f"{row_num+1}. {name_current}")


def clear_student_page(_w1):
    """
    Clear all student page widgets and reset them to default state.
    This ensures a clean form when switching between users.
    """
    # Hide ranking and stats frames
    _w1.ScrolledwindowRUP.place_forget()
    _w1.ST_facts_frame.place_forget()
    
    # Clear degree
    _w1.degree_var.set('Select Degree')
    
    # Clear grade
    _w1.ST_grade_entry.delete(0, tk.END)
    
    # Clear all added languages
    for lang_frame, level_var in _w1.added_languages.values():
        lang_frame.destroy()
    _w1.added_languages.clear()
    
    # Clear continent checkboxes
    _w1.var_EU.set(0)
    _w1.var_NA.set(0)
    _w1.var_AS.set(0)
    _w1.var_SA.set(0)
    _w1.var_OC.set(0)
    _w1.var_AF.set(0)
    
    # Reset preference labels
    _w1.pref_label1.config(text="1. Cost of Living")
    _w1.pref_label2.config(text="2. Weather")
    _w1.pref_label3.config(text="3. Nightlife")
    _w1.pref_label4.config(text="4. Academic Rank")
    
    # Clear language menu
    # use the same placeholder used when the GUI is first created
    _w1.lang_var.set('Select Language')

def populate_student_page_from_profile(_w1, student):
    """
    Populate student page widgets with the student's saved profile data.
    This is called after login to restore a student's previous entries.
    Kept simple to avoid any unintended triggers.
    """
    try:
        # Set degree
        degree = student.get_degree()
        if degree and degree != "":
            _w1.degree_var.set(degree)
        
        # Set grade
        grade = student.get_grade()
        if grade and grade != 0.0 and grade != "":
            _w1.ST_grade_entry.delete(0, tk.END)
            _w1.ST_grade_entry.insert(0, str(grade))
        
        # Set languages by adding rows for each saved language
        langs = student.get_languages()
        if langs:
            for lang, level in langs.items():
                # Add the language row with explicit language name so the
                # label does not end up empty (combobox may not yet have the
                # correct value during profile restoration).
                add_language_row(_w1, language=lang)
                # Set the level on the newly added row
                if lang in _w1.added_languages:
                    frame, level_var = _w1.added_languages[lang]
                    level_var.set(level)
        
        # Set continents
        continents = student.get_continents()
        continent_mapping = {
            "Europe": _w1.var_EU,
            "North America": _w1.var_NA,
            "Asia": _w1.var_AS,
            "South America": _w1.var_SA,
            "Oceania": _w1.var_OC,
            "Africa": _w1.var_AF,
        }
        for continent, var in continent_mapping.items():
            if continent in continents:
                var.set(1)
            else:
                var.set(0)
        
        # Set preferences
        preferences = student.get_preferences()
        if preferences:
            pref_fields = ['Cost of Living', 'Weather', 'Nightlife', 'Academic Rank']
            for i, pref in enumerate(preferences):
                if i < 4:
                    label = getattr(_w1, f"pref_label{i+1}")
                    label.config(text=f"{i+1}. {pref}")
        # Ensure language combobox is visually cleared after populating
        try:
            _w1.lang_var.set('Select Language')
            _w1.ST_lang_menu.selection_clear()
            _w1.ST_grade_entry.focus_set()
        except Exception:
            pass
    
    except Exception as e:
        print(f"Error populating student page: {e}")

def get_score_color(score):
    """
    Map affinity score to a color for visualization.
    100: green, 80: lime, 60: yellow, 40: orange, 20: dark orange, 0: red
    """
    if score >= 90:
        return "#00cc00"  # green
    elif score >= 70:
        return "#ccff00"  # lime
    elif score >= 50:
        return "#ffff00"  # yellow
    elif score >= 30:
        return "#ff8800"  # orange
    elif score >= 10:
        return "#ff6600"  # dark orange
    else:
        return "#ff0000"  # red

def rank_button_action(_w1, catalog: Catalog | None = None, engine: ScoringEngine | None = None):
    """
    Handle the Rank! button click silently. This function:
    1. Loads the student data from the GUI into the current_student instance
    2. Validates that all required student fields are filled
    3. Saves the student data to CSV
    4. Instantiates/uses a Catalog to load university objects and prints them
       (minimal proof-of-concept until the scoring engine is hooked up)

    The ``catalog`` parameter is optional; if provided (e.g. by main.py) the
    same instance will be reused.  If it is ``None`` the function will still
    behave normally but no catalog operations will occur.
    """
    global current_student

    if current_student is None:
        return

    try:
        # Load current GUI values into the student instance
        current_student.load_from_gui(_w1)

        # Validate required fields
        degree = current_student.get_degree()
        grade = current_student.get_grade()
        lang = current_student.get_languages()
        continents = current_student.get_continents()
        preferences = current_student.get_preferences()

        # Check required fields - silently return if any missing
        if not degree or degree == "" or degree == "Select Degree":
            tk.messagebox.showerror("Missing field", "Please select a degree.")
            return

        if grade == 0.0 or grade == "":
            tk.messagebox.showerror("Missing field", "Please enter a valid grade.")
            return

        if not lang or len(lang) == 0:
            tk.messagebox.showerror("Missing field", "Please select at least one language.")
            return

        if not continents or len(continents) == 0:
            tk.messagebox.showerror("Missing field", "Please select at least one continent.")
            return

        if not preferences or len(preferences) == 0:
            tk.messagebox.showerror("Missing field", "Please select and rank your preferences.")
            return

        # Save to CSV (silently)
        current_student.save_to_csv()

        # print student preferences to show their structure
        print("--- student preferences ---")
        print(preferences)
        print("--- end student preferences ---")

        # Get ranked universities
        if catalog is not None and engine is not None:
            global ranked_universities_display
            
            # Show the ranking frame
            _w1.ScrolledwindowRUP.place(relx=0.319, rely=0.06, relheight=0.606, relwidth=0.668)
            
            catalog.load()
            ranked_universities = catalog.rank(current_student, engine)
            
            # Separate available (score > 0) and unavailable (score == 0)
            available = [(uni, score) for uni, score in ranked_universities if score > 0]
            unavailable = [(uni, score) for uni, score in ranked_universities if score == 0]
            
            # Clear previous storage
            ranked_universities_display = {}
            
            # Display first 10: available first, then random unavailable
            import random
            for i in range(10):
                if i < len(available):
                    uni, score = available[i]
                    uni_name = uni.get_uni_att('name')
                    is_available = True
                elif unavailable:
                    # Pick random unavailable
                    uni, score = random.choice(unavailable)
                    uni_name = uni.get_uni_att('name')
                    is_available = False
                else:
                    # No more options
                    uni_name = "No more options available"
                    score = 0.0
                    is_available = False
                    uni = None
                
                # Update GUI labels
                uni_label = getattr(_w1, f'ST_rankrow{i+1}_uniname_label')
                score_label = getattr(_w1, f'ST_rankrow{i+1}_score_label')
                action_button = getattr(_w1, f'ST_rankrow{i+1}_button')
                
                uni_label.configure(text=uni_name)
                score_label.configure(text=f'{score:.2f}')
                
                # Set color based on availability
                if is_available:
                    uni_label.configure(foreground="black")
                    # Apply colormap to score label with bold black text
                    score_color = get_score_color(score)
                    score_label.configure(foreground="black", background=score_color, font="{Lexend} 10 bold", padx=5, pady=2)
                    action_button.configure(state='normal')
                    # Store university for button callback
                    ranked_universities_display[i + 1] = uni
                    # Bind button to display this university's info
                    action_button.configure(command=lambda u=uni, w=_w1: display_university_info(w, u))
                else:
                    uni_label.configure(foreground=_w1.THEME["DISABLED_GREY"])
                    score_label.configure(foreground=_w1.THEME["DISABLED_GREY"], background=_w1.THEME["BG_GREY"], font="{Lexend} 10")
                    action_button.configure(state='disabled')
                    
    except Exception as e:
        print(f"Error during ranking process: {e}")

def save_student_profile(_w1):
    """
    Save the current student's profile data from GUI to CSV.
    This should be called before ranking or whenever student data is updated.
    Updates the global current_student with GUI values and saves to CSV.
    """
    global current_student
    
    if current_student is None:
        tk.messagebox.showerror("Error", "No student logged in. Please log in first.")
        return False
    
    try:
        # Load current GUI values into the student instance
        current_student.load_from_gui(_w1)
        
        # Save to CSV
        current_student.save_to_csv()
        
        tk.messagebox.showinfo("Success", "Profile saved successfully!")
        return True
    except Exception as e:
        tk.messagebox.showerror("Error", f"Error saving profile: {e}")
        return False

def print_student_attributes(gui_frame):
    """Create a temporary Student object, populate it from the GUI and
    print all of its stored attributes to stdout.

    This can be used as the command for the "Rank !" button during
    development to verify that the GUI state is being captured correctly.
    
    Validates that all required fields are filled before proceeding.
    """
    from user import Student

    # instantiate with dummy credentials; they're not used here
    student = Student("", "", "")
    student.load_from_gui(gui_frame)

    # Validate required fields
    degree = student.get_stud_att("degree")
    grade = student.get_stud_att("grade")
    lang = student.get_stud_att("lang")
    continents = student.get_stud_att("continents")

    # Check degree
    if not degree or degree == "Select Degree":
        messagebox.showerror("Missing Data", "Please select a degree.")
        return

    # Check grade is valid number
    if grade is None or grade == 0.0:
        messagebox.showerror("Missing Data", "Please enter a valid grade (number).")
        return

    # Check at least one language
    if not lang or len(lang) == 0:
        messagebox.showerror("Missing Data", "Please select at least one language certification.")
        return

    # Check at least one continent
    if not continents or len(continents) == 0:
        messagebox.showerror("Missing Data", "Please select at least one continent.")
        return

    # All validations passed, print data
    attrs = ["degree", "grade", "lang", "continents", "preferences"]
    print("--- student data ---")
    for a in attrs:
        print(f"{a}: {student.get_stud_att(a)}")
    print("--------------------")

#_________________________________________________LOGIN LOGIC_________________________________________________________

def show_student_login(_w1, root):
    """Toggle Student selection: show student buttons or deselect if already selected."""
    if _w1.auth_selection == 'student':
        # deselect: hide panel entirely
        _w1.auth_selection = None
        _w1.LG_sublabelframe.configure(text='')
        _w1.LG_sublabelframe.place_forget()
        _w1.LG_studentlogin_button.place_forget()
        _w1.LG_studentsingup_button.place_forget()
        _w1.LG_adminlogin_button.place_forget()
        try:
            _w1.LG_student_button.configure(style='Unselected.TButton')
            _w1.LG_admin_button.configure(style='Unselected.TButton')
        except Exception:
            # fallback for tk.Button which does not support ttk styles
            _w1.LG_student_button.configure(background=_w1.THEME["UPF_red"], foreground="white")
            _w1.LG_admin_button.configure(background=_w1.THEME["UPF_red"], foreground="white")
        root.update_idletasks()
        return

    # select student
    _w1.auth_selection = 'student'
    _w1.LG_sublabelframe.place(relx=0.312, rely=0.466, relheight=0.388, relwidth=0.382)
    _w1.LG_sublabelframe.configure(text='Student')
    _w1.LG_studentlogin_button.place(relx=0.178, rely=0.772, height=56, width=125, bordermode='ignore')
    _w1.LG_studentsingup_button.place(relx=0.606, rely=0.772, height=56, width=125, bordermode='ignore')
    _w1.LG_adminlogin_button.place_forget()
    try:
        _w1.LG_student_button.configure(style='Selected.TButton')
        _w1.LG_admin_button.configure(style='Unselected.TButton')
    except Exception:
        _w1.LG_student_button.configure(background=_w1.THEME["BG_GREY"], foreground="black")
        _w1.LG_admin_button.configure(background=_w1.THEME["UPF_red"], foreground="white")
    root.update_idletasks()

def show_admin_login(_w1, root):
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
    try:
        _w1.LG_admin_button.configure(style='Selected.TButton')
        _w1.LG_student_button.configure(style='Unselected.TButton')
    except Exception:
        _w1.LG_admin_button.configure(background=_w1.THEME["BG_GREY"], foreground="black")
        _w1.LG_student_button.configure(background=_w1.THEME["UPF_red"], foreground="white")
    root.update_idletasks()

def show_student(_w1):
    _w1.ST_bg.lift()

def show_admin(_w1):
    _w1.AD_bg.lift()

def initialize_login_ui_state(_w1):
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

def show_login(_w1, root):
    initialize_login_ui_state(_w1)
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

def logout(_w1, root):
    global current_student
    # Save student data before logout if a student is logged in.
    # Make sure GUI current values are loaded into the Student instance
    # (same behavior as the Rank action) before persisting.
    if current_student is not None:
        try:
            current_student.load_from_gui(_w1)
        except Exception:
            pass
        try:
            current_student.save_to_csv()
        except Exception:
            pass
        current_student = None
    
    # Clear all student page widgets
    clear_student_page(_w1)
    
    clear_admin_entries(_w1)
    _w1.AD_entries_frame.place_forget()
    _w1.AD_uni_combobox.set("Select University")
    show_login(_w1, root)
    check_uni_selection(_w1)

def check_uni_selection(_w1):
    """Enable/disable Edit/Delete button based on combobox selection"""
    if _w1.AD_uni_combobox.get() == "Select University" or _w1.AD_uni_combobox.get() == "":
        _w1.AD_editdelete_button.config(state="disabled")
    else:
        _w1.AD_editdelete_button.config(state="normal")

#_____________________________________________AUTHENTICATION BUTTON HANDLERS____________________________________________

def admin_login_action(_w1, mobility_manager):
    email = _w1.LG_mail_entry.get().strip()
    pwd = _w1.LG_pwd_entry.get().strip()
    if not email or not pwd:
        tk.messagebox.showerror("Missing fields", "Please enter email and password.")
        return
    # Prefer mobilityManager.verify_credentials if implemented
    if hasattr(mobility_manager, 'verify_credentials'):
        try:
            ok = mobility_manager.verify_credentials(email, pwd, 'admin')
        except Exception as e:
            tk.messagebox.showerror("Error", f"Error during auth: {e}")
            return
        if ok:
            show_admin(_w1)
        else:
            tk.messagebox.showerror("Authentication failed", "Invalid admin credentials.")
    else:
        # Fallback: simulate success
        tk.messagebox.showinfo("Not implemented", "verify_credentials not implemented yet — proceeding to Admin.")
        show_admin(_w1)

def student_login_action(_w1, mobility_manager):
    global current_student
    
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
            # Get user data including UID
            user_data = mobility_manager.get_user_by_credentials(email, pwd, 'student')
            if user_data:
                # Clear student page first
                clear_student_page(_w1)
                
                # Create a Student instance
                uid = user_data.get('UID')
                current_student = Student(uid, email, pwd)
                
                # Load student data from CSV
                current_student.load_from_csv()
                
                # Populate student page with saved data
                populate_student_page_from_profile(_w1, current_student)
                
                # Clear login fields and show student page
                _w1.LG_mail_entry.delete(0, tk.END)
                _w1.LG_pwd_entry.delete(0, tk.END)
                show_student(_w1)
                tk.messagebox.showinfo("Login success", f"Welcome back, {email}!")
            else:
                tk.messagebox.showerror("Error", "Could not retrieve user data.")
        else:
            tk.messagebox.showerror("Authentication failed", "Invalid student credentials.")
    else:
        tk.messagebox.showinfo("Not implemented", "verify_credentials not implemented yet — proceeding to Student.")
        show_student(_w1)

def student_signup_action(_w1, mobility_manager):
    global current_student
    
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
    # Call mobilityManager.add_user if available
    if hasattr(mobility_manager, 'add_user'):
        try:
            uid = mobility_manager.add_user({
                'email': email,
                'password': pwd,
                'user_type': 'student'
            })
            
            # Clear student page for new user
            clear_student_page(_w1)
            
            # Create a Student instance with the new UID
            current_student = Student(uid, email, pwd)
            
            # Initialize student data (empty but ready to be filled)
            # The load_from_csv will return False for new students, which is expected
            current_student.load_from_csv()
            
            # Clear login fields and show student page
            _w1.LG_mail_entry.delete(0, tk.END)
            _w1.LG_pwd_entry.delete(0, tk.END)
            tk.messagebox.showinfo("Success", "Account created successfully!")
            show_student(_w1)
        except Exception as e:
            tk.messagebox.showerror("Error", f"Error creating user: {e}")
            return
    else:
        # Fallback: simulate user creation
        tk.messagebox.showinfo("Not implemented", "add_user not implemented yet — proceeding to Student.")
        show_student(_w1)
