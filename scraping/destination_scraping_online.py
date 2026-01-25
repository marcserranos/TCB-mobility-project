import requests
import pandas as pd
from bs4 import BeautifulSoup
import time

# 1. SETUP URL
url = "https://www.upf.edu/web/estudiarfora/destinacions"
print(f"Fetching data from: {url}")

try:
    response = requests.get(url)
    response.raise_for_status() # Check for HTTP errors
    html_content = response.content
except requests.exceptions.RequestException as e:
    print(f"Error fetching the URL: {e}")
    exit()

soup = BeautifulSoup(html_content, 'html.parser')

# 2. FIND ALL ENTRIES
items = soup.find_all('div', class_='llistat_item')
print(f"Found {len(items)} entries. Starting scrape...")

data = []

# 3. ITERATE AND EXTRACT
for idx, item in enumerate(items):
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

    # --- Name ---
    name_tag = item.find('h3')
    if name_tag:
        entry['Name'] = name_tag.get_text(strip=True)

    # --- Country and City ---
    # Usually the first text node in the first paragraph
    paragraphs = item.find_all('p')
    if paragraphs:
        first_p_text = paragraphs[0].contents[0] if paragraphs[0].contents else ""
        if isinstance(first_p_text, str):
            clean_loc = first_p_text.strip().replace('"', '')
            if ',' in clean_loc:
                parts = clean_loc.split(',', 1)
                entry['Country'] = parts[0].strip()
                entry['City'] = parts[1].strip()
            else:
                entry['Country'] = clean_loc

    # --- Labeled Fields ---
    # Map Catalan labels to your English columns
    label_map = {
        'Programa:': 'Program',
        'Estudis:': 'Studies',
        'Observacions:': 'Observations',
        'Places:': 'Spots',
        'Durada:': 'Duration Months',
        'Idioma requerit:': 'Languages',
        'Nota mínima:': 'Grade', # Updated based on verification
        'Nota:': 'Grade'
    }

    spans = item.find_all('span', class_='etiq')
    for span in spans:
        label_text = span.get_text(strip=True)
        
        # Check against our map
        # We use 'in' to handle cases like " | Durada:"
        target_field = None
        for key, field in label_map.items():
            if key in label_text:
                target_field = field
                break
        
        if target_field:
            # Get the text immediately following the span
            value_node = span.next_sibling
            if value_node:
                text_val = str(value_node).strip()
                # Clean up format (remove pipes, quotes, trailing semicolons)
                text_val = text_val.strip('|').strip('"').strip()
                if text_val.endswith(';'):
                    text_val = text_val[:-1]
                
                entry[target_field] = text_val.strip()

    # --- Links (Website vs Factsheet) ---
    links = item.find_all('a')
    for link in links:
        href = link.get('href')
        text = link.get_text(strip=True).lower()
        
        if not href: 
            continue

        # Logic: Check anchor text first ("Lloc web" vs "Factsheet")
        if 'factsheet' in text or 'pdf' in href.lower() or 'documents' in href.lower():
            entry['Factsheet'] = href
        elif 'web' in text or 'website' in text:
            entry['Website'] = href
        else:
            # Fallback if no clear text label
            if not entry['Website']:
                entry['Website'] = href

    data.append(entry)

# 4. EXPORT
df = pd.DataFrame(data)

# Reorder columns
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