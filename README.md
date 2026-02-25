# TCB-mobility-project
This repo contains the full TCB II final project (now in development). 
An app that scrapes, processes, enriches and displays erasmus and mobility programs information from UPF. And matches them according to the student's preferences.

- All libraries used are contained on the "requirements.txt" file.

CURRENT REPO DISTRIBUTION: 
- main.py: application entry point; initializes the GUI and wires interface actions.
- mobilityManager.py: central class, manager of universities/users and CSV persistence.
- GUI.py: Tkinter visual layout and widgets.
- GUI_logic.py: GUI behavior, navigation, authentication, and admin/student actions.
- user.py: base user, admin, and student class definitions.
- university.py: university and location entity classes.
- utilities.py: helper utilities (e.g., random ID generation).
- socring.py: scoring engine skeleton for affinity/risk ranking.
- scraping/: experimental scripts for data scraping (read SCRAPING_README.md).
- data/: CSV files used as the app database and persistence memory.
- images/: logo files associated with universities.


Aleix Ruf i Marc Serrano.
Enginyeria Biomèdica UPF
