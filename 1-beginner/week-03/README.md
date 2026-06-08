# 🌸 Iris Dataset Analysis

A beginner-friendly data analysis project using Python's **Pandas** and **NumPy** libraries to explore and summarise the classic Iris dataset.

---

## 📋 Overview

This script performs a full statistical exploration of the [Iris dataset](https://scikit-learn.org/stable/datasets/toy_dataset.html#iris-dataset) — one of the most well-known datasets in data science. It covers data exploration, descriptive statistics, and feature correlation analysis.

---

## 📁 Project Structure

```
iris-analysis/
│
├── iris_analysis.py   # Main analysis script
└── README.md          # You're here
```

---

## 🔍 What It Does

### Step 1 — Data Exploration
- Previews the first 5 rows with `data.head()`
- Checks column names, data types, and null counts with `data.info()`
- Generates automatic summary statistics (count, mean, std, quartiles) with `data.describe()`

### Step 2 — Basic Statistics
- Calculates **mean, median, mode, and standard deviation** for each numerical feature
- Produces a **correlation matrix** with `data.corr()`
- Highlights strong correlations (|r| > 0.8) with human-readable output

---

## 📊 Key Findings

| Feature Pair | Correlation (r) | Strength |
|---|---|---|
| Petal length ↔ Petal width | 0.9629 | Very strong positive |
| Sepal length ↔ Petal length | 0.8718 | Strong positive |
| Sepal length ↔ Petal width | 0.8179 | Strong positive |
| Sepal width ↔ anything | < 0.43 | Weak / negative |

> Petal dimensions are highly correlated with each other and with sepal length, making them strong candidates for species classification.

---

## 🛠️ Requirements

- Python 3.7+
- pandas
- numpy
- scikit-learn

Install dependencies:

```bash
pip install pandas numpy scikit-learn
```

---

## 🚀 Usage

```bash
python iris_analysis.py
```

No arguments needed — the dataset is loaded automatically from scikit-learn.

---

## 📦 Dataset

The **Iris dataset** contains 150 samples across 3 species (*setosa*, *versicolor*, *virginica*) with 4 features each:

- Sepal length (cm)
- Sepal width (cm)
- Petal length (cm)
- Petal width (cm)

It has **no missing values** and is fully numerical (except the species label), making it ideal for introductory analysis.

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
