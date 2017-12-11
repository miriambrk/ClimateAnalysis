import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, and_

from flask import Flask, jsonify

# function to subtract one year from input date
def date_minus_one_year(input_date):
    year_earlier, month, day = input_date.split("-")
    year_earlier = str(int(year_earlier) - 1)
    new_date = year_earlier + '-' + month + '-' + day
    return new_date


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to the measurement and station tables
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)


### Select the latest date in the database and the date 1 year earlier; used in precipitation and temperature queries below
def get_latest_date():
    # first select the latest date in the database
    result = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    latest_date = result[0]

    # change latest_date to 1 year earlier
    year_earlier_date = date_minus_one_year(latest_date)

    return(latest_date, year_earlier_date)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Avalable Routes:<br/>"
        f"/api/v1.0/precipitation - List of Precipitation Observations from the previous year<br/>"

        f"/api/v1.0/stations"
        f"- List of observation stations<br/>"

        f"/api/v1.0/tobs"
        f"- List of Temperature Observations (tobs) for the previous year<br/>"

        f"/api/v1.0/temps/&ltstart&gt/&ltend&gt"
        f"- Min, avg, max temp for start or start-end date range (format yyyy-mm-dd)<br/>"

    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of Precipitation Observations from the previous year"""

    # first select the latest date
    latest_date, new_date = get_latest_date()

    # select date and precip for last 12 months
    results = session.query(Measurement.date, Measurement.prcp). \
        filter(Measurement.date >= new_date). \
        order_by(Measurement.date).all()

    # convert results to dictionary
    prec_dict = {}

    for r in results:
        prec_dict[r.date] = r.prcp

    return jsonify(prec_dict)


@app.route("/api/v1.0/stations")
def stations():
    #Return a list of stations

    results = session.query(Station.name, func.count(Measurement.measurement_id) ).\
    filter(Measurement.station == Station.station ).  \
        group_by(Measurement.station).order_by(func.count(Measurement.measurement_id).desc()).all()

    #create dictionary from results
    station_dict = {}
    for s in results:
        station_dict[s.name] = s[1]

    return jsonify(station_dict)


@app.route("/api/v1.0/tobs")
def tobs():
    #Return a json list of Temperature Observations (tobs) for the previous year
    # first select the latest date
    latest_date, new_date = get_latest_date()

    # select date and tobs for last 12 months
    results = session.query(Measurement.date, Measurement.tobs). \
        filter(Measurement.date >= new_date). \
        order_by(Measurement.date).all()

    # convert results to dictionary
    tobs_dict = {}

    for r in results:
        tobs_dict[r.date] = r.tobs

    return jsonify(tobs_dict)


@app.route("/api/v1.0/temps/<start_date>")
@app.route("/api/v1.0/temps/<start_date>/<end_date>")
def temps(start_date, end_date="XXX"):

    if (end_date == "XXX"):
        #set the end date to the latest date
        end_date, new_date = get_latest_date()

    results = session.query(Measurement.date, Measurement.tobs). \
        filter(and_(Measurement.date >= start_date, Measurement.date <= end_date)).all()
    temps_df = pd.DataFrame(results, columns=["date", "tobs"])

    temps_dict = {}
    temps_dict["min_temp"] = int(temps_df["tobs"].min())
    temps_dict["avg_temp"] = temps_df["tobs"].mean()
    temps_dict["max_temp"] = int(temps_df["tobs"].max())

    print('temps_dict: ')
    print(temps_dict)

    return jsonify(temps_dict)

if __name__ == '__main__':
    app.run()


