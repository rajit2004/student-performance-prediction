# 🎓 Student Performance Prediction System

A Machine Learning powered web application that predicts student academic performance based on behavioral, academic, and engagement parameters.

This system allows administrators or academic staff to input student data and obtain a predicted performance category using a trained Random Forest classification model.

The application also includes an analytics dashboard to visualize student performance trends.

---
# Live Demo

https://student-performance-prediction-22fsp6ypmbcfcwxbqdmo6.streamlit.app

---

# 📌 Project Overview

Student performance is influenced by many factors such as study habits, academic engagement, class participation, and sleep patterns.

This project uses **Machine Learning classification techniques** to analyze these factors and predict whether a student’s performance is likely to be:

- Poor
- Average
- Good
- Excellent

The system is implemented as an **interactive web application using Streamlit**.

---

# ⚙️ Technologies Used

- **Python**
- **Streamlit** (Web application framework)
- **Scikit-learn** (Machine Learning)
- **Pandas** (Data processing)
- **NumPy** (Numerical computing)
- **Matplotlib & Seaborn** (Data visualization)

---

# 🧠 Machine Learning Model

The application uses a **Random Forest Classifier**.

Random Forest was selected because:

- It handles classification problems effectively
- It works well with mixed feature types
- It reduces overfitting through ensemble learning

### Input Features

The prediction model considers the following student parameters:

- Daily Study Time
- Study Consistency
- Assignment Completion Rate
- Class Participation
- Previous Semester Average
- Sleep Duration
- Monthly Absences
- Age

These parameters represent both **academic engagement and behavioral indicators**.

---

# 🚀 Features

### 🔐 Login System
- Role based access
- Admin and Staff login

### 🧾 Student Data Entry
Users can enter student academic information including:

- Study habits
- Assignment completion
- Participation level
- Previous grades
- Sleep patterns

### 🤖 Performance Prediction
The system predicts student performance into categories:

- Poor
- Average
- Good
- Excellent

### 📊 Analytics Dashboard (Admin Only)

The admin panel includes:

- Total student records
- Average absence statistics
- Performance distribution chart
- Study time vs absence heatmap
- Student search functionality
- CSV export for records

### 🔄 Predict Another Student
The form resets after each prediction for quick entry of multiple students.

---

# 📊 Visualizations

The system generates the following analytics:

### Performance Distribution
Bar chart showing number of students in each performance category.

### Study vs Absence Heatmap
Visual representation of how study time and absence levels correlate with student outcomes.

---


---

# ☁️ Deployment

This project can be deployed using:

- **Streamlit Community Cloud**
- **Docker**
- **AWS / Azure**
- **Heroku**

For easy deployment use **Streamlit Community Cloud**.

---

# 🎯 Future Improvements

Possible future enhancements include:

- Integration with real academic datasets
- Advanced ML models (XGBoost, Neural Networks)
- Feature importance visualization
- Student risk detection system
- Automated academic recommendations
- Database integration (PostgreSQL / MongoDB)

---

# 📚 Academic Use

This project was developed as part of a **Machine Learning / Data Science academic project** to demonstrate:

- Classification algorithms
- Educational data mining
- Interactive analytics dashboards
- Machine learning deployment

---

# 👨‍💻 Author

Ranesh Rajit
Computer Science Engineering Student

---

# 📜 License

This project is open source and available for educational use.
