# Code and Data for "Machine Learning Insights into Ternary Hybrid Nanofluids"

This repository contains all the data and code used for the analysis in the paper: **"Machine Learning Insights into Ternary Hybrid Nanofluids, A Structural Topic Modeling Approach to Thematic Landscapes, Material Trends, and Future Frontiers"**.

The goal of this repository is to ensure the complete transparency and reproducibility of our research. The analysis is divided into two parts, each using a different script.

## Repository Contents 📂

-   **`nanoparticle_analyzer.py`**: A Python script to identify nanoparticle combinations and generate a LaTeX table and BibTeX file.
-   **`THNF_STM_Analysis.R`**: An R script to perform the Structural Topic Model (STM) analysis and generate figures.
-   **`THNF575.csv`** & **`THNF_575_articles.csv`**: The bibliographic datasets used by the Python and R scripts, respectively.
-   **`output_plots/`**: A folder created by the R script to store the STM figures.

---

## Part 1: Nanoparticle Combination Analysis (Python)

This analysis identifies the combinations of nanoparticles discussed in the literature and generates a LaTeX table of their frequencies and citations.

### How to Run the Python Script

**Prerequisites:**
- Python 3.6+
- Pandas library (`pip install pandas`)

**Instructions:**
1.  Ensure you have both `nanoparticle_analyzer.py` and `THNF575.csv` in the same directory.
2.  Open a terminal or command prompt in that directory.
3.  Run the script using the command:
    ```sh
    python nanoparticle_analyzer.py
    ```
4.  Two files will be created: `latex_table.tex` and `references.bib`.

---

## Part 2: Structural Topic Modeling (R)

This analysis uses STM to identify the 9 core research topics in the THNF literature, analyze their trends over time, and visualize their relationships.

### How to Run the R Script

**Prerequisites:**
- R and RStudio
- The script will automatically install the necessary R packages.

**Instructions:**
1.  Open the `THNF_STM_Analysis.R` script in RStudio.
2.  Ensure the `THNF_575_articles.csv` file is in the same directory.
3.  Run the entire script by clicking the "Source" button in RStudio.
4.  The script will save all generated figures (trends, proportions, network) into a new folder named `output_plots`.