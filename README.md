# 🏅 Olympics Insights Dashboard

An interactive dashboard and data analysis project that explores over a century of Olympic Games history. Using athlete performance data, this project provides insights into participation, medals, countries, and sports through both data visualization and an interactive dashboard.

👉 **Live App**: [Olympics Insights Dashboard](https://olympics-insights-dashboard-9utdirfdhgf4cgefnrh5zf.streamlit.app/)

---

## 📌 Project Overview

This project uses the **Olympics dataset (`athlete_events.csv`)** along with the **NOC regions mapping (`noc_regions.csv`)** to analyze trends in the Olympics.
It combines **exploratory data analysis (EDA)** in Jupyter Notebook with a **Streamlit-based dashboard** for interactive exploration.

Key questions addressed:

* How has athlete participation evolved over time?
* Which countries dominate medal counts?
* Gender distribution in sports participation across decades.
* Evolution of specific sports in terms of popularity.
* Country-specific medal tallies and performance trends.

---

## 📂 Repository Structure

```
Olympics-Insights-Dashboard/
│
├── app.py                  # Main dashboard app (Streamlit)
├── preprocessor.py         # Data cleaning and preprocessing functions
├── helper.py               # Utility/helper functions for analysis
├── olympic_analysis.ipynb  # Jupyter notebook for EDA
│
├── athlete_events.zip      # Dataset (compressed CSV of athlete events)
├── noc_regions.csv         # Mapping of NOC codes to regions
│
├── requirements.txt        # Dependencies
└── README.md               # Project documentation
```

---

## ⚙️ Installation & Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/nileshgorai-byte/Olympics-Insights-Dashboard.git
   cd Olympics-Insights-Dashboard
   ```

2. **Create and activate a virtual environment** (recommended)

   ```bash
   python -m venv venv
   source venv/bin/activate    # On Linux/Mac
   venv\Scripts\activate       # On Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Extract the dataset**

   ```bash
   unzip athlete_events.zip
   ```

---

## ▶️ Running the Dashboard Locally

Start the Streamlit app:

```bash
streamlit run app.py
```

The dashboard will open in your browser (usually at **[http://localhost:8501](http://localhost:8501)**).

Or skip the setup and view it directly here:
👉 [Olympics Insights Dashboard (Live)](https://olympics-insights-dashboard-9utdirfdhgf4cgefnrh5zf.streamlit.app/)

---

## 📊 Features

* **Interactive Medal Tally**: Explore medal counts by country and year.
* **Overall Trends**: Visualize participation growth over decades.
* **Country-Specific Analysis**: Drill down into individual country performance.
* **Athlete Analysis**: Insights on gender participation and top-performing athletes.
* **Sport-wise Analysis**: Trends in the rise and decline of sports.

---

## 📈 Dataset

* **Athlete Events**: Records of athletes, events, medals from 1896–2016.
* **NOC Regions**: Mapping between National Olympic Committees and regions.

Source: [Olympics Dataset on Kaggle](https://www.kaggle.com/datasets/heesoo37/120-years-of-olympic-history-athletes-and-results)

---

## 💡 Future Improvements

* Add live data from the latest Olympics.
* Include predictive analysis (e.g., medal forecasts).
* Deploy dashboard online (Streamlit Cloud / Heroku).
* Enhance visualizations with Plotly for richer interactivity.

---

## 🤝 Contributing

Contributions are welcome! Feel free to fork the repo, raise issues, or submit pull requests.

---

## 📜 License

This project is licensed under the MIT License.

---
