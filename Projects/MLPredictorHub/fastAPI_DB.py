
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import date, datetime
import psycopg2
import joblib
import pandas as pd

# Create a connection to the PostgreSQL database
conn = psycopg2.connect(
    host="localhost",
    database="diabetes",
    user="postgres",
    password="root"
)
cursor = conn.cursor()

# Create a FastAPI instance
app = FastAPI()

# Create a Pydantic model to represent the input data for the prediction

class DiabetesData(BaseModel):
    Pregnancies: int
    Glucose: int
    BloodPressure: int
    SkinThickness: int
    Insulin: int
    BMI: float
    DiabetesPedigreeFunction: float
    Age: int

# Define a function to insert a new prediction record into the database
def insert_prediction(prediction_date, pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, pedigree_function, age, prediction_result, prediction_source):
    sql = """
        INSERT INTO predictions (prediction_date, pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, pedigree_function, age, prediction_result, prediction_source)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(sql, (prediction_date, pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, pedigree_function, age, prediction_result, prediction_source))
    conn.commit()

# Placeholder function for making predictions
def make_predictions(my_features: DiabetesData):

    print("in predictions")
    scaler = joblib.load("scaler.joblib")
    model = joblib.load("model.joblib")

        # Convert the input features to a DataFrame
    df = pd.DataFrame([my_features.dict()])

        # Perform data scaling with feature names
    feature_names = df.columns
    data_scaled = scaler.transform(df)
    df_scaled = pd.DataFrame(data_scaled, columns=feature_names)

        # Make predictions
    prediction_result = model.predict(df_scaled)

    out = int(prediction_result[0])
    print(out,
          'OUTPUT')

    return out

    #return 42

# Define a FastAPI endpoint to load data from a CSV file and make predictions
@app.post("/predict-from-csv")
async def predict_from_csv(data: DiabetesData):
    try:
        # Decode the file content
        print("in API")
        prediction_result = make_predictions(data)


        prediction_date = datetime.now()
        pregnancies = data.Pregnancies
        glucose = data.Glucose
        blood_pressure = data.BloodPressure
        skin_thickness = data.SkinThickness
        insulin = data.Insulin
        bmi = data.BMI
        pedigree_function = data.DiabetesPedigreeFunction
        age = data.Age
        prediction_source = 'prediction job'

        insert_prediction(prediction_date, pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, pedigree_function, age, prediction_result, prediction_source)

        return {"predictions": prediction_result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Define a FastAPI endpoint to handle the prediction request
@app.post("/predict")
async def predict(data: DiabetesData):
    # Make prediction using input data
    # Store prediction result and used features in the database
    try:
        # Make prediction using input data
        # In this example, the prediction result is just the sum of all input features

        prediction_result = make_predictions(data)
        print(prediction_result)

        # Store prediction result and used features in the database
        prediction_date = datetime.now()
        pregnancies = data.Pregnancies
        glucose = data.Glucose
        blood_pressure = data.BloodPressure
        skin_thickness = data.SkinThickness
        insulin = data.Insulin
        bmi = data.BMI
        pedigree_function = data.DiabetesPedigreeFunction
        age = data.Age
        prediction_source = 'webapp'

        insert_prediction(prediction_date, pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, pedigree_function, age, prediction_result, prediction_source)

        return {"prediction": prediction_result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Define a function to retrieve past predictions from the database
def get_past_predictions(start_date, end_date, prediction_source):
    sql = """
        SELECT prediction_date, pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, pedigree_function, age, prediction_result
        FROM predictions
        WHERE prediction_date BETWEEN %s AND %s
        AND prediction_source = %s
    """
    sql_all = """
        SELECT prediction_date, pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, pedigree_function, age, prediction_result
        FROM predictions
        WHERE prediction_date BETWEEN %s AND %s
    """
    if prediction_source == 'all':
        cursor.execute(sql_all, (start_date, end_date))
    else:
        cursor.execute(sql, (start_date, end_date, prediction_source))
    rows = cursor.fetchall()
    past_predictions =[
        {
            "prediction_date": row[0].strftime("%Y-%m-%d %H:%M:%S"),
            "pregnancies": row[1],
            "glucose": row[2],
            "blood_pressure": row[3],
            "skin_thickness": row[4],
            "insulin": row[5],
            "bmi": row[6],
            "pedigree_function": row[7],
            "age": row[8],
            "prediction": row[9]
            } for row in rows
    ]
    return past_predictions


# Define a FastAPI endpoint to retrieve past predictions from the database
@app.get("/past-predictions")
async def past_predictions(start_date: date, end_date: date, prediction_source: str = 'all'):
    # Retrieve past predictions from the database and return them as a JSON response
    try:
        past_predictions = get_past_predictions(start_date, end_date, prediction_source)
        return past_predictions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
