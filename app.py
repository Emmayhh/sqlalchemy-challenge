import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

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
Measurement = Base.classes.measurement
Station = Base.classes.station


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
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    results = session.query(Measurement.date,Measurement.prcp).all()
    
    session.close()

    # Convert list of tuples into normal list
    
    all_prcps = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict[date] = prcp
        all_prcps.append(prcp_dict)
    

    return jsonify(all_prcps)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    results = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()
    
    session.close()

    # Convert list of tuples into normal list

    station_list = []
    for station, name, latitude, longitude, elevation in results:
        station_dict = {}
        station_dict['station'] = station
        station_dict['name'] = name
        station_dict['latitude'] = latitude
        station_dict['longitude'] = longitude
        station_dict['elevation'] = elevation
        station_list.append(station_dict)

        station_list.append(station_dict)
        
    return jsonify(station_list)



@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    Recent_date = dt.date(2017,8, 23)

    # Calculate the date one year from the last date in data set.
    One_Year = Recent_date - dt.timedelta(days=366)

    # Perform a query to retrieve the data and precipitation scores
    results = session.query(Measurement.date, Measurement.tobs).filter_by(station = "USC00519281").filter(Measurement.date >= One_Year).all()
    
    
    session.close()

    # Convert list of tuples into normal list
    
    Past_12Months = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict[date] = tobs
        Past_12Months.append(tobs_dict) 
   
    return jsonify(Past_12Months)  


@app.route("/api/v1.0/start")
def start():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    
    Temperature_Num = [Measurement.station,
           func.min(Measurement.tobs),
           func.max(Measurement.tobs),
           func.avg(Measurement.tobs)]
    
    Query= session.query(*Temperature_Num).filter_by(Measurement.date > start).all()
    Start_list =[{"TMIN": Query[0][1]},
                 {"TAVG": Query[0][2]},
                 {"TMAX": Query[0][3]}]

    session.close()
    
@app.route("/api/v1.0/start/end")
def end():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    
    Temperature_Num = [Measurement.station,
           func.min(Measurement.tobs),
           func.max(Measurement.tobs),
           func.avg(Measurement.tobs)]
    
    Query= session.query(*Temperature_Num).filter_by(Measurement.date > end).all()
    End_list =[{"TMIN": Query[0][1]},
               {"TAVG": Query[0][2]},
               {"TMAX": Query[0][3]}]

    session.close()


if __name__ == '__main__':
    app.run(debug=True)