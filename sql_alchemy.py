import numpy as np
import pandas as pd
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

# Save reference to the table
Measurement=Base.classes.measurement
Station=Base.classes.station

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
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
     # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all dates and precipitation"""
    # Query all dates and precipitations
    results = session.query(Measurement.date, Measurement.prcp).\
        order_by(Measurement.date).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    list_prcp = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        list_prcp.append(prcp_dict)

    return jsonify(list_prcp)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    # Query all stations
    results = session.query(Station.station, Station.name).all()

    session.close()

    # Create a dictionary from the row data and append to list of stations
    list_station = []
    for station, name in results:
        station_dict = {}
        station_dict["station"] = station
        station_dict["name"] = name
        list_station.append(station_dict)

    return jsonify(list_station)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #Calculate the date one year ago from the last date
    year_ago=dt.date(2017, 8, 23) - dt.timedelta(days=365)


    """Return a list of dates and tobs"""
    # Query all dates and tobs of most active station last year
    results = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.station=='USC00519281').\
    filter(Measurement.date>=year_ago).\
    order_by(Measurement.tobs).all()

    session.close()

    # Create a dictionary from the row data and append to list of tobs
    list_tobs = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        list_tobs.append(tobs_dict)

    return jsonify(list_tobs)


@app.route("/api/v1.0/<start>")
def start():
    # Create our session (link) from Python to the DB
    session = Session(engine)


    """Return a list of temp min,avg and max"""
    # calculate/query `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date

    results = session.query(Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
        filter(Measurement.date>=start).\
        group_by(Measurement.date).all()

    session.close()

    # Create a dictionary from the row data and append to list of tobs
    list_start = []
    for date, min, max, avg in results:
        start_dict = {}
        start_dict["date"] = date
        start_dict["TMIN"] = min
        start_dict["TMAX"] = max
        start_dict["TAVG"] = avg
        list_start.append(start_dict)

    return jsonify(list_start)



@app.route("/api/v1.0/<start>/<end>")
def end():

    # Create our session (link) from Python to the DB
    session = Session(engine)


    """Return a list of temp min,avg and max"""
    # calculate/query `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date

    results = session.query(Measurement.date,func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
        filter(Measurement.date>=start, Measurement.date<=end).\
        group_by(Measurement.date).all()

    session.close()

    # Create a dictionary from the row data and append to list of tobs
    list_end = []
    for date, min, max, avg in results:
        end_dict = {}
        end_dict["date"] = date
        end_dict["TMIN"] = min
        end_dict["TMAX"] = max
        end_dict["TAVG"] = avg
        list_end.append(end_dict)

    return jsonify(list_end)




if __name__ == '__main__':
    app.run(debug=True) 