import os
import pandas as pd
import requests

# Specify the directory containing the CSV files
csv_directory = './folder_C/'
PREDICT_URL = 'http://localhost:8000/predict-from-csv'
# Get a list of all files in the directory
file_list = os.listdir(csv_directory)
predicted_files = "predicted_file.txt"
with open(predicted_files, "r") as file:
    lines = file.readlines()

new_list = [file for file in file_list if file not in lines]
# Read each CSV file, make predictions, and store the results
for file_name in new_list:
    with open(predicted_files, "a") as file:
        file.write("\n" + file_name)
    if file_name.endswith('.csv'):
        file_path = os.path.join(csv_directory, file_name)

        if file_name is not None:
            # Read CSV file and extract feature values
            df = pd.read_csv(file_path)
            data = df.to_dict('records')

            # Make API request to model service with feature values and display prediction results
            predictions = []
            for row in data:
                response = requests.post(PREDICT_URL, json=row)
                if response.status_code == 200:
                    result = response.json()
                    print(result)

                else:
                    print("Error making prediction")







