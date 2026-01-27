import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *
import os.path

_location = os.path.dirname(__file__)

import GUI_support

_bgcolor = '#d9d9d9'
_fgcolor = '#000000'
_tabfg1 = 'black' 
_tabfg2 = 'white' 
_bgmode = 'light' 
_tabbg1 = '#d9d9d9' 
_tabbg2 = 'gray40' 

_style_code_ran = 0
def _style_code():
    global _style_code_ran
    if _style_code_ran: return        
    try: GUI_support.root.tk.call('source',
                os.path.join(_location, 'themes', 'default.tcl'))
    except: pass
    style = ttk.Style()
    style.theme_use('default')
    style.configure('.', font = "TkDefaultFont")
    if sys.platform == "win32":
       style.theme_use('winnative')    
    _style_code_ran = 1

class EntryPlaceholder(ttk.Entry):
    def __init__(self, master=None, placeholder="", color='grey', **kwargs):
        super().__init__(master, **kwargs)
        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = '#000000' # Negro

        self.bind("<FocusIn>", self._clear_placeholder)
        self.bind("<FocusOut>", self._add_placeholder)

        self._add_placeholder()

    def _add_placeholder(self, e=None):
        if not self.get():
            self.insert(0, self.placeholder)
            self.configure(foreground=self.placeholder_color)

    def _clear_placeholder(self, e=None):
        if self.get() == self.placeholder:
            self.delete(0, tk.END)
            self.configure(foreground=self.default_fg_color)

class FrameBP:

    THEME = {
        "UPF_red": "#c8102e",  
        "BG_GREY": "#d9d9d9",
        "TEXT_DARK": "#000000",
        "DISABLED_GREY": "#a3a3a3",
        "SCALE_GREY": "#c4c4c4",
        "TEXT_LIGHT": "#ffffff",
        "border_width": "2"
    }

    def __init__(self, top=None):

        top.geometry("1440x829+-7+0")
        top.minsize(120, 1)
        top.maxsize(1444, 881)
        top.resizable(1,  1)
        top.title("Toplevel 0")
        top.configure(background=self.THEME["BG_GREY"], highlightbackground=self.THEME["BG_GREY"], highlightcolor=self.THEME["TEXT_DARK"])
 
        # Initialization variables, will be renamed for use. Related to the continents in the STUDENT page.
        self.top = top
        self.combobox = tk.StringVar()
        self.combobox.set('TCombobox')
        self.tch65 = tk.IntVar()
        self.tch66 = tk.IntVar()
        self.tch69 = tk.IntVar()
        self.tch67 = tk.IntVar()
        self.tch68 = tk.IntVar()
        self.tch70 = tk.IntVar() 
#__________________________________________________________STUDENT PAGE_________________________________________________________

        # Frame for the STUDENT page
        self.ST_bg = tk.Frame(self.top)
        self.ST_bg.place(relx=0.0, rely=0.0, relheight=1.006
                , relwidth=1.003)
        self.ST_bg.configure(relief='groove', borderwidth="2",
                background=self.THEME["UPF_red"], highlightbackground=self.THEME["UPF_red"],
                highlightcolor=self.THEME["UPF_red"])

#-----------------------------------------------------STUDENT PAGE, MENU BAR----------------------------------------------------

        # STUDENT menu bar
        self.ST_menubar = tk.Frame(self.ST_bg)
        self.ST_menubar.place(relx=0.0, rely=0.0, relheight=0.042
                , relwidth=1.001)
        self.ST_menubar.configure(relief='groove', borderwidth="2",
                background=self.THEME["BG_GREY"], highlightbackground=self.THEME["BG_GREY"],
                highlightcolor=self.THEME["TEXT_DARK"])

        # STUDENT help button
        self.ST_help_button = tk.Button(self.ST_menubar)
        self.ST_help_button.place(relx=0.902, rely=0.143, height=26, width=47)
        self.ST_help_button.configure(activebackground=self.THEME["BG_GREY"],
                activeforeground="black", background=self.THEME["BG_GREY"],
                compound='left', cursor="fleur", disabledforeground=self.THEME["DISABLED_GREY"],
                foreground="white", highlightbackground=self.THEME["BG_GREY"],
                highlightcolor=self.THEME["TEXT_DARK"], text='''Help''')

        # STUDENT export button
        self.ST_export_button = tk.Button(self.ST_menubar)
        self.ST_export_button.place(relx=0.947, rely=0.143, height=26
                , width=47)
        self.ST_export_button.configure(activebackground=self.THEME["BG_GREY"],
                activeforeground="black", background=self.THEME["BG_GREY"],
                compound='left', disabledforeground=self.THEME["DISABLED_GREY"],
                foreground="white", highlightbackground=self.THEME["BG_GREY"],
                highlightcolor=self.THEME["TEXT_DARK"], text='''Export''')

        # STUDENT export button
        self.ST_logout_button = tk.Button(self.ST_menubar)
        self.ST_logout_button.place(relx=0.013, rely=0.143, height=26
                , width=47)
        self.ST_logout_button.configure(activebackground=self.THEME["BG_GREY"],
                activeforeground="black", background=self.THEME["BG_GREY"],
                compound='left', disabledforeground=self.THEME["DISABLED_GREY"],
                foreground="white", highlightbackground=self.THEME["BG_GREY"],
                highlightcolor=self.THEME["TEXT_DARK"], text='''Log out''')

#-----------------------------------------------------STUDENT PAGE, INPUTS------------------------------------------------------

        # STUDENT inputs frame
        self.ST_inputspanel_frame = tk.Frame(self.ST_bg)
        self.ST_inputspanel_frame.place(relx=0.014, rely=0.06, relheight=0.904
                , relwidth=0.296)
        self.ST_inputspanel_frame.configure(relief='groove', borderwidth="2",
                background=self.THEME["BG_GREY"], highlightbackground=self.THEME["BG_GREY"],
                highlightcolor=self.THEME["TEXT_DARK"])

        _style_code()
        
        # STUDENT title label
        self.ST_inputspanel_title = tk.Label(self.ST_inputspanel_frame)
        self.ST_inputspanel_title.place(relx=0.07, rely=0.027, height=21, width=64)
        self.ST_inputspanel_title.configure(activebackground=self.THEME["BG_GREY"],
                activeforeground="black", anchor='w', background=self.THEME["BG_GREY"],
                compound='left', disabledforeground=self.THEME["DISABLED_GREY"],
                foreground="white", highlightbackground=self.THEME["BG_GREY"],
                highlightcolor=self.THEME["TEXT_DARK"], text='''Student''')

        # STUDENT grade entry
        self.ST_grade_entry = ttk.Entry(self.ST_inputspanel_frame)
        self.ST_grade_entry.place(relx=0.164, rely=0.106, relheight=0.028
                , relwidth=0.785)
        self.ST_grade_entry.configure(exportselection="0",cursor="ibeam")

        # STUDENT grade label
        self.ST_grade_label = tk.Label(self.ST_inputspanel_frame)
        self.ST_grade_label.place(relx=0.07, rely=0.106, height=21, width=34)
        self.ST_grade_label.configure(activebackground=self.THEME["BG_GREY"],
                                    activeforeground="black", anchor='w', background=self.THEME["BG_GREY"],
                                    compound='left', disabledforeground=self.THEME["DISABLED_GREY"],
                                    foreground="white", highlightbackground=self.THEME["BG_GREY"],
                                    highlightcolor=self.THEME["TEXT_DARK"], text='''Grade''')

        # STUDENT Languages selector (TO DO)
        self.ST_lang_menu = ttk.Combobox(self.ST_inputspanel_frame)
        self.ST_lang_menu.place(relx=0.07, rely=0.225, relheight=0.025
                , relwidth=0.343)
        self.ST_lang_menu.configure(exportselection="0", textvariable=self.combobox)
        self.ST_lang_frame = tk.Frame(self.ST_inputspanel_frame)
        self.ST_lang_frame.place(relx=0.07, rely=0.265, relheight=0.179
                , relwidth=0.855)
        self.ST_lang_frame.configure(relief='groove', borderwidth="2",
                background=self.THEME["BG_GREY"], highlightbackground=self.THEME["BG_GREY"],
                highlightcolor=self.THEME["TEXT_DARK"])
        self.ST_lang_label = tk.Label(self.ST_inputspanel_frame)
        self.ST_lang_label.place(relx=0.07, rely=0.184, height=22, width=74)
        self.ST_lang_label.configure(activebackground=self.THEME["BG_GREY"],
                                        activeforeground="black", anchor='w', background=self.THEME["BG_GREY"],
                                        compound='left', disabledforeground=self.THEME["DISABLED_GREY"],
                                        foreground="white", highlightbackground=self.THEME["BG_GREY"],
                                        highlightcolor=self.THEME["TEXT_DARK"], text='''Languages''')
        self.ST_lang_button = ttk.Button(self.ST_inputspanel_frame)
        self.ST_lang_button.place(relx=0.444, rely=0.221, height=26
                                       , width=65)
        self.ST_lang_button.configure(text='''Add''', compound='left')

        # STUDENT Degree menu
        self.ST_degree_menu = ttk.Combobox(self.ST_inputspanel_frame)
        self.ST_degree_menu.place(relx=0.21, rely=0.066, relheight=0.025
                , relwidth=0.743)
        self.ST_degree_menu.configure(exportselection="0", textvariable=self.combobox)

        # STUDENT Degree label
        self.ST_degree_label = tk.Label(self.ST_inputspanel_frame)
        self.ST_degree_label.place(relx=0.07, rely=0.066, height=21, width=54)
        self.ST_degree_label.configure(activebackground=self.THEME["BG_GREY"],
                activeforeground="black", anchor='w', background=self.THEME["BG_GREY"],
                compound='left', disabledforeground=self.THEME["DISABLED_GREY"],
                foreground="white", highlightbackground=self.THEME["BG_GREY"],
                highlightcolor=self.THEME["TEXT_DARK"], text='''Degree''')

        # STUDENT continents label
        self.ST_continents_label = tk.Label(self.ST_inputspanel_frame)
        self.ST_continents_label.place(relx=0.07, rely=0.464, height=21, width=84)
        self.ST_continents_label.configure(activebackground=self.THEME["BG_GREY"],
                activeforeground="black", anchor='w', background=self.THEME["BG_GREY"],
                compound='left', disabledforeground=self.THEME["DISABLED_GREY"],
                foreground="white", highlightbackground=self.THEME["BG_GREY"],
                highlightcolor=self.THEME["TEXT_DARK"], text='''Continents''')
        
        # STUDENT continent checkbutton (EU)
        self.ST_europe_check = ttk.Checkbutton(self.ST_inputspanel_frame)
        self.ST_europe_check.place(relx=0.093, rely=0.503, relwidth=0.131
                , relheight=0.0, height=19)
        self.ST_europe_check.configure(variable=self.tch65, text='''Europe''', compound='left')

        # STUDENT continent checkbutton (SA)
        self.ST_southamerica_check = ttk.Checkbutton(self.ST_inputspanel_frame)
        self.ST_southamerica_check.place(relx=0.376, rely=0.503, relwidth=0.245
                , relheight=0.0, height=19)
        self.ST_southamerica_check.configure(variable=self.tch66, text='''North America''', compound='left')

        # STUDENT continent checkbutton (AS)
        self.ST_asia_check = ttk.Checkbutton(self.ST_inputspanel_frame)
        self.ST_asia_check.place(relx=0.657, rely=0.503, relwidth=0.245
                , relheight=0.0, height=19)
        self.ST_asia_check.configure(variable=self.tch69, text='''South America''', compound='left')

        # STUDENT continents checkbutton (AF)
        self.ST_africa_check = ttk.Checkbutton(self.ST_inputspanel_frame)
        self.ST_africa_check.place(relx=0.093, rely=0.531, relwidth=0.131
                , relheight=0.0, height=18)
        self.ST_africa_check.configure(variable=self.tch67, text='''Asia''', compound='left')

        # STUDENT continent checkbutton (NA)
        self.ST_northamerica_check = ttk.Checkbutton(self.ST_inputspanel_frame)
        self.ST_northamerica_check.place(relx=0.376, rely=0.531, relwidth=0.129
                , relheight=0.0, height=18)
        self.ST_northamerica_check.configure(variable=self.tch68, text='''Africa''', compound='left')

        # STUDENT continent checkbutton (OC)
        self.ST_oceania_check = ttk.Checkbutton(self.ST_inputspanel_frame)
        self.ST_oceania_check.place(relx=0.657, rely=0.531, relwidth=0.152
                , relheight=0.0, height=18)
        self.ST_oceania_check.configure(variable=self.tch70, text='''Oceania''', compound='left')

        # STUDENT preferences scrolled window (TO DO: rename, plan, code, beautify)
        self.ScrolledwindowPreferencesLP = ScrolledWindow(self.ST_inputspanel_frame)
        self.ScrolledwindowPreferencesLP.place(relx=0.07, rely=0.623
                , relheight=0.273, relwidth=0.853)
        self.ScrolledwindowPreferencesLP.configure(background=self.THEME["BG_GREY"],
                borderwidth="2", highlightbackground=self.THEME["BG_GREY"],
                highlightcolor=self.THEME["TEXT_DARK"], insertbackground=self.THEME["TEXT_DARK"],
                relief="groove", selectbackground=self.THEME["BG_GREY"],
                selectforeground="black")
        self.color = self.ScrolledwindowPreferencesLP.cget("background")
        self.ScrolledwindowPreferencesLP_f = tk.Frame(self.ScrolledwindowPreferencesLP,
                            background=self.color)
        self.ScrolledwindowPreferencesLP.create_window(0, 0, anchor='nw',
                                           window=self.ScrolledwindowPreferencesLP_f)

        # STUDENT Rank! button
        self.ST_rank_button = ttk.Button(self.ST_inputspanel_frame)
        self.ST_rank_button.place(relx=0.35, rely=0.914, height=46, width=125)
        self.ST_rank_button.configure(text='''Rank !''')
        self.ST_rank_button.configure(compound='left')

        # STUDENT visual separators
        self.ST_separator1 = ttk.Separator(self.ST_inputspanel_frame)
        self.ST_separator1.place(relx=0.058, rely=0.164,  relwidth=0.886)
        self.T_separator2 = ttk.Separator(self.ST_inputspanel_frame)
        self.T_separator2.place(relx=0.061, rely=0.584,  relwidth=0.876)

#-----------------------------------------------------STUDENT PAGE, RANKING------------------------------------------------------

        # STUDENT Ranking scrolled window  (to do: name, plan, code, beautify)
        self.ScrolledwindowRUP = ScrolledWindow(self.ST_bg)
        self.ScrolledwindowRUP.place(relx=0.319, rely=0.06, relheight=0.606
                , relwidth=0.668)
        self.ScrolledwindowRUP.configure(background=self.THEME["BG_GREY"],
                borderwidth="2", highlightbackground=self.THEME["BG_GREY"],
                highlightcolor=self.THEME["TEXT_DARK"], insertbackground=self.THEME["TEXT_DARK"],
                relief="groove", selectbackground=self.THEME["BG_GREY"],
                selectforeground="black")
        self.color = self.ScrolledwindowRUP.cget("background")
        self.ScrolledwindowRUP_f = tk.Frame(self.ScrolledwindowRUP,
                            background=self.color)
        self.ScrolledwindowRUP.create_window(0, 0, anchor='nw',
                                           window=self.ScrolledwindowRUP_f)

 #-----------------------------------------------------STUDENT PAGE, UNI STATS--------------------------------------------------
        
        # STUDENT University facts frame
        self.ST_facts_frame = tk.Frame(self.ST_bg)
        self.ST_facts_frame.place(relx=0.319, rely=0.683, relheight=0.281
                , relwidth=0.668)
        self.ST_facts_frame.configure(relief='groove', borderwidth="2",
                background=self.THEME["BG_GREY"], highlightbackground=self.THEME["BG_GREY"],
                highlightcolor=self.THEME["TEXT_DARK"])

        self.ST_uniname_label = tk.Label(self.ST_facts_frame)
        self.ST_uniname_label.place(relx=0.031, rely=0.085, height=21, width=352)
        self.ST_uniname_label.configure(activebackground=self.THEME["BG_GREY"],
                activeforeground="black", anchor='w', background=self.THEME["BG_GREY"],
                compound='left', disabledforeground=self.THEME["DISABLED_GREY"],
                foreground="white", highlightbackground=self.THEME["BG_GREY"],
                highlightcolor=self.THEME["TEXT_DARK"], text='''University, City, Country''')

        # STUDENT University stats subframe
        self.ST_unistats_label = tk.Frame(self.ST_facts_frame)
        self.ST_unistats_label.place(relx=0.218, rely=0.256, relheight=0.658
                , relwidth=0.76)
        self.ST_unistats_label.configure(relief='groove', borderwidth="2",
                background=self.THEME["BG_GREY"], cursor="fleur",
                highlightbackground=self.THEME["BG_GREY"], highlightcolor=self.THEME["TEXT_DARK"])
        
        # STUDENT Stats11 label
        self.ST_stat11_label = tk.Label(self.ST_unistats_label)
        self.ST_stat11_label.place(relx=0.014, rely=0.052, height=65, width=154)
        self.ST_stat11_label.configure(activebackground=self.THEME["BG_GREY"],
                activeforeground="black", anchor='w', background=self.THEME["BG_GREY"],
                compound='left', disabledforeground=self.THEME["DISABLED_GREY"],
                foreground="white", highlightbackground=self.THEME["BG_GREY"],
                highlightcolor=self.THEME["TEXT_DARK"], text='''Ranking''')
        
        # STUDENT Stats21 label
        self.ST_stat21_label = tk.Label(self.ST_unistats_label)
        self.ST_stat21_label.place(relx=0.014, rely=0.552, height=65, width=155)
        self.ST_stat21_label.configure(activebackground=self.THEME["BG_GREY"],
                activeforeground="black", anchor='w', background=self.THEME["BG_GREY"],
                compound='left', disabledforeground=self.THEME["DISABLED_GREY"],
                foreground="white", highlightbackground=self.THEME["BG_GREY"],
                highlightcolor=self.THEME["TEXT_DARK"], text='''Engineering Ranking''')
        
        # STUDENT Stats12 label
        self.ST_stat12_label = tk.Label(self.ST_unistats_label)
        self.ST_stat12_label.place(relx=0.259, rely=0.052, height=65, width=155)
        self.ST_stat12_label.configure(activebackground=self.THEME["BG_GREY"],
                activeforeground="black", anchor='w', background=self.THEME["BG_GREY"],
                compound='left', disabledforeground=self.THEME["DISABLED_GREY"],
                foreground="white", highlightbackground=self.THEME["BG_GREY"],
                highlightcolor=self.THEME["TEXT_DARK"], text='''Cost of living''')
        
        # STUDENT Stats22 label
        self.ST_stat22_label = tk.Label(self.ST_unistats_label)
        self.ST_stat22_label.place(relx=0.259, rely=0.552, height=65, width=155)
        self.ST_stat22_label.configure(activebackground=self.THEME["BG_GREY"],
                activeforeground="black", anchor='w', background=self.THEME["BG_GREY"],
                compound='left', cursor="fleur", disabledforeground=self.THEME["DISABLED_GREY"],
                foreground="white", highlightbackground=self.THEME["BG_GREY"],
                highlightcolor=self.THEME["TEXT_DARK"], text='''Weather''')
        
        # STUDENT Stats13 label
        self.ST_stat13_label = tk.Label(self.ST_unistats_label)
        self.ST_stat13_label.place(relx=0.503, rely=0.052, height=65, width=154)
        self.ST_stat13_label.configure(activebackground=self.THEME["BG_GREY"],
                activeforeground="black", anchor='w', background=self.THEME["BG_GREY"],
                compound='left', cursor="fleur", disabledforeground=self.THEME["DISABLED_GREY"],
                foreground="white", highlightbackground=self.THEME["BG_GREY"],
                highlightcolor=self.THEME["TEXT_DARK"], text='''Nightlife''')
        
        # STUDENT Stats23 label
        self.ST_stat23_label = tk.Label(self.ST_unistats_label)
        self.ST_stat23_label.place(relx=0.503, rely=0.552, height=65, width=154)
        self.ST_stat23_label.configure(activebackground=self.THEME["BG_GREY"],
                activeforeground="black", anchor='w', background=self.THEME["BG_GREY"],
                compound='left', cursor="fleur", disabledforeground=self.THEME["DISABLED_GREY"],
                foreground="white", highlightbackground=self.THEME["BG_GREY"],
                highlightcolor=self.THEME["TEXT_DARK"], text='''Previous cutoff grade''')
        
        # STUDENT Stats14 label
        self.ST_stat14_label = tk.Label(self.ST_unistats_label)
        self.ST_stat14_label.place(relx=0.748, rely=0.052, height=65, width=154)
        self.ST_stat14_label.configure(activebackground=self.THEME["BG_GREY"],
                activeforeground="black", anchor='w', background=self.THEME["BG_GREY"],
                compound='left', cursor="fleur", disabledforeground=self.THEME["DISABLED_GREY"],
                foreground="white", highlightbackground=self.THEME["BG_GREY"],
                highlightcolor=self.THEME["TEXT_DARK"], text='''Available spots''')
        
        # STUDENT Stats24 label
        self.ST_stat24_label = tk.Label(self.ST_unistats_label)
        self.ST_stat24_label.place(relx=0.748, rely=0.552, height=65, width=155)
        self.ST_stat24_label.configure(activebackground=self.THEME["BG_GREY"],
                activeforeground="black", anchor='w', background=self.THEME["BG_GREY"],
                compound='left', cursor="fleur", disabledforeground=self.THEME["DISABLED_GREY"],
                foreground="white", highlightbackground=self.THEME["BG_GREY"],
                highlightcolor=self.THEME["TEXT_DARK"], text='''Duration''')
        
        # STUDENT University logo label
        self.ST_logo_label = tk.Label(self.ST_facts_frame)
        self.ST_logo_label.place(relx=0.024, rely=0.239, height=160, width=160)
        self.ST_logo_label.configure(activebackground=self.THEME["UPF_red"],
                activeforeground=self.THEME["UPF_red"], anchor='w', background=self.THEME["BG_GREY"],
                compound='left', disabledforeground=self.THEME["DISABLED_GREY"],
                foreground="white", highlightbackground=self.THEME["BG_GREY"],
                highlightcolor=self.THEME["TEXT_DARK"], text='''University LOGO (image)''')
        
        # STUDENT Map button
        self.ST_map_button = ttk.Button(self.ST_facts_frame)
        self.ST_map_button.place(relx=0.913, rely=0.085, height=26, width=65)
        self.ST_map_button.configure(takefocus="")
        self.ST_map_button.configure(text='''Map''')
        self.ST_map_button.configure(compound='left')

        # STUDENT Website button
        self.ST_web_button = ttk.Button(self.ST_facts_frame)
        self.ST_web_button.place(relx=0.83, rely=0.085, height=26, width=65)
        self.ST_web_button.configure(takefocus="")
        self.ST_web_button.configure(text='''Website''')
        self.ST_web_button.configure(compound='left')

#___________________________________________________________LOGIN PAGE__________________________________________________________

        # LOGIN page frame
        self.LG_bg = tk.Frame(self.top)
        self.LG_bg.place(relx=0.0, rely=0.0, relheight=1.006
                , relwidth=1.003)
        self.LG_bg.configure(relief='groove', borderwidth="2",
                background=self.THEME["UPF_red"], highlightbackground=self.THEME["BG_GREY"],
                highlightcolor=self.THEME["TEXT_DARK"])

        # LOGIN subframe
        self.LG_sublabelframe= tk.LabelFrame(self.LG_bg)
        self.LG_sublabelframe.place(relx=0.312, rely=0.466, relheight=0.388
                , relwidth=0.382)
        self.LG_sublabelframe.configure(relief='groove', foreground="white",
                text='''Student''', background=self.THEME["UPF_red"],
                highlightbackground=self.THEME["BG_GREY"], highlightcolor=self.THEME["TEXT_DARK"])

        # LOGIN mail label
        self.LG_mail_label = ttk.Label(self.LG_sublabelframe)
        self.LG_mail_label.place(relx=0.181, rely=0.216, height=17, width=34
                , bordermode='ignore')
        self.LG_mail_label.configure(font="TkDefaultFont", relief="flat",
                text='''Email:''', compound='left')
        
        # LOGIN mail entry
        self.LG_mail_entry = ttk.Entry(self.LG_sublabelframe)
        self.LG_mail_entry.place(relx=0.181, rely=0.278, relheight=0.065
                , relwidth=0.646, bordermode='ignore')
        self.LG_mail_entry.configure(exportselection="0", cursor="ibeam")

        # LOGIN password label
        self.LG_pwd_label = ttk.Label(self.LG_sublabelframe)
        self.LG_pwd_label.place(relx=0.181, rely=0.432, height=17, width=64
                , bordermode='ignore')
        self.LG_pwd_label.configure(font="TkDefaultFont", relief="flat",
                text='''Password:''', compound='left')
        
        # LOGIN password entry
        self.LG_pwd_entry = ttk.Entry(self.LG_sublabelframe)
        self.LG_pwd_entry.place(relx=0.181, rely=0.494, relheight=0.065
                , relwidth=0.646, bordermode='ignore')
        self.LG_pwd_entry.configure(exportselection="0", cursor="ibeam")

        # LOGIN student login button
        self.LG_studentlogin_button = ttk.Button(self.LG_sublabelframe)
        self.LG_studentlogin_button.place(relx=0.178, rely=0.772, height=56, width=125
                , bordermode='ignore')
        self.LG_studentlogin_button.configure(text='''Log In (S)''')
        self.LG_studentlogin_button.configure(compound='left')

        # LOGIN admin login button
        self.LG_adminlogin_button = ttk.Button(self.LG_sublabelframe)
        self.LG_adminlogin_button.place(relx=0.392, rely=0.772, height=56
                , width=125, bordermode='ignore')
        self.LG_adminlogin_button.configure(text='''Log In (A)''')
        self.LG_adminlogin_button.configure(compound='left')

        # LOGIN student sign up button
        self.LG_studentsingup_button = ttk.Button(self.LG_sublabelframe)
        self.LG_studentsingup_button.place(relx=0.606, rely=0.772, height=56, width=125
                , bordermode='ignore')
        self.LG_studentsingup_button.configure(text='''Sign Up (S)''')
        self.LG_studentsingup_button.configure(compound='left')

        # LOGIN title label
        self.LG_title_label = tk.Label(self.LG_bg)
        self.LG_title_label.place(relx=0.284, rely=0.18, height=91, width=644)
        self.LG_title_label.configure(activebackground=self.THEME["BG_GREY"],
                activeforeground="black", anchor='w', background=self.THEME["UPF_red"],
                compound='left', disabledforeground=self.THEME["DISABLED_GREY"],
                font="-family {Microsoft YaHei} -size 48 -weight bold",
                foreground=self.THEME["TEXT_LIGHT"], highlightbackground=self.THEME["BG_GREY"],
                highlightcolor=self.THEME["TEXT_DARK"], text='''UPF Mobility Agent''')

        # LOGIN admin selection button
        self.LG_admin_button = ttk.Button(self.LG_bg)
        self.LG_admin_button.place(relx=0.54, rely=0.323, height=86, width=125)
        self.LG_admin_button.configure(text='''Admin''')
        self.LG_admin_button.configure(compound='left')

        # LOGIN student selection button
        self.LG_student_button = ttk.Button(self.LG_bg)
        self.LG_student_button.place(relx=0.388, rely=0.323, height=86
                , width=125)
        self.LG_student_button.configure(text='''Student''')
        self.LG_student_button.configure(compound='left')
        self.LG_student_button.configure(cursor="fleur")

 #___________________________________________________________ADMIN PAGE__________________________________________________________

        # ADMIN page frame
        self.AD_bg = tk.Frame(self.top)
        self.AD_bg.place(relx=0.0, rely=0.0, relheight=1.006
                , relwidth=1.003)
        self.AD_bg.configure(relief='groove', borderwidth="2",
                background=self.THEME["UPF_red"], highlightbackground=self.THEME["BG_GREY"],
                highlightcolor=self.THEME["TEXT_DARK"])
        
        # ADMIN subframe
        self.AD_subframe = tk.Frame(self.AD_bg)
        self.AD_subframe.place(relx=0.017, rely=0.066, relheight=0.903
                , relwidth=0.967)
        self.AD_subframe.configure(relief='groove', borderwidth="2",
                background=self.THEME["BG_GREY"], highlightbackground=self.THEME["BG_GREY"],
                highlightcolor=self.THEME["TEXT_DARK"])

#----------------------------------------------------ADMIN PAGE, ADD/EDIT/DELETE---------------------------------------------------

        # ADMIN Edit/Delete button
        self.AD_editdelete_button = ttk.Button(self.AD_subframe)
        self.AD_editdelete_button.place(relx=0.028, rely=0.224, height=86
                , width=275)
        self.AD_editdelete_button.configure(takefocus="")
        self.AD_editdelete_button.configure(text='''Edit / Delete''')
        self.AD_editdelete_button.configure(compound='left')

        # ADMIN Add button
        self.AD_add_button = ttk.Button(self.AD_subframe)
        self.AD_add_button.place(relx=0.029, rely=0.598, height=86, width=275)
        self.AD_add_button.configure(takefocus="")
        self.AD_add_button.configure(text='''Add''')
        self.AD_add_button.configure(compound='left')
        self.AD_add_button.configure(cursor="fleur")

        # ADMIN uni selector combobox
        self.provalist = ["Universitat Pompeu Fabra", "Universitat de Barcelona", "Universitat de València", "Autonomous University of Barcelona", "University of Granada", "University of Sevilla", "University of Salamanca", "ANTONIO", "PEPE", "JOSEP", "MARIA", "LAIA", "Igor"]
        self.AD_uni_combobox = ttk.Combobox(self.AD_subframe, values=self.provalist)
        self.AD_uni_combobox.place(relx=0.028, rely=0.345, relheight=0.027
                , relwidth=0.198)
        self.AD_uni_combobox.configure(background="white", takefocus="", height=10, state="readonly")

        # ADMIN title label
        self.AD_title_label = ttk.Label(self.AD_subframe)
        self.AD_title_label.place(relx=0.014, rely=0.027, height=28, width=143)
        self.AD_title_label.configure(font="TkDefaultFont", relief="flat",
                text='''Admin Settings''', compound='left')

#-----------------------------------------------------ADMIN PAGE, INPUTS---------------------------------------------------------

        # ADMIN entries frame
        self.AD_entries_frame = ttk.Frame(self.AD_subframe)
        self.AD_entries_frame.place(relx=0.244, rely=0.027, relheight=0.948
                , relwidth=0.741)
        self.AD_entries_frame.configure(relief='groove', borderwidth="2",
                cursor="fleur")

        # ADMIN uni name label
        self.AD_uniname_label = ttk.Label(self.AD_entries_frame)
        self.AD_uniname_label.place(relx=0.058, rely=0.07, height=17, width=86)
        self.AD_uniname_label.configure(font="TkDefaultFont", relief="flat",
                text='''Name''', compound='left', cursor="fleur")
        # ADMIN uni name entry
        self.AD_uniname_entry = EntryPlaceholder(self.AD_entries_frame, placeholder="Universitat Pompeu Fabra")
        self.AD_uniname_entry.place(relx=0.058, rely=0.098, relheight=0.029
                , relwidth=0.248)
        self.AD_uniname_entry.configure(exportselection="0", cursor="ibeam")

        # ADMIN uni ID label
        self.AD_ID_label = ttk.Label(self.AD_entries_frame)
        self.AD_ID_label.place(relx=0.058, rely=0.196, height=17, width=117)
        self.AD_ID_label.configure(font="TkDefaultFont", relief="flat",
                text='''ID''', compound='left')
        # ADMIN uni ID entry
        self.AD_ID_entry = EntryPlaceholder(self.AD_entries_frame, placeholder="98FE9FHASN91U3")
        self.AD_ID_entry.place(relx=0.058, rely=0.224, relheight=0.029
                , relwidth=0.248)
        self.AD_ID_entry.configure(exportselection="0", cursor="ibeam", state="disabled")

        # ADMIN country label
        self.AD_country_label = ttk.Label(self.AD_entries_frame)
        self.AD_country_label.place(relx=0.058, rely=0.322, height=17, width=86)
        self.AD_country_label.configure(font="TkDefaultFont", relief="flat",
                text='''Country''', compound='left')
        # ADMIN country entry
        self.AD_country_entry = EntryPlaceholder(self.AD_entries_frame, placeholder="Spain")
        self.AD_country_entry.place(relx=0.058, rely=0.35, relheight=0.029
                , relwidth=0.248)
        self.AD_country_entry.configure(exportselection="0", cursor="ibeam")

        # ADMIN city label
        self.AD_city_label = ttk.Label(self.AD_entries_frame)
        self.AD_city_label.place(relx=0.058, rely=0.448, height=18, width=117)
        self.AD_city_label.configure(font="TkDefaultFont", relief="flat",
                text='''City''', compound='left')
        # ADMIN city entry
        self.AD_city_entry = EntryPlaceholder(self.AD_entries_frame, placeholder="Barcelona")
        self.AD_city_entry.place(relx=0.058, rely=0.476, relheight=0.029
                , relwidth=0.248)
        self.AD_city_entry.configure(exportselection="0", cursor="ibeam")

        # ADMIN continent label
        self.AD_continent_label = ttk.Label(self.AD_entries_frame)
        self.AD_continent_label.place(relx=0.058, rely=0.573, height=17
                , width=165)
        self.AD_continent_label.configure(font="TkDefaultFont", relief="flat",
                text='''Continent''', compound='left')
        # ADMIN continent entry
        self.AD_continent_entry = EntryPlaceholder(self.AD_entries_frame, placeholder="Europe")
        self.AD_continent_entry.place(relx=0.058, rely=0.601, relheight=0.028
                , relwidth=0.248)
        self.AD_continent_entry.configure(exportselection="0", cursor="ibeam")

        # ADMIN minimum grade label
        self.AD_mingrade_label = ttk.Label(self.AD_entries_frame)
        self.AD_mingrade_label.place(relx=0.058, rely=0.699, height=17
                , width=164)
        self.AD_mingrade_label.configure(font="TkDefaultFont", relief="flat",
                text='''Minimum grade''', compound='left')
        # ADMIN minimum grade entry
        self.AD_mingrade_entry = EntryPlaceholder(self.AD_entries_frame, placeholder="5.0")
        self.AD_mingrade_entry.place(relx=0.058, rely=0.727, relheight=0.028
                , relwidth=0.248)
        self.AD_mingrade_entry.configure(exportselection="0", cursor="ibeam")

        # ADMIN website label
        self.AD_web_label = ttk.Label(self.AD_entries_frame)
        self.AD_web_label.place(relx=0.058, rely=0.825, height=17, width=85)
        self.AD_web_label.configure(font="TkDefaultFont", relief="flat",
                text='''Website''', compound='left')
        # ADMIN website entry
        self.AD_web_entry = EntryPlaceholder(self.AD_entries_frame, placeholder="www.upf.edu")
        self.AD_web_entry.place(relx=0.058, rely=0.853, relheight=0.029
                , relwidth=0.248)
        self.AD_web_entry.configure(exportselection="0", cursor="ibeam")

        # ADMIN latitude label
        self.AD_lat_label = ttk.Label(self.AD_entries_frame)
        self.AD_lat_label.place(relx=0.358, rely=0.07, height=17, width=86)
        self.AD_lat_label.configure(font="TkDefaultFont", relief="flat",
                text='''Latitude''', compound='left')
        # ADMIN latitude entry
        self.AD_lat_entry = EntryPlaceholder(self.AD_entries_frame, placeholder="41.4039")
        self.AD_lat_entry.place(relx=0.358, rely=0.098, relheight=0.029
                , relwidth=0.257)
        self.AD_lat_entry.configure(exportselection="0", cursor="fleur")

        # ADMIN longitude label
        self.AD_long_label = ttk.Label(self.AD_entries_frame)
        self.AD_long_label.place(relx=0.358, rely=0.196, height=17
                , width=117)
        self.AD_long_label.configure(font="TkDefaultFont", relief="flat",
                text='''Longitude''', compound='left', cursor="fleur")
        # ADMIN longitude entry
        self.AD_long_entry = EntryPlaceholder(self.AD_entries_frame, placeholder="2.1940")
        self.AD_long_entry.place(relx=0.358, rely=0.224, relheight=0.029
                , relwidth=0.257)
        self.AD_long_entry.configure(exportselection="0", cursor="ibeam")

        # ADMIN languages label
        self.AD_lang_label = ttk.Label(self.AD_entries_frame)
        self.AD_lang_label.place(relx=0.358, rely=0.322, height=17
                , width=198)
        self.AD_lang_label.configure(font="TkDefaultFont", relief="flat",
                text='''Languages required''', compound='left')
        # ADMIN languages frame
        self.AD_lang_frame = ttk.Frame(self.AD_entries_frame)
        self.AD_lang_frame.place(relx=0.358, rely=0.35, relheight=0.401
                , relwidth=0.259)
        self.AD_lang_frame.configure(relief='groove', borderwidth="2")

        # ADMIN spots label
        self.AD_spots_label = ttk.Label(self.AD_entries_frame)
        self.AD_spots_label.place(relx=0.358, rely=0.797, height=17, width=94)
        self.AD_spots_label.configure(font="TkDefaultFont", relief="flat",
                text='''Spots available''', compound='left')
        # ADMIN spots scale
        self.AD_spots_scale =  tk.Scale(self.AD_entries_frame, from_=0.0, to=100.0, resolution=1.0)
        self.AD_spots_scale.place(relx=0.358, rely=0.825, relheight=0.059
                , relwidth=0.258)
        self.AD_spots_scale.configure(activebackground=self.THEME["BG_GREY"],
                background=self.THEME["BG_GREY"], foreground=self.THEME["TEXT_DARK"],
                highlightbackground=self.THEME["BG_GREY"], highlightcolor=self.THEME["TEXT_DARK"],
                length="267", orient="horizontal", troughcolor=self.THEME["SCALE_GREY"], from_=1, to=25, resolution=1)

        # ADMIN academic rank label
        self.AD_rank_label = tk.Label(self.AD_entries_frame)
        self.AD_rank_label.place(relx=0.667, rely=0.07, height=21, width=113)
        self.AD_rank_label.configure(activebackground=self.THEME["BG_GREY"],
                activeforeground="black", anchor='w', background=self.THEME["BG_GREY"],
                compound='left', disabledforeground=self.THEME["DISABLED_GREY"],
                foreground=self.THEME["TEXT_DARK"], highlightbackground=self.THEME["BG_GREY"],
                highlightcolor=self.THEME["TEXT_DARK"], text='''University Ranking''')
        # ADMIN academic rank entry
        self.AD_rank_entry = EntryPlaceholder(self.AD_entries_frame, placeholder="187 (N/A if not ranked)")
        self.AD_rank_entry.place(relx=0.667, rely=0.098, relheight=0.029
                , relwidth=0.257)
        self.AD_rank_entry.configure(exportselection="0", takefocus="",
                cursor="ibeam")

        # ADMIN engineering rank label
        self.AD_engrank_label = tk.Label(self.AD_entries_frame)
        self.AD_engrank_label.place(relx=0.667, rely=0.196, height=21
                , width=124)
        self.AD_engrank_label.configure(activebackground=self.THEME["BG_GREY"],
                activeforeground="black", anchor='w', background=self.THEME["BG_GREY"],
                compound='left', disabledforeground=self.THEME["DISABLED_GREY"],
                foreground=self.THEME["TEXT_DARK"], highlightbackground=self.THEME["BG_GREY"],
                highlightcolor=self.THEME["TEXT_DARK"], text='''Engineering Ranking''')
        # ADMIN engineering rank entry
        self.AD_engrank_entry = EntryPlaceholder(self.AD_entries_frame, placeholder="301-400 (N/A if not ranked)")
        self.AD_engrank_entry.place(relx=0.667, rely=0.224, relheight=0.029
                , relwidth=0.257)
        self.AD_engrank_entry.configure(exportselection="0", takefocus="",
                cursor="ibeam")

        # ADMIN weather label
        self.AD_weather_label = tk.Label(self.AD_entries_frame)
        self.AD_weather_label.place(relx=0.667, rely=0.322, height=21, width=53)
        self.AD_weather_label.configure(activebackground=self.THEME["BG_GREY"],
                activeforeground="black", anchor='w', background=self.THEME["BG_GREY"],
                compound='left', cursor="fleur", disabledforeground=self.THEME["DISABLED_GREY"],
                foreground=self.THEME["TEXT_DARK"], highlightbackground=self.THEME["BG_GREY"],
                highlightcolor=self.THEME["TEXT_DARK"], text='''Weather''')
        # ADMIN weather entry
        self.AD_weather_entry = EntryPlaceholder(self.AD_entries_frame, placeholder="Mediterranean")
        self.AD_weather_entry.place(relx=0.667, rely=0.35, relheight=0.029
                , relwidth=0.257)
        self.AD_weather_entry.configure(exportselection="0", takefocus="",
                cursor="ibeam")

        # ADMIN nightlife label
        self.AD_nightlife_label = tk.Label(self.AD_entries_frame)
        self.AD_nightlife_label.place(relx=0.667, rely=0.448, height=21
                , width=49)
        self.AD_nightlife_label.configure(activebackground=self.THEME["BG_GREY"],
                activeforeground="black", anchor='w', background=self.THEME["BG_GREY"],
                compound='left', disabledforeground=self.THEME["DISABLED_GREY"],
                foreground=self.THEME["TEXT_DARK"], highlightbackground=self.THEME["BG_GREY"],
                highlightcolor=self.THEME["TEXT_DARK"], text='''Nightlife''')
        # ADMIN nightlife scale
        self.AD_nightlife_scale =  tk.Scale(self.AD_entries_frame, from_=0.0, to=100.0, resolution=1.0)
        self.AD_nightlife_scale.place(relx=0.667, rely=0.476, relheight=0.06
                , relwidth=0.255)
        self.AD_nightlife_scale.configure(activebackground=self.THEME["BG_GREY"],
                background=self.THEME["BG_GREY"], foreground=self.THEME["TEXT_DARK"],
                highlightbackground=self.THEME["BG_GREY"], highlightcolor=self.THEME["TEXT_DARK"],
                length="266", orient="horizontal", troughcolor=self.THEME["SCALE_GREY"],
                from_=1.0, to=10.0, resolution=1.0)
        
        # ADMIN cost of living label
        self.AD_cost_label = tk.Label(self.AD_entries_frame)
        self.AD_cost_label.place(relx=0.667, rely=0.573, height=20, width=124)
        self.AD_cost_label.configure(activebackground=self.THEME["BG_GREY"],
                activeforeground="black", anchor='w', background=self.THEME["BG_GREY"],
                compound='left', disabledforeground=self.THEME["DISABLED_GREY"],
                foreground=self.THEME["TEXT_DARK"], highlightbackground=self.THEME["BG_GREY"],
                highlightcolor=self.THEME["TEXT_DARK"], text='''Cost of living''')
        # ADMIN cost of living scale
        self.AD_cost_scale =  tk.Scale(self.AD_entries_frame, from_=0.0, to=100.0, resolution=1.0)
        self.AD_cost_scale.place(relx=0.667, rely=0.601, relheight=0.059
                , relwidth=0.256)
        self.AD_cost_scale.configure(activebackground=self.THEME["BG_GREY"],
                background=self.THEME["BG_GREY"], foreground=self.THEME["TEXT_DARK"],
                highlightbackground=self.THEME["BG_GREY"], highlightcolor=self.THEME["TEXT_DARK"],
                length="266", orient="horizontal", troughcolor=self.THEME["SCALE_GREY"],
                from_=1.0, to=10.0, resolution=1.0)

        # ADMIN previous cutoff grade label
        self.AD_cutoff_label = tk.Label(self.AD_entries_frame)
        self.AD_cutoff_label.place(relx=0.667, rely=0.699, height=21, width=134)
        self.AD_cutoff_label.configure(activebackground=self.THEME["BG_GREY"],
                activeforeground="black", anchor='w', background=self.THEME["BG_GREY"],
                compound='left', disabledforeground=self.THEME["DISABLED_GREY"],
                foreground=self.THEME["TEXT_DARK"], highlightbackground=self.THEME["BG_GREY"],
                highlightcolor=self.THEME["TEXT_DARK"], text='''Previous cutoff grade''')
        # ADMIN previous cutoff grade entry
        self.AD_cutoff_entry = EntryPlaceholder(self.AD_entries_frame, placeholder="5.00")
        self.AD_cutoff_entry.place(relx=0.667, rely=0.727, relheight=0.029
                , relwidth=0.257)
        self.AD_cutoff_entry.configure(exportselection="0", takefocus="",
                cursor="ibeam")

        # ADMIN duration label
        self.AD_duration_label = tk.Label(self.AD_entries_frame)
        self.AD_duration_label.place(relx=0.667, rely=0.797, height=21
                , width=104)
        self.AD_duration_label.configure(activebackground=self.THEME["BG_GREY"],
                activeforeground="black", anchor='w', background=self.THEME["BG_GREY"],
                compound='left', disabledforeground=self.THEME["DISABLED_GREY"],
                foreground=self.THEME["TEXT_DARK"], highlightbackground=self.THEME["BG_GREY"],
                highlightcolor=self.THEME["TEXT_DARK"], text='''Duration (months)''')
        # ADMIN duration scale
        self.AD_duration_scale =  tk.Scale(self.AD_entries_frame, from_=0.0, to=100.0, resolution=1.0)
        self.AD_duration_scale.place(relx=0.667, rely=0.825, relheight=0.059
                , relwidth=0.256)
        self.AD_duration_scale.configure(activebackground=self.THEME["BG_GREY"],
                background=self.THEME["BG_GREY"], foreground=self.THEME["TEXT_DARK"],
                highlightbackground=self.THEME["BG_GREY"], highlightcolor=self.THEME["TEXT_DARK"],
                length="266", orient="horizontal", troughcolor=self.THEME["SCALE_GREY"],
                from_=1.0, to=12.0, resolution=1.0)     

#-----------------------------------------------------ADMIN PAGE, ACTION BUTTONS------------------------------------------------------
      
        # ADMIN save button
        self.AD_save_button = tk.Button(self.AD_entries_frame)
        self.AD_save_button.place(relx=0.909, rely=0.923, height=36, width=67)
        self.AD_save_button.configure(activebackground=self.THEME["BG_GREY"],
                activeforeground="black", background=self.THEME["BG_GREY"],
                compound='left', disabledforeground=self.THEME["DISABLED_GREY"],
                foreground=self.THEME["TEXT_DARK"], highlightbackground=self.THEME["BG_GREY"],
                highlightcolor=self.THEME["TEXT_DARK"], text='''Delete''')

        # ADMIN delete button
        self.AD_delete_button = tk.Button(self.AD_entries_frame)
        self.AD_delete_button.place(relx=0.822, rely=0.923, height=36
                , width=67)
        self.AD_delete_button.configure(activebackground=self.THEME["BG_GREY"],
                activeforeground="black", background=self.THEME["BG_GREY"],
                compound='left', disabledforeground=self.THEME["DISABLED_GREY"],
                foreground=self.THEME["TEXT_DARK"], highlightbackground=self.THEME["BG_GREY"],
                highlightcolor=self.THEME["TEXT_DARK"], text='''Save''')

#-----------------------------------------------------ADMIN PAGE, MENU BAR--------------------------------------------------------      

        # ADMIN menu bar frame
        self.AD_menubar = tk.Frame(self.AD_bg)
        self.AD_menubar.place(relx=0.0, rely=0.0, relheight=0.042
                , relwidth=1.001)
        self.AD_menubar.configure(relief='groove', borderwidth="2",
                background=self.THEME["BG_GREY"], highlightbackground=self.THEME["BG_GREY"],
                highlightcolor=self.THEME["TEXT_DARK"])

        # ADMIN Help button
        self.AD_help_button = tk.Button(self.AD_menubar)
        self.AD_help_button.place(relx=0.947, rely=0.114, height=26, width=47)
        self.AD_help_button.configure(activebackground=self.THEME["BG_GREY"],
                activeforeground="black", background=self.THEME["BG_GREY"],
                compound='left', cursor="fleur", disabledforeground=self.THEME["DISABLED_GREY"],
                foreground="white", highlightbackground=self.THEME["BG_GREY"],
                highlightcolor=self.THEME["TEXT_DARK"], text='''Help''')

        # Admin Log out button
        self.AD_logout_button = tk.Button(self.AD_menubar)
        self.AD_logout_button.place(relx=0.013, rely=0.143, height=26, width=47)
        self.AD_logout_button.configure(activebackground=self.THEME["BG_GREY"],
                activeforeground="black", background=self.THEME["BG_GREY"],
                compound='left', disabledforeground=self.THEME["DISABLED_GREY"],
                foreground="white", highlightbackground=self.THEME["BG_GREY"],
                highlightcolor=self.THEME["TEXT_DARK"], text='''Log out''')

# Code related to scroll and special widgets, will be activated later.-------------------------------------------------
class AutoScroll(object):
    '''Configure the scrollbars for a widget.'''
    def __init__(self, master):
        #  Rozen. Added the try-except clauses so that this class
        #  could be used for scrolled entry widget for which vertical
        #  scrolling is not supported. 5/7/14.
        try:
            vsb = ttk.Scrollbar(master, orient='vertical', command=self.yview)
        except:
            pass
        hsb = ttk.Scrollbar(master, orient='horizontal', command=self.xview)
        try:
            self.configure(yscrollcommand=self._autoscroll(vsb))
        except:
            pass
        self.configure(xscrollcommand=self._autoscroll(hsb))
        self.grid(column=0, row=0, sticky='nsew')
        try:
            vsb.grid(column=1, row=0, sticky='ns')
        except:
            pass
        hsb.grid(column=0, row=1, sticky='ew')
        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)
        # Copy geometry methods of master  (taken from ScrolledText.py)
        methods = tk.Pack.__dict__.keys() | tk.Grid.__dict__.keys() \
                  | tk.Place.__dict__.keys()
        for meth in methods:
            if meth[0] != '_' and meth not in ('config', 'configure'):
                setattr(self, meth, getattr(master, meth))

    @staticmethod
    def _autoscroll(sbar):
        '''Hide and show scrollbar as needed.'''
        def wrapped(first, last):
            first, last = float(first), float(last)
            if first <= 0 and last >= 1:
                sbar.grid_remove()
            else:
                sbar.grid()
            sbar.set(first, last)
        return wrapped

    def __str__(self):
        return str(self.master)

def _create_container(func):
    '''Creates a ttk Frame with a given master, and use this new frame to
    place the scrollbars and the widget.'''
    def wrapped(cls, master, **kw):
        container = ttk.Frame(master)
        container.bind('<Enter>', lambda e: _bound_to_mousewheel(e, container))
        container.bind('<Leave>', lambda e: _unbound_to_mousewheel(e, container))
        return func(cls, container, **kw)
    return wrapped

class ScrolledWindow(AutoScroll, tk.Canvas):
    '''A standard Tkinter Canvas widget with scrollbars that will
    automatically show/hide as needed.'''
    @_create_container
    def __init__(self, master, **kw):
        tk.Canvas.__init__(self, master, **kw)
        AutoScroll.__init__(self, master)

import platform
def _bound_to_mousewheel(event, widget):
    child = widget.winfo_children()[0]
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        child.bind_all('<MouseWheel>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Shift-MouseWheel>', lambda e: _on_shiftmouse(e, child))
    else:
        child.bind_all('<Button-4>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Button-5>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Shift-Button-4>', lambda e: _on_shiftmouse(e, child))
        child.bind_all('<Shift-Button-5>', lambda e: _on_shiftmouse(e, child))

def _unbound_to_mousewheel(event, widget):
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        widget.unbind_all('<MouseWheel>')
        widget.unbind_all('<Shift-MouseWheel>')
    else:
        widget.unbind_all('<Button-4>')
        widget.unbind_all('<Button-5>')
        widget.unbind_all('<Shift-Button-4>')
        widget.unbind_all('<Shift-Button-5>')

def _on_mousewheel(event, widget):
    if platform.system() == 'Windows':
        widget.yview_scroll(-1*int(event.delta/120),'units')
    elif platform.system() == 'Darwin':
        widget.yview_scroll(-1*int(event.delta),'units')
    else:
        if event.num == 4:
            widget.yview_scroll(-1, 'units')
        elif event.num == 5:
            widget.yview_scroll(1, 'units')

def _on_shiftmouse(event, widget):
    if platform.system() == 'Windows':
        widget.xview_scroll(-1*int(event.delta/120), 'units')
    elif platform.system() == 'Darwin':
        widget.xview_scroll(-1*int(event.delta), 'units')
    else:
        if event.num == 4:
            widget.xview_scroll(-1, 'units')
        elif event.num == 5:
            widget.xview_scroll(1, 'units')
def start_up():
    GUI_support.main()

if __name__ == '__main__':
    GUI_support.main()




