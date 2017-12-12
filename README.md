# ClimateAnalysis
Climate Analysis using SQLAlchemy

Files Used:
1) fetch.py - load the data into 2 CSV files in the Resources/data folder
2) data_engineering.ipynb - reads the CSV files, cleans them, and stores them in clean CSV files in Resources/data folder
3) database_engineering.ipynb - reads the clean CSV files, creates and loads sqlite tables with the data
4) climate_analysis.ipynb - reads the sqlite database, performs analysis on the data, and creates charts
5) output charts: daily_normals_hawaii.png, precip_in_hawaii.png, tobs_histogram_hawaii.png, TripAvgTemp.png
6) app.py - Flask program to provide analysis on the Hawaii climate data
