# 🎬 Movie Revenue Analysis Dashboard

An interactive Streamlit dashboard for exploring movie performance data — revenue, budget, popularity, runtime, and audience ratings — across genres.

## Features

- **Sidebar Filters**
  - Genre (multi-select)
  - Budget range (slider)
  - Rating range (slider)
- **Dataset Preview** — browse the filtered data in a table
- **KPI Cards** — Total Movies, Average Revenue, Average Budget, Average Rating
- **Interactive Charts** (Plotly)
  - Top 10 Revenue Movies
  - Revenue by Genre
  - Budget vs Revenue (with trendline)
  - Popularity vs Revenue (with trendline)
  - Runtime Distribution
  - Rating Distribution
- **Business Insights** — key findings computed live from the filtered data (top genre, budget/popularity correlation with revenue, % profitable movies, average runtime, revenue lift for highly-rated movies)
- **Business Recommendations** — actionable suggestions based on the insights above

All KPIs, charts, insights, and recommendations update dynamically as you change the sidebar filters.

## Project Structure

```
.
├── app.py                 # Main Streamlit application
├── movies_cleaned.csv      # Dataset used by the app
├── requirements.txt        # Python dependencies
└── README.md
```

## Dataset

`movies_cleaned.csv` contains 2,000 movies with the following columns:

| Column         | Description                                  |
|----------------|-----------------------------------------------|
| `title`        | Movie title                                    |
| `genre`        | Movie genre (some rows are missing → shown as "Unknown") |
| `budget`       | Production budget ($)                          |
| `revenue`      | Box office revenue ($)                         |
| `profit`       | Revenue minus budget ($)                       |
| `popularity`   | Popularity score                               |
| `runtime`      | Runtime in minutes                             |
| `vote_average` | Average audience rating (0–10)                 |

## Requirements

- Python 3.9+
- Packages listed in `requirements.txt`:
  - `streamlit`
  - `pandas`
  - `plotly`
  - `statsmodels` (needed for scatter plot trendlines)

## Setup & Installation

1. Clone or download this project folder.
2. (Recommended) Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the App

Make sure `app.py` and `movies_cleaned.csv` are in the same folder, then run:

```bash
streamlit run app.py
```

The dashboard will open automatically in your browser at `http://localhost:8501`.

## Usage

1. Use the sidebar to filter by genre, budget range, and rating range.
2. Review the dataset preview and KPI cards for a quick summary.
3. Explore the charts to understand revenue drivers.
4. Read the Business Insights and Recommendations sections for a data-driven summary.

## Notes

- Movies with a missing `genre` value are labeled `"Unknown"` rather than removed, so they remain visible and filterable.
- If no movies match the selected filters, the app displays a warning and pauses further rendering until filters are adjusted.
- To use your own dataset, replace `movies_cleaned.csv` with a file that has the same column names, or update the column references in `app.py`.
