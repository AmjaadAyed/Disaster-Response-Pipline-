Disaster Response Pipeline 
In this project, I'll apply Data Engineering skills besides the Data Science to analyze disaster data from Figure Eight to build a model for an API that classifies disaster messages.
To run this project:
1.	Run process_data.py to export data to a database file
2.	Run train.py to export the machine learning model to a pickle file
3.	Run run.py to get a web application
The data are tweets and texts that were sent during real world disasters and can be labeled into at least one of 36 categories.
1.	Create ETL of data from CSV files and upload cleansed data to a database
2.	Write a machine-learning algorithm to analyze messages and optimize the model to correctly classify labels for that text
3.	Create a web application that can show 2 graphs of overviews of the messages, as well as an input bar that could read a message and correctly classify what label it would belong to.
Running Instructions
Run process_data.py
1.	Save the data folder in the current working directory and process_data.py in the data folder.
2.	From the current working directory, run the following command: python data/process_data.py data/disaster_messages.csv data/disaster_categories.csv data/disaster_response.db
Run train_classifier.py
1.	In the current working directory, create a folder called 'models' and save train_classifier.py in this.
2.	From the current working directory, run the following command: python models/train_classifier.py data/disaster_response.db models/classifier.pkl
Run the web app
1.	Save the app folder in the current working directory.
2.	Run the following command in the app directory: python run.py
3.	Go to http://0.0.0.0:3001/

disaster_categories.csv
CSV contains all messages’ categories almost 36 categories 
disaster_messages.csv
CSV contains disaster messages
Disaster_response.db
The Database file which is the result of the process_data.py 
process_data.py 
The ETL part is the extract - transform - load process. The provided data were processed and cleaned using the Pandas and Numpy libraries, also some labelling was applied on the data since that I was categorical data, the duplication was handled, after that, the data had been saved to the disaster_response.db SQLite database file.
Train_classifier.py
On this file, the following were applied, loads data from the SQLite disaster_response.db database, Splits the dataset into training and test sets, Builds a text processing and machine learning pipeline, Trains and tunes a model using GridSearchCV, Outputs results on the test set, and exports the final model as a pickle file.
run.py
The web app, run.py The main page includes visualizations using data from the SQLite database.


