#  Movie Rating Analysis & Prediction

##  Overview

This project explores how key attributes of movies — such as **budget**, **genre**, **duration**, and **number of ratings** — influence **IMDb scores**. The goal is to identify what makes a movie highly rated and to **predict movie ratings** using machine learning techniques.

---

##  Objectives

- Scrape and clean real-world movie data from IMDb and other sources.
- Perform exploratory data analysis to find insights about high-rated movies.
- Train a **Random Forest** model to predict IMDb ratings based on features like genre, budget, and duration.
- Draw statistical insights on genre popularity and performance trends.

---

##  Dataset Summary

All cleaned data are stored in the `/data` folder:
- `movie_api_top_250.json`
- `movie_budget.json`
- `movie_info.json`
- `movie_imb_data.csv`
- `movie_url.json`

Data was scraped from the web and transformed into structured formats for analysis.

---

##  Key Findings

-  Action movies dominate the top-rated and most-followed categories.
-  Animation movies are shorter and tend to receive higher scores.
-  Budget and runtime are strong predictors of a film’s rating.
-  Random Forest model achieved **95%+ accuracy** in predicting rating tiers.

---

##  How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the scraping and transformation pipeline
```bash
cd src
python main.py       # Scrapes data and stores JSON
python extract.py    # Converts JSON into CSV for analysis
```

### 3. Open the analysis notebook
Open `report.ipynb` in Jupyter Notebook to explore the full analysis and modeling steps.

---

##  File Structure

```
Zhuoyou-Shen-DSCI510-Project/
│
├── data/                 # All raw and cleaned movie datasets
├── src/                  # Python scripts for scraping and data extraction
│   ├── main.py
│   └── extract.py
├── report.ipynb          # Main analysis notebook
├── report.pdf            # PDF version of the notebook
├── requirements.txt      # List of dependencies
└── readme.txt            # Initial instructions (replaced by this README)
```

---

##  Known Limitations

- Web scraping may take more than 10 minutes.
- Data may have missing fields depending on source availability.
- Model performance might not generalize well beyond IMDb top movies.

---

##  Tools & Libraries Used

- Python (Pandas, NumPy, Scikit-learn, Seaborn)
- Requests & BeautifulSoup for web scraping
- Jupyter Notebook

