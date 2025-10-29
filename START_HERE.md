# 🚀 Quick Start Guide

Welcome! This guide will help you get started with your E-commerce Sales Analysis project.

---

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

---

## 🛠️ Setup (3 Simple Steps)

### Step 1: Create Virtual Environment

```bash
# Open terminal/command prompt in this directory
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Launch Jupyter

```bash
jupyter notebook
```

This will open Jupyter in your browser. Navigate to the `notebooks/` folder.

---

## 📥 Adding Your Data

1. **Download your dataset** from Kaggle or other sources
   - Recommended: [E-commerce Sales Data on Kaggle](https://www.kaggle.com/datasets)
   - Or use Superstore Sales dataset

2. **Place the raw data** in `data/raw/` folder
   ```bash
   # Example:
   data/raw/ecommerce_data.csv
   ```

3. **Document your data** in `data/README.md`

---

## 📓 Working with Notebooks

Follow this order in the `notebooks/` folder:

1. **01_data_loading.ipynb** → Load and inspect your data
2. **02_data_cleaning.ipynb** → Clean the data
3. **03_exploratory_analysis.ipynb** → Explore patterns
4. **06_dashboard.ipynb** → Create your final dashboard

---

## 🎯 Key Tasks

### ✅ What You Need to Do:

1. **Load data** into `01_data_loading.ipynb`
2. **Clean data** in `02_data_cleaning.ipynb`
3. **Analyze data** in `03_exploratory_analysis.ipynb`
4. **Create visualizations** in `06_dashboard.ipynb`
5. **Generate insights** and save in `reports/insights/`
6. **Save charts** in `reports/visualizations/`

---

## 📊 Expected Deliverables

Your final project should include:

1. ✅ Cleaned dataset (CSV in `data/processed/`)
2. ✅ Interactive dashboard notebook
3. ✅ Visualizations (charts saved as images)
4. ✅ Insights report (markdown or PDF)
5. ✅ KPIs calculated:
   - Total Revenue
   - Total Orders
   - Average Order Value
   - Best-selling Products
   - Sales Trends

---

## 💡 Pro Tips

- **Start small**: Begin with basic analysis before complex dashboards
- **Document everything**: Add comments and markdown cells
- **Version control**: Commit your work regularly
- **Save often**: Save your notebooks frequently
- **Test your code**: Run cells one by one to catch errors early

---

## 🆘 Need Help?

- Check the main [README.md](README.md) for detailed information
- Review [data/README.md](data/README.md) for data documentation
- Explore the `src/` folder for utility functions

---

## 🎨 Visualization Ideas

- Bar charts for top products/categories
- Line charts for sales trends over time
- Pie charts for category distribution
- Heatmaps for regional performance
- Interactive dashboards using Plotly

---

**Happy Analyzing! 📈**

