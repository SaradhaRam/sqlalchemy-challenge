import numpy as np
import sys
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

print(Base.classes.keys())

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################


# Home Page - List all routes that are available
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

# JSON representation of dictionary Key:Date,Value:prcp


@app.route("/api/v1.0/precipitation")
def precipitation():
    # latest_date = 2017, 8 ,23
    year_ago_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    session = Session(engine)
    # Design a query to retrieve the last 12 months of precipitation data and plot the results
    prcp_last_12months = session.query(Measurement.date, Measurement.prcp).filter(
        Measurement.date.between(year_ago_date, '2017-8-23')).all()

    session.close()
    # Create a dictionary from the row data and append to a list of all_passengers
    # last_year_data = []
    # for date,prcp in prcp_last_12months:
    #     prcp_dict = {}
    #     prcp_dict["date"] = date
    #     prcp_dict["prcp"] = prcp
    #     last_year_data.append(prcp_dict)
    # return jsonify(last_year_data)

    date_precipitation = {date: prcp for date, prcp in prcp_last_12months}
    return jsonify(date_precipitation)

# Return a JSON list of stations from the dataset


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all station names"""
    # Query all station
    all_stations = session.query(Station.station).all()
    session.close()

    # Convert list of tuples into normal list
    station_list = list(np.ravel(all_stations))
    return jsonify(station_list)

# Query the dates and temperature observations of the most active station for the last year of data.


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Find the most active station"""
    # Query all station
    # Find Most active station
    station_desc_order = session.query(Measurement.station, func.count(Measurement.station)).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).all()
    print(f'The most active station is: {station_desc_order[0][0]}')
    # The most active station is 'USC00519281'
    
    # Query the last 12 months of temperature observation data for the most active station
    # latest_date = 2017, 8 ,23
    year_ago_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    station_tobs = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == "USC00519281").\
        filter(Measurement.date.between(year_ago_date, '2017-8-23')).all()
    session.close()
    # Convert list of tuples into normal list
    tobs_list = list(np.ravel(station_tobs))
    
    return jsonify(tobs_list)

# Find min,max and avg temperature observation greater than the given start date
# @app.route("/api/v1.0/<start>")
# def start(start=None):
#     # Create our session (link) from Python to the DB
#     session = Session(engine)

#     """Return a list of all station names"""
#     # Query all station

#     min_tobs = session.query(func.min(Measurement.tobs)).filter(
#         Measurement.station == "USC00519281").scalar()
#     max_tobs = session.query(func.max(Measurement.tobs)).filter(
#         Measurement.station == "USC00519281").scalar()
#     avg_tobs = session.query(func.avg(Measurement.tobs)).filter(
#         Measurement.station == "USC00519281").scalar()

#     session.close()

#     return jsonify(min_tobs, max_tobs, avg_tobs)

# Find min,max and avg temperature observation between the given start and end date


if __name__ == '__main__':
    app.run(debug=True)
