import streamlit as st
from datetime import datetime
import requests
import pandas as pd
import plotly.express as px

API_URL = "http://localhost:8000"

def update_and_plot():
    workout_date =st.date_input("Enter Date", datetime(2024, 8, 1), label_visibility="collapsed")
    categories = ['bicep_curl', 'shoulder_press', 'bench_press']
    # Insert a placeholder option
    categories_with_placeholder = ["Select a Workout"] + categories
    # Streamlit selectbox with no default selection
    workout_name = st.selectbox(label="Workout_Name", options=categories_with_placeholder, index=0,
                                label_visibility="collapsed")
    # Ensure a valid selection is made before proceeding
    if workout_name == "Select a Workout":
        st.warning("Please select a workout.")
    else:
        st.success(f"You selected: {workout_name}")
    response = requests.get(f"{API_URL}/workout/{workout_name}")
    if response.status_code == 200:
        existing_workout = response.json()
        st.write("Workout Retrieved")
    else:
        st.error("Failed to retrieve workout")
        existing_workout = []
    with st.form(key="workout-form"):
        col1, col2 = st.columns(2)
        with col1:
            st.text('Max Weight')
        with col2:
            st.text('Repetitions')
        max_weight = col1.number_input(label="Max Weight")
        repetitions = col2.number_input(label = "Repetitions")
        submit_button = st.form_submit_button(label="Submit")
        if submit_button:
            response_return = requests.post(f"{API_URL}/workout/{workout_date}", json={"workout_name":workout_name,"max_weight": max_weight, "repetitions": repetitions})
            if response.status_code == 200:
                st.success("Workout updated successfully!")
            else:
                st.error("Failed to update workout.")
    if st.button("Get Past Info"):
        data = {
            "workout_date" :list(existing_workout.keys()),
            "max_weight": [existing_workout[date]["max_weight"] for date in existing_workout],
            }
        df = pd.DataFrame(data)

        # Convert "workout_date" column to datetime

        # Convert "workout_date" column to datetime
        df["workout_date"] = pd.to_datetime(df["workout_date"])

        # Sort by date
        df_sorted = df.sort_values("workout_date")
        print(df_sorted)

        # Check if we have only one workout entry
        if len(df_sorted) == 1:
            single_date = df_sorted["workout_date"].iloc[0]
            df_sorted = pd.concat([
                pd.DataFrame({"workout_date": [single_date - pd.Timedelta(days=1)], "max_weight": [None]}),
                df_sorted,
                pd.DataFrame({"workout_date": [single_date + pd.Timedelta(days=1)], "max_weight": [None]})
            ], ignore_index=True)

        # Create the Plotly Line Chart
        fig = px.line(df_sorted, x="workout_date", y="max_weight", title="Max Weight Progress")

        fig.update_layout(
            xaxis_title="Workout Date",
            yaxis_title="Max Weight (kg)",
            xaxis=dict(
                tickformat="%Y-%m-%d",  # Ensure only date is shown
                tickmode="linear",  # Show all dates without skipping
            )
        )

        # Display in Streamlit
        st.plotly_chart(fig)