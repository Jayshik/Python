*** SmartPredict: End-to-End ML Prediction System with Monitoring and Dashboard ***


Project requirement:

A user interface where the user can make on-demand predictions and view past predictions (streamlit)
An API for exposing the ML model (FastAPI) and saving the predictions in the database
An SQL database for saving data (predictions along with the used features, ...) (PostgreSQL, SQLAlchemy)
A prediction job to make scheduled predictions each n mins (Airflow)
An ingestion job to ingest and validate the data quality (great expectations, TensorFlow Data Validation)
A monitoring dashboard to monitor data quality problems of the ingested data and the drift of training and serving data (Grafana)
These components will interact as shown in this architecture:

Project architecture

User interface
Should be composed of 2 webpages: one for the user to make predictions and another one to display past predictions

Prediction page
Should contain:

A form to fill in the features for a single sample prediction.
An upload button to upload a csv file for making multiple predictions: the file should contain the inference data in the correct format without labels 
A predict button to make on-demand predictions by calling the model API service
Note: when predictions are returned by the model service (API), they need to be displayed in the webapp along with the features used for making the prediction

Past predictions display webpage
Should contain:

A date selection component to select the start and end date of the predictions
A prediction source drop list to select the source of the predictions to retrieve
webapp: to show only predictions made using the webapp
scheduled predictions: to show predictions made using the prediction job
all: to show predictions made from the webapp or the prediction job
Model service (API)
An API for:

serving the model (making predictions)
saving the model predictions and used features in the database
returning past predictions and used features to the webapp
It should contain the following endpoints:

predict: for making model predictions from the the webapp or the prediction job
past-predictions: to get the model past predictions along with the used features
Database
It will be used by multiple components:

The model service to save the model predictions and query them
The data ingestion job to save data quality problems
The dashboard to display data quality problems and data drift
Prediction job
This job will be used to make scheduled predictions. It will executed each n minutes.

It should be composed of 2 tasks:

check_for_new data: in this task, you will check in the folder where the data is ingested if there are any new files (one or multiple). If so read it and pass it to the next task, otherwise mark the dag run status as skipped(Dag run status)
make_predictions: in this task, you will make API call to the model service to make predictions on the data read by the previous task.
Data ingestion job
This job will be responsible for:

Ingesting new data each n minutes
Validating data quality of the ingested data
Raising alerts if any data quality problem
Monitoring dashboard
This dashboard will be used to monitor:

data quality problems detected by the data ingestion job
data drift between training and serving data (example: during training, users average age was 45 and in serving, it is 60)
It will be querying the data from the same database where the predictions are saved