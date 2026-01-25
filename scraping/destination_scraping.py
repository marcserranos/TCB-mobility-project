import pandas as pd
from bs4 import BeautifulSoup
import re

# 1. LOAD THE HTML FILE
# Replace 'erasmus_list.html' with the actual name of the file you saved
file_path = 'erasmus_entries_upf.html'

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
except FileNotFoundError:
    print(f"Error: Could not find '{file_path}'. Make sure to save the webpage as an HTML file first.")
    exit()

soup = BeautifulSoup(html_content, 'html.parser')

# 2. FIND ALL UNIVERSITY ENTRIES
# Based on your screenshot, each entry is a div with class "llistat_item"
items = soup.find_all('div', class_='llistat_item')

print(f"Found {len(items)} entries. Starting scrape...")

data = []

# 3. ITERATE AND EXTRACT
for idx, item in enumerate(items):
    # --- A. Basic Setup ---
    entry = {
        'ID': idx,
        'Name': None,
        'Country': None,
        'City': None,
        'Program': None,
        'Studies': None,
        'Observations': None,
        'Spots': None,
        'Duration Months': None,
        'Languages': None,
        'Grade': None,
        'Website': None,
        'Factsheet': None
    }

    # --- B. Get Name ---
    # The name is always in the <h3> tag
    name_tag = item.find('h3')
    if name_tag:
        entry['Name'] = name_tag.get_text(strip=True)

    # --- C. Get Country and City ---
    # These are always the first text node in the first <p> tag
    paragraphs = item.find_all('p')
    if paragraphs:
        # Get the first paragraph's text content, but stop before child tags (spans)
        # .contents[0] usually grabs the text node "Argentina, Buenos Aires" before the <br>
        first_p_text = paragraphs[0].contents[0] if paragraphs[0].contents else ""
        
        if isinstance(first_p_text, str):
            clean_loc = first_p_text.strip().replace('"', '') # Clean quotes/spaces
            # Split by the FIRST comma only, as requested
            if ',' in clean_loc:
                parts = clean_loc.split(',', 1)
                entry['Country'] = parts[0].strip()
                entry['City'] = parts[1].strip()
            else:
                entry['Country'] = clean_loc # Fallback if no comma

    # --- D. Extract Labeled Fields (Robust Method) ---
    # Instead of relying on fixed paragraph positions (p[1] vs p[2]),
    # we search for the labels anywhere inside the item.
    
    # Map the Catalan labels from the HTML to your English columns
    label_map = {
        'Programa:': 'Program',
        'Estudis:': 'Studies',
        'Observacions:': 'Observations',
        'Places:': 'Spots',
        'Durada:': 'Duration Months',
        'Idioma requerit:': 'Languages',
        'Nota mitjana:': 'Grade',  # Assuming standard label; will catch if present
        'Nota:': 'Grade'
    }

    spans = item.find_all('span', class_='etiq')
    for span in spans:
        label_text = span.get_text(strip=True)
        
        # Check if this label is one we care about
        # We check keys since labels might have slight variations, but usually exact matches work
        target_field = label_map.get(label_text)
        
        # Handle " | Durada:" which has a pipe separator in the label sometimes
        if not target_field and 'Durada' in label_text:
            target_field = 'Duration Months'

        if target_field:
            # The value is the text node immediately following the span
            # We use next_sibling to get the text right after </span>
            value_node = span.next_sibling
            
            if value_node:
                text_val = str(value_node).strip()
                # Clean up common debris
                text_val = text_val.strip('"').strip('|').strip()
                # Remove trailing semicolons for cleaner look (optional)
                if text_val.endswith(';'):
                    text_val = text_val[:-1]
                
                entry[target_field] = text_val

    # --- E. Extract Links ---
    # Links are usually in the last paragraph
    links = item.find_all('a')
    for link in links:
        href = link.get('href')
        if not href:
            continue
            
        # Heuristic to differentiate Website vs Factsheet
        # Usually website is short/root domain, factsheet is a PDF or long URL
        # Or based on position: 1st is usually website, 2nd is factsheet
        
        if 'pdf' in href.lower() or 'documents' in href.lower():
            entry['Factsheet'] = href
        elif entry['Website'] is None: 
            # If we haven't found a website yet, assume the first non-pdf link is it
            entry['Website'] = href
        else:
            # If we already have a website, this might be the factsheet (fallback)
            entry['Factsheet'] = href

    data.append(entry)

# 4. EXPORT TO EXCEL/CSV
df = pd.DataFrame(data)

# Reorder columns to match your exact request
columns_ordered = [
    'ID', 'Name', 'Country', 'City', 'Program', 'Studies', 
    'Observations', 'Spots', 'Duration Months', 'Languages', 
    'Grade', 'Website', 'Factsheet'
]
df = df[columns_ordered]

output_filename = 'erasmus_destinations.csv'
df.to_csv(output_filename, index=False)

print(f"Done! Scraped {len(df)} rows. Saved to '{output_filename}'.")
print(df.head())