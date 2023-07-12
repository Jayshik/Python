# dsa_ninja_turtles
Use Case:
      In this project we focuses on developing a machine learning model to predict the likelihood of women above age of 21 having diabetes. The dataset used for this project is sourced from Kaggle, which contains various features related to health indicators and diagnostic measurements. The goal is to create a simple and accurate prediction model for diabetes without spending extensive time on the model development step.The ML-Powered Application will enable users to assess their risk of having diabetes by providing their health indicators and receiving predictions instantly
Dataset:
source: kaggle (https://www.kaggle.com/datasets/nancyalaswad90/review)
Architecture: 1.User Interface: A web application developed using Streamlit, providing prediction and past prediction functionalities.  
              2.Model Service (API): An API developed using FastAPI to serve the machine learning model, make predictions, and store predictions in the database.
              3.ML model: Using decision tree for prediction 
              3.Database: An SQL database (PostgreSQL) used to store past predictions, along with the features used for prediction.
              4.Prediction Job: A scheduled job implemented using Airflow that periodically makes predictions on the ingested data.
              5.Great expection:  Data validation (blood pressure, glucose, age)
              6.Monitoring Dashboard: A Grafana dashboard to monitor data quality problems and model prediction issues.
                                      Created two dashboard i) XY- plot for Age vs Peregnincies
                                                            	        ii) Bar guage
               7.Workflow: User-end :      i)Users can access the web application to make on-demand predictions by filling in the features for a single sample or                                                     uploading a CSV file for multiple predictions.
                                           ii)The web application calls the model service API to retrieve predictions, which are then displayed to the user along with                                                the corresponding features used for the prediction.
    
                          Prediction-end:   i)New data files are ingested and validated for quality using tools like Great Expectations.
                                            ii)Clean data files are stored, while files with data quality issues are flagged and saved in the database.
                                            iii)The prediction job, running every 5 minutes, checks for new clean data files.
                                            iv)The prediction job reads the clean data files and makes API calls to the model service for predictions.
                                            v)Predictions are stored in the database, enabling access to the latest predictions and historical prediction data.
Installation:
            1.Install the dependencies: pip install -r requirements.txt
            2.Application setup: streamlit run app.py
            3.Airflow: pip install apache-airflow
             Initialize the Airflow Database: airflow db init
             Start the Airflow Web Server and Scheduler: airflow webserver --port 8080
                                                         airflow scheduler
             4.Great Expectations: pip install great_expectations
             5.Visualization tool Grafana: Downloaded from offical website  
                                            echo "deb https://packages.grafana.com/oss/deb stable main" | sudo tee -a /etc/apt/sources.list.d/grafana.list
                                            sudo apt-get install -y adduser libfontconfig1
                                            wget https://dl.grafana.com/enterprise/release/grafana-enterprise_10.0.0_amd64.deb
                                            sudo dpkg -i grafana-enterprise_10.0.0_amd64.deb
                                            sudo yum install -y https://dl.grafana.com/enterprise/release/grafana-enterprise-10.0.0-1.x86_64.rpm
                                            wget https://dl.grafana.com/enterprise/release/grafana-enterprise-10.0.0-1.x86_64.rpm
                                            sudo rpm -Uvh grafana-enterprise-10.0.0-1.x86_64.rpm
 Usage:
      Prediction Webpage: Use this (streamlit - Diabetic predictor)webpage to make predictions.
      i)Fill in the features for a single sample prediction using the provided form.
      ii)In order to make multiple predictions,need to upload a CSV file containing the inference data (without labels).
      and then Clicking the "Predict" button to make on-demand predictions, which will be displayed in the webapp along with the used features.
      
      Past Predictions Webpage: Use this webpage to view past predictions.   
      i) Select the start and end dates for the predictions.
      ii) Choose the prediction source from the drop-down list (webapp, scheduled predictions, or all).
         View the past predictions along with the corresponding used features.
       Visualzation: Using grafana Data Quality Monitoring, Model Performance Monitoring , Data Drift Detection , Dashboard Customization and Alerting and                                  Notifications
         
 API Endpoints:
The model service (API) exposes the following endpoints:
    i)POST /predict: Make model predictions by providing the necessary input features.
    ii)GET /past-predictions: Retrieve past predictions along with the used features.


             
      
      
      
     



