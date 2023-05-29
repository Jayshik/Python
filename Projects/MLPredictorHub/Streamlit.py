import requests
import streamlit as st
import pandas as pd

# FastAPI endpoint URLs
PREDICT_URL = 'http://localhost:8000/predict'
PAST_PREDICTIONS_URL = 'http://localhost:8000/past-predictions'
# Prediction page
def prediction_page():
    st.header("Prediction Page")
    # Display form for single sample prediction
    st.subheader("Single Sample Prediction")
    # Input fields for features
    pregnancies = st.number_input("Pregnancies", min_value=0, step=1)
    glucose = st.number_input("Glucose", min_value=0)
    blood_pressure = st.number_input("Blood Pressure", min_value=0)
    skin_thickness = st.number_input("Skin Thickness", min_value=0)
    insulin = st.number_input("Insulin", min_value=0)
    bmi = st.number_input("BMI", min_value=0)
    pedigree_function = st.number_input("Diabetes Pedigree Function", min_value=0.0)
    age = st.number_input("Age", min_value=0, step=1)
    # Predict button
    if st.button("Predict"):
        #TO-DO
        # Make API request to model service with feature values
        # Get prediction from model service
        # Display prediction result
        data = {
            'pregnancies': pregnancies,
            'glucose': glucose,
            'blood_pressure': blood_pressure,
            'skin_thickness': skin_thickness,
            'insulin': insulin,
            'bmi': bmi,
            'pedigree_function': pedigree_function,
            'age': age
        }
        # Make API request to model service with feature values
        response = requests.post(PREDICT_URL, json=data)
        if response.status_code == 200:
            result = response.json()
            table_data = {**data, **result}
            table_data = {k: [v] for k, v in table_data.items()}
            # Display prediction result
            st.write("Prediction:")
            st.table(table_data)
        else:
            st.write("Error making prediction")

    # Upload CSV file for multiple predictions
    st.subheader("Multiple Sample Prediction")
    file = st.file_uploader("Upload CSV file", type=["csv"])

    if st.button("Predict Multiple"):


        if file is not None:
        # Read CSV file and extract feature values
            df = pd.read_csv(file)
            data = df.to_dict('records')

        # Make API request to model service with feature values and display prediction results
            predictions = []
            for row in data:
                response = requests.post(PREDICT_URL, json=row)
                if response.status_code == 200:
                    result = response.json()
                    row['Prediction'] = result['prediction']
                    predictions.append(row)
                else:
                    st.write("Error making prediction")

            # Display prediction results
            if predictions:
                st.write("Predictions:")
                st.table(predictions)
            else:
                st.write("No predictions to display.")

# Past predictions display webpage
def past_predictions_page():
    st.header("Past Predictions Display Webpage")
    # Date selection component
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")
    # Prediction source drop-down list
    prediction_source = st.selectbox("Prediction Source", ["webapp", "scheduled predictions", "all"])
    if st.button("Retrieve Predictions"):
        print("Retrive predction")
        # Make API request to model service with date range and prediction source
        # Get past predictions from model service
        # Display past predictions
        params = {
            'start_date': start_date,
            'end_date': end_date,
            'prediction_source': prediction_source
        }
        response = requests.get(PAST_PREDICTIONS_URL, params=params)
        if response.status_code == 200:
            # Get past predictions from model service
            past_predictions = response.json()
            # Display past predictions
            if past_predictions:
                st.write("Prediction date:")
                past_predictions_df = pd.DataFrame(past_predictions)
                st.table(past_predictions_df)
            else:
                st.write("No past predictions found.")

        else:
            st.write("Error retrieving past predictions")

# Main Streamlit app
# Main Streamlit app
def main():
    st.set_page_config(layout="wide")
    st.title("Diabetes Prediction Web App")
    # Navigation menu
    page = st.sidebar.radio("Select Page", ["Prediction", "Past Predictions"])
    # Display selected page
    if page == "Prediction":
        prediction_page()
    elif page == "Past Predictions":
        past_predictions_page()


if __name__ == "__main__":
    main()
