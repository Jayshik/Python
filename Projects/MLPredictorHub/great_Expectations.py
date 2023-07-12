import great_expectations as ge
import shutil
import pandas as pd
from datetime import datetime
import psycopg2
import os

csv_directory = './folder_A/'
# Get a list of all files in the directory
file_list = os.listdir(csv_directory)
# Read the CSV file into a Great Expectations dataset
print(file_list)
with open("file_number.txt", "r") as file:
    # Read the entire file content as a single string
    f_number = file.read()
filename="file_" + f_number + ".csv"

if filename in file_list:
    print(filename)
    path = "./data/" + filename
    dataset = ge.read_csv(path)
    master = dataset.copy()
    next_file = int(f_number) + 1
    with open("file_number.txt", "w") as file:
        # Write new content to the file
        file.write(str(next_file))


    # Define the expectations
    dataset.expect_column_to_exist('Pregnancies')
    dataset.expect_column_to_exist('Glucose')
    dataset.expect_column_to_exist('BloodPressure')
    dataset.expect_column_to_exist('SkinThickness')
    dataset.expect_column_to_exist('Insulin')
    dataset.expect_column_to_exist('BMI')
    dataset.expect_column_to_exist('DiabetesPedigreeFunction')
    dataset.expect_column_to_exist('Age')

    dataset.expect_column_values_to_not_be_null('Age')
    dataset.expect_column_values_to_not_be_null('Glucose')
    dataset.expect_column_values_to_not_be_null('BloodPressure')
    dataset.expect_column_values_to_not_be_null('SkinThickness')
    dataset.expect_column_values_to_not_be_null('Insulin')
    dataset.expect_column_values_to_not_be_null('BMI')
    dataset.expect_column_values_to_not_be_null('DiabetesPedigreeFunction')
    dataset.expect_column_values_to_not_be_null('density')

    dataset.expect_column_values_to_be_of_type("Age", "int64")
    dataset.expect_column_values_to_be_between("Glucose", min_value=70, max_value=150)
    dataset.expect_column_values_to_be_between("Age", min_value=21, max_value=110)
    dataset.expect_column_values_to_be_between("BloodPressure", min_value=40, max_value=120)

    # Validate the data
    results = dataset.validate()

    invalid_path = "folder_B/invalid_data_"+filename
    valid_path = "folder_C/valid_data_"+filename
    # Check if any data quality issues were found
    if results["statistics"]["successful_expectations"] == results["statistics"]["evaluated_expectations"]:
        # No data quality issues found, move the file to folder C
        shutil.move(path, valid_path)
    else:
        # Get the validation statistics
        statistics = results["statistics"]

        # Get the details of the data quality issues
        data_quality_issues = results["results"]

        invalid_rows_data = pd.DataFrame(columns=dataset.columns)

        # Connect to the PostgreSQL database
        connection = psycopg2.connect(
            host="localhost",
            database="diabetes",
            user="postgres",
            password="root"
        )

        # Create a cursor object to execute SQL queries
        cursor = connection.cursor()

        # Iterate over each data quality issue
        for expectation_result in data_quality_issues:
            if not expectation_result["success"]:
                # Create a dataframe for invalid rows of the current expectation type

                column = expectation_result["expectation_config"]["kwargs"]["column"]
                partial_unexpected_list = expectation_result["result"]["partial_unexpected_list"]
                invalid_rows_data = invalid_rows_data.append(dataset[dataset[column].isin(partial_unexpected_list)])

                # Save error information to PostgreSQL database
                timestamp = datetime.now()
                error_type = expectation_result["expectation_config"]["expectation_type"]
                errored_values = ", ".join(map(str, partial_unexpected_list))

                # Define the SQL query to insert the error information into the table
                insert_query = "INSERT INTO error_table (filename, timestamp, error_type, errored_values) " \
                               "VALUES (%s, %s, %s, %s)"

                # Execute the SQL query with the error information
                cursor.execute(insert_query, (filename, timestamp, error_type, errored_values))



        if invalid_rows_data.shape[0] == dataset.shape[0]:
                    # All rows have data problems, move the file to folder B
            shutil.move(path, invalid_path)
        else:
                    # Reset the indices of the dataset
            dataset.reset_index(drop=True, inplace=True)

                    # Drop the invalid rows from the main dataset
            dataset.drop(invalid_rows_data.index, inplace=True)

                    # Move the invalid rows to folder B
            invalid_rows_data.to_csv(invalid_path, index=False)

                    # Move the valid rows to folder C
            dataset.to_csv(valid_path, index=False)

        # Commit the transaction to save the changes
        connection.commit()

        # Close the cursor and database connection
        cursor.close()
        connection.close()
else:
    print("no new file")