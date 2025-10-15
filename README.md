# Nanoparticle Literature Analysis for Review Article

This repository contains the data and Python script used to analyze the literature for the review article titled "[Your Article Title Here]". The script automates the process of identifying nanoparticle combinations in a curated list of publications and generates a LaTeX table and a BibTeX file for citation.

## Purpose

The goal of this project is to provide a transparent and reproducible method for our literature analysis. The script `nanoparticle_analyzer.py` processes a bibliographic CSV file to:
- Identify mentions of predefined nanoparticles within the titles, abstracts, and keywords.
- Group publications by the unique combination of nanoparticles they discuss (mono, binary, ternary, etc.).
- Calculate the frequency of each combination.
- Generate a LaTeX-formatted table of the results, complete with citations.
- Generate a corresponding `.bib` file with all necessary references, ordered by their appearance in the table.

## How to Run the Code

### Prerequisites
- Python 3.6+
- Pandas library (`pip install pandas`)

### Instructions
1. Ensure you have both `nanoparticle_analyzer.py` and the data file (`THNF670.csv`) in the same directory.
2. Open a terminal or command prompt in that directory.
3. Run the script using the command:
   ```sh
   python nanoparticle_analyzer.py
   ```
4. Upon successful execution, two new files will be created:
   - `latex_table.tex`: Contains the rows for the summary table.
   - `references.bib`: The BibTeX database for the citations.

## Using the Output
1. Add the `references.bib` file to your LaTeX project and link it using `\bibliography{references}`.
2. Copy the contents of `latex_table.tex` into the body of your `longtable` environment in your main `.tex` document.