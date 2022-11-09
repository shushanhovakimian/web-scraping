# web-scraping

# Descrption
In this project financial data will be scraped from "Yahoo Finance". The aim of this project
is to scrap data from Yahoo Finance, store data in DB and then make 
visualizations.


### About

In the folder 'etl' data gathering part is implemented.

- etl.py - the file includes the scripts for accessing BigQuery datasets, preprocessing data, building, training and saving the 
price prediction model with neural networks
- init_database.py - the file is created for executing the script.py
- web-scraping.py - the script includes connection with Rest API and prediction with a random dataset (here data_test_n.csv can be used)
- helpers.py - the file includes intermediate functions which are used in script.py

In the file 'app' visualizations are created and user entering the company name and range can see
a line chart with that specific features.

Dockerfile is created in order to make the app containerized.

## Start


To start the application  run:
```
docker build -t sentium:latest -f Dockerfile
docker run -p3000:5000 sentium:latest
```
The application will be available with this address: `localhost:3000`

The pretrained model is already available on the directory model/ , but you
can re-execute the tool by running:

```
docker build -t training:latest -f Dockerfile_training
docker run training
```
The model will be created in directory model/

## Endpoint

The predict endpoint is accessible with this path: `/predict`