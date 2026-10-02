# 🚦 SmartRoute AI

## ML-Based Traffic-Aware Route Recommendation System

SmartRoute AI is a Machine Learning-based route recommendation system designed to predict travel time and compare alternative routes using traffic, road, weather, construction and drainage conditions.

## 🎯 Objectives

- Predict expected travel time
- Analyze traffic conditions
- Identify construction activity
- Detect drainage and waterlogging problems
- Consider road condition and weather
- Compare alternative routes
- Recommend a route based on predicted travel time

## 🤖 Machine Learning Model

The project uses **Random Forest Regression** to predict travel time.

### Input Features

- Traffic Level
- Construction
- Drainage Leak
- Road Condition
- Weather
- Distance
- Time of Day

### Output

The model predicts:

**Travel Time in minutes**

## 🛣️ Alternative Route Comparison

The application compares three simulated route scenarios:

- **Route A – Main Road**
- **Route B – Alternative Road**
- **Route C – Outer Road**

The Machine Learning model predicts the expected travel time for each route.

## 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- Streamlit
- Matplotlib
- CSV
- Random Forest Regression

## 📁 Project Structure

```text
SmartRouteAI/
│
├── app.py
├── train_model.py
├── data.csv
├── model.pkl
└── requirements.txt
