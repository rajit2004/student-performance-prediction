import streamlit as st
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import seaborn as sns
import matplotlib.pyplot as plt

# ================= PAGE CONFIG =================
st.set_page_config(page_title="Student Performance System", layout="wide")

# ================= SESSION STATE =================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = ""
    st.session_state.username = ""

if "students" not in st.session_state:
    st.session_state.students = []

if "form_id" not in st.session_state:
    st.session_state.form_id = 0


# ================= RESET FORM =================
def reset_form():
    st.session_state.form_id += 1


# ================= MODEL =================
@st.cache_resource
def load_model():

    X = np.array([
        [1,1,1,1,1,1,18],
        [2,2,2,2,2,2,19],
        [3,3,3,3,3,3,20],
        [4,4,4,4,4,4,21],
        [2,3,2,3,2,3,18],
        [1,2,1,2,1,2,19],
        [3,4,3,4,3,4,20],
        [4,4,4,4,4,4,22]
    ])

    y = np.array([
        "Poor",
        "Average",
        "Good",
        "Excellent",
        "Average",
        "Poor",
        "Good",
        "Excellent"
    ])

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X,y)

    return model


model = load_model()

USERS = {
    "admin":"admin123",
    "staff":"staff123"
}


# ================= LOGIN PAGE =================
def login_page():

    st.title("🎓 Student Performance System")
    st.caption("Academic analytics and prediction dashboard")

    col1, col2, col3 = st.columns([2,3,2])

    with col2:

        st.subheader("🔐 Login")

        username = st.text_input(
            "Username",
            value="",
            placeholder="Enter your username"
        )

        password = st.text_input(
            "Password",
            type="password",
            value="",
            placeholder="Enter password"
        )

        login_btn = st.button("Login", use_container_width=True)

        if login_btn:

            if username in USERS and USERS[username] == password:

                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.role = "admin" if username == "admin" else "staff"

                st.rerun()

            else:
                st.error("Invalid username or password")


# ================= PREDICTION FORM =================
def prediction_form():

    st.subheader("Student Information")

    with st.form(key=f"student_form_{st.session_state.form_id}"):

        col1, col2 = st.columns(2)

        with col1:

            name = st.text_input("Student Name", value="")

            age = st.number_input(
                "Age",
                min_value=15,
                max_value=30,
                value=18
            )

            study = st.selectbox(
                "Daily Study Time",
                ["Select...","<1 hr","1-2 hrs","2-4 hrs","4-6 hrs",">6 hrs"],
                index=0
            )

            consistency = st.selectbox(
                "Study Consistency",
                ["Select...","Rarely","Sometimes","Regular","Very Regular"],
                index=0
            )

        with col2:

            absences = st.number_input(
                "Monthly Absences",
                min_value=0,
                max_value=30,
                value=0
            )

            assignment = st.selectbox(
                "Assignment Completion Rate",
                ["Select...","Low","Medium","High","Very High"],
                index=0
            )

            participation = st.selectbox(
                "Class Participation",
                ["Select...","Low","Moderate","High"],
                index=0
            )

        st.subheader("Academic Environment")

        col3, col4 = st.columns(2)

        with col3:

            prev_grade = st.selectbox(
                "Previous Semester Average",
                ["Select...","<50","50-60","60-75",">75"],
                index=0
            )

        with col4:

            sleep = st.selectbox(
                "Sleep Duration",
                ["Select...","<5 hrs","5-6 hrs","6-7 hrs",">7 hrs"],
                index=0
            )

        submit = st.form_submit_button(
            "Predict Performance",
            use_container_width=True
        )

    # ================= PREDICTION =================
    if submit:

        if (
            name == "" or
            "Select..." in [study, consistency, assignment, participation, prev_grade, sleep]
        ):
            st.warning("Please fill all fields before predicting.")
            return

        map_val = {
            "<1 hr":1,"1-2 hrs":2,"2-4 hrs":3,"4-6 hrs":4,">6 hrs":5,
            "Rarely":1,"Sometimes":2,"Regular":3,"Very Regular":4,
            "Low":1,"Medium":2,"High":3,"Very High":4,
            "Moderate":2,"High":3,
            "<50":1,"50-60":2,"60-75":3,">75":4,
            "<5 hrs":1,"5-6 hrs":2,"6-7 hrs":3,">7 hrs":4
        }

        vector = [[
            map_val[study],
            map_val[assignment],
            map_val[consistency],
            map_val[participation],
            map_val[prev_grade],
            map_val[sleep],
            age
        ]]

        pred = model.predict(vector)[0]

        st.success(f"Predicted Performance: {pred}")

        st.session_state.students.append({
            "Name":name,
            "Study":study,
            "Absences":absences,
            "Prediction":pred
        })

        st.button(
            "Predict Another Student",
            on_click=reset_form,
            use_container_width=True
        )


# ================= ADMIN DASHBOARD =================
def admin_dashboard():

    st.divider()

    st.subheader("Analytics Dashboard")

    if not st.session_state.students:
        st.info("No records yet")
        return

    df = pd.DataFrame(st.session_state.students)

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Records", len(df))
    col2.metric("Avg Absences", round(df["Absences"].mean(),2))
    col3.metric("Top Result", df["Prediction"].mode()[0])

    st.divider()

    st.subheader("Student Search")

    search = st.text_input("Search Student")

    if search:
        df = df[df["Name"].str.contains(search,case=False)]

    st.dataframe(df, use_container_width=True, hide_index=True)

    st.divider()

    st.subheader("Performance Distribution")

    st.bar_chart(df["Prediction"].value_counts())

    st.divider()

    st.subheader("Performance Heatmap")

    heat = pd.pivot_table(
        df,
        values="Prediction",
        index="Study",
        columns="Absences",
        aggfunc="count",
        fill_value=0
    )

    fig, ax = plt.subplots()

    sns.heatmap(heat, annot=True, cmap="YlGnBu", ax=ax)

    st.pyplot(fig)

    st.divider()

    csv = df.to_csv(index=False)

    st.download_button(
        "Export Records (CSV)",
        data=csv,
        file_name="student_records.csv",
        mime="text/csv"
    )


# ================= MAIN =================
def main():

    with st.sidebar:

        st.title("System Menu")
        st.write(f"Logged in as **{st.session_state.username}**")

        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

    st.title("🎓 Student Performance System")

    prediction_form()

    if st.session_state.role == "admin":
        admin_dashboard()


# ================= RUN =================
if not st.session_state.logged_in:
    login_page()
else:
    main()