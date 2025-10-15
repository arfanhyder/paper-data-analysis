# nanoparticle_analyzer.py
#
# A script for analyzing bibliographic data to identify and count nanoparticle
# combinations in scientific literature, specifically for review articles.
#
# Purpose:
# 1. Reads a CSV file containing article data (Title, Abstract, Keywords, etc.).
# 2. Searches the text for predefined nanoparticles and their variations.
# 3. Identifies the unique combination of nanoparticles mentioned in each article.
# 4. Generates a LaTeX table summarizing the frequency of each combination and
#    the corresponding citations.
# 5. Generates a BibTeX (.bib) file containing formatted references for all
#    cited articles, ordered by their appearance in the table.
#
# Author: Gemini AI (based on user's iterative development)
# Date: October 15, 2025

import pandas as pd
import re
from collections import defaultdict, Counter
import unicodedata

# ==============================================================================
# --- 1. USER CONFIGURATION ---
# ==============================================================================
# Please update these values to match your project.

# The name of your input CSV file.
CSV_FILENAME = 'THNF575.csv'

# The dictionary mapping canonical nanoparticle names to their search variations.
# This is the "brain" of the search. Add or remove nanoparticles as needed.
# Format: 'Canonical Name': ['search_term_1', 'search_term_2', ...],
NANOPARTICLE_MAP = {
    'Alumina': [r'Al2O3', r'aluminum oxide', r'alumina'],
    'Titania': [r'TiO2', r'titanium dioxide', r'titania'],
    'Silica': [r'SiO2', r'silicon dioxide', r'silica'],
    'Copper Oxide': [r'CuO', r'cupric oxide', r'copper oxide'],
    'Zinc Oxide': [r'ZnO', r'zinc oxide'],
    'Magnetite': [r'Fe3O4', r'magnetite', r'iron oxide'],
    'Zirconia': [r'ZrO2', r'zirconium dioxide', r'zirconia'],
    'Graphene': [r'graphene', r'graphene nanoplatelets', r'GNP', 'graphene oxide', 'GO'],
    'Carbon Nanotube': [r'carbon nanotube', r'CNT', r'SWCNT', 'MWCNT'],
    'Diamond': [r'diamond', r'nano-diamond'],
    'Silver': [r'silver', r'Ag'],
    'Copper': [r'copper', 'Cu'],
    'Gold': [r'gold', 'Au'],
    'MXene': [r'mxene', r'ti3c2tx'],
    'Molybdenum Disulfide': [r'MoS2', r'molybdenum disulfide'],
}

# The dictionary for mapping names to their LaTeX chemical formulas for the table.
LATEX_SYMBOL_MAP = {
    'Alumina': r'\ce{Al2O3}', 'Titania': r'\ce{TiO2}', 'Silica': r'\ce{SiO2}',
    'Copper Oxide': r'\ce{CuO}', 'Zinc Oxide': r'\ce{ZnO}', 'Magnetite': r'\ce{Fe3O4}',
    'Zirconia': r'\ce{ZrO2}', 'Graphene': r'Graphene', 'Carbon Nanotube': r'CNT',
    'Diamond': r'Diamond', 'Silver': r'\ce{Ag}', 'Copper': r'\ce{Cu}', 'Gold': r'\ce{Au}',
    'MXene': r'MXene', 'Molybdenum Disulfide': r'\ce{MoS2}',
}

# ==============================================================================
# --- 2. HELPER FUNCTIONS ---
# ==============================================================================

def sanitize_text(text):
    """Removes or escapes special characters to prevent BibTeX errors."""
    if not isinstance(text, str):
        return ''
    # Normalize unicode to closest ASCII representation (e.g., accents)
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    # Escape characters that have special meaning in BibTeX
    replacements = {'&': r'\&', '%': r'\%', '$': r'\$', '#': r'\#', '_': r'\_', '{': r'\{', '}': r'\}'}
    for char, escaped_char in replacements.items():
        text = text.replace(char, escaped_char)
    return text

def generate_bib_key(authors, year, title):
    """Generates a unique citation key (e.g., 'author2023title') for an article."""
    try:
        s_authors = sanitize_text(str(authors))
        s_title = sanitize_text(str(title))
        
        # Extract the last name of the first author
        first_author_lastname = s_authors.split(',')[0].split()[-1].lower()
        clean_author = ''.join(c for c in first_author_lastname if c.isalnum())
        
        # Extract the first significant word of the title
        first_word_title = s_title.split()[0].lower()
        clean_title = ''.join(c for c in first_word_title if c.isalnum())
        
        year_str = str(int(year)) if pd.notna(year) else "nd" # "nd" for "no date"
        
        return f"{clean_author}{year_str}{clean_title}"
    except (IndexError, AttributeError, ValueError):
        # Fallback for entries with missing or unusual data
        return f"ref_{abs(hash(title))}"

# ==============================================================================
# --- 3. MAIN ANALYSIS LOGIC ---
# ==============================================================================

def analyze_literature():
    """Main function to perform the entire analysis and generate output files."""
    # --- Load Data ---
    try:
        df = pd.read_csv(CSV_FILENAME)
        print(f"✅ Successfully loaded '{CSV_FILENAME}'. Found {len(df)} articles.")
    except FileNotFoundError:
        print(f"❌ Error: File not found. Please make sure '{CSV_FILENAME}' is in the same directory as the script.")
        return

    # --- Pre-process Data and Generate Unique BibTeX Keys ---
    bib_keys = []
    seen_keys_count = defaultdict(int)
    for index, row in df.iterrows():
        base_key = generate_bib_key(row.get('Authors'), row.get('Year'), row.get('Title'))
        count = seen_keys_count[base_key]
        seen_keys_count[base_key] += 1
        # If key is a duplicate, append a number (e.g., author2023title2)
        unique_key = base_key if count == 0 else f"{base_key}{count+1}"
        bib_keys.append(unique_key)
    df['bib_key'] = bib_keys
    
    # Combine text fields for a comprehensive search
    text_columns = ['Title', 'Abstract', 'Keywords', 'Index Keywords']
    df['combined_text'] = df[text_columns].fillna('').agg(' '.join, axis=1)

    # --- Identify Nanoparticle Combinations in Each Article ---
    combination_keys = defaultdict(list)
    article_counts = Counter()

    for index, row in df.iterrows():
        nanoparticles_found = set()
        for name, variations in NANOPARTICLE_MAP.items():
            # Check if any variation exists in the article's text (case-insensitive)
            if any(re.search(r'\b' + re.escape(v) + r'\b', row['combined_text'], re.IGNORECASE) for v in variations):
                nanoparticles_found.add(name)
        
        num_found = len(nanoparticles_found)
        if num_found > 0:
            # Store the combination and its citation key
            combo_key = tuple(sorted(list(nanoparticles_found)))
            combination_keys[combo_key].append(row['bib_key'])
            
            # Update summary statistics
            if num_found == 1: article_counts['mono'] += 1
            elif num_found == 2: article_counts['binary'] += 1
            elif num_found == 3: article_counts['ternary'] += 1
            else: article_counts['other'] += 1

    # --- Sort and Prepare Data for LaTeX Table ---
    table_data = sorted(
        [{'combo': combo, 'freq': len(keys), 'keys': keys} for combo, keys in combination_keys.items()],
        key=lambda x: (len(x['combo']), x['freq']), # Sort by num particles, then by frequency
        reverse=True
    )

    # --- Generate LaTeX Table Rows ---
    latex_table_rows = []
    all_ordered_cite_keys = []
    for item in table_data:
        latex_combo_str = ' + '.join([LATEX_SYMBOL_MAP.get(name, name) for name in item['combo']])
        cite_str = r'\cite{' + ','.join(item['keys']) + '}'
        latex_table_rows.append(f"  {latex_combo_str} & {item['freq']} & {cite_str} \\\\ \\hline")
        all_ordered_cite_keys.extend(item['keys'])
    
    unique_ordered_keys = list(dict.fromkeys(all_ordered_cite_keys)) # Remove duplicates while preserving order

    # --- Generate BibTeX (.bib) File Content ---
    final_bib_content = []
    key_to_article_map = df.set_index('bib_key')
    for key in unique_ordered_keys:
        try:
            article = key_to_article_map.loc[key]
            pages = f"{int(article['Page start'])}--{int(article['Page end'])}" if pd.notna(article['Page start']) and pd.notna(article['Page end']) else ''
            
            entry = (f"@article{{{key},\n"
                     f"  title={{{sanitize_text(article.get('Title', ''))}}},\n"
                     f"  author={{{sanitize_text(article.get('Authors', '')).replace(',', ' and')}}},\n"
                     f"  journal={{{sanitize_text(article.get('Source title', ''))}}},\n"
                     f"  volume={{{str(article.get('Volume', ''))}}},\n"
                     f"  pages={{{pages}}},\n"
                     f"  year={{{int(article.get('Year', 0))}}},\n"
                     f"  publisher={{{sanitize_text(article.get('Publisher', ''))}}},\n"
                     f"  doi={{{article.get('DOI', '')}}}\n"
                     f"}}")
            final_bib_content.append(entry)
        except Exception as e:
            print(f"⚠️ Warning: Could not create BibTeX entry for key {key}. Error: {e}")

    # --- Save Output Files ---
    with open('references.bib', 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(final_bib_content))
    
    with open('latex_table.tex', 'w', encoding='utf-8') as f:
        f.write('\n'.join(latex_table_rows))

    # --- Print Final Summary and Instructions ---
    print("\n" + "="*50)
    print("📊 ANALYSIS SUMMARY")
    print("="*50)
    print(f"Articles with 1 nanoparticle (Mono):   {article_counts['mono']}")
    print(f"Articles with 2 nanoparticles (Binary): {article_counts['binary']}")
    print(f"Articles with 3 nanoparticles (Ternary):{article_counts['ternary']}")
    print(f"Articles with 4+ nanoparticles:       {article_counts['other']}")
    print("\n" + "="*50)
    print("✅ SCRIPT COMPLETE")
    print("="*50)
    print("Two files have been generated:")
    print("1. latex_table.tex - Contains the body of your LaTeX table.")
    print("2. references.bib  - Contains the BibTeX entries for your citations.")
    print("\nNext steps: Add these files to your LaTeX project and use them in your main document.")


# ==============================================================================
# --- 4. RUN SCRIPT ---
# ==============================================================================
if __name__ == "__main__":
    analyze_literature()