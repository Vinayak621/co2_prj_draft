from flask import Flask,render_template,url_for,request,jsonify
from flask_cors import cross_origin
import pandas as pd
import numpy as np
import datetime
import joblib
import folium
from geopy.geocoders import Nominatim
from sklearn.preprocessing import StandardScaler
from decimal import Decimal
import mysql.connector
from flask import Flask, render_template, request, jsonify
import ee
from datetime import date

app = Flask(__name__, template_folder="green")
model = joblib.load(open("./models/DecisionTreeClassifier.pkl", "rb"))
scaler = joblib.load(open("./models/scaler.joblib", "rb"))
print("Model Loaded")

@app.route("/",methods=['GET'])
@cross_origin()
def home():
	return render_template("index.html")

@app.route("/predict",methods=['GET', 'POST'])
@cross_origin()
def predict():
	if request.method == "POST":
		cereal_yield = float(request.form['cereal_yield'])
		
		fdi_perc_gdp = float(request.form['fdi_perc_gdp'])
		
		en_per_gdp = float(request.form['en_per_gdp'])
		
		en_per_cap = float(request.form['en_per_cap'])
		
		co2_ttl = float(request.form['co2_ttl'])
		
		# co2_per_cap = float(request.form['co2_per_cap'])
		
		co2_per_gdp = float(request.form['co2_per_gdp'])
		
		pop_urb_aggl_perc= float(request.form['pop_urb_aggl_perc'])
		
		prot_area_perc = float(request.form['prot_area_perc'])
		
		#gdp = float(request.form['gdp'])
		
		gni_per_cap = float(request.form['gni_per_cap'])
		
		under_5_mort_rate = float(request.form['under_5_mort_rate'])
		
		pop_growth_perc = float(request.form['pop_growth_perc'])
		
		#pop = float(request.form['pop'])
		
		#urb_pop_growth_perc = float(request.form['urb_pop_growth_perc'])
		
		#urb_pop = float(request.form['urb_pop'])





		input_lst = [[cereal_yield,
            fdi_perc_gdp,
            en_per_gdp,
            en_per_cap,
            co2_ttl,
            
            co2_per_gdp,
            pop_urb_aggl_perc,
            prot_area_perc,
            
            gni_per_cap,
            under_5_mort_rate,
            pop_growth_perc,
           
            ]]
  
		# scaler = StandardScaler().fit(np.array(input_lst).reshape(1,-1))
		# input_data_norm = scaler.transform(np.array(input_lst).reshape(1,-1))
		
		inp_data_norm=scaler.transform(input_lst)
		
  
  		
		pred = model.predict(inp_data_norm)
		output = pred
  		
		if output == 'green':
			return render_template("green1.html")
		else:
			return render_template("red1.html")
	return render_template("predictor.html")


@app.route("/green_tax_credit")
def green_tax_cal():
    return render_template("index_p.html")

@app.route('/calculate', methods=['GET', 'POST'])
def index():
    # Connect to the MySQL database
    cnx = mysql.connector.connect(user='root', password='Mysql#001', host='localhost', database='offset')
    cursor = cnx.cursor()

    if request.method == 'POST':
        name = request.form['name']
        model = request.form['model']
        miles = request.form['miles']

        # Execute the query to retrieve the co2_emissions and fuel_consumption_comb_mpg for the given make and model
        query = "SELECT co2_emissions, fuel_consumption_comb_mpg FROM cars_11 WHERE make = %s AND model = %s"
        cursor.execute(query, (name, model))
        data = cursor.fetchone()

        if data:
            co2_emissions = Decimal(str(data[0]))
            mpg = Decimal(str(data[1]))
            miles_year = int(miles) * 52
            co2_emissions_lb = co2_emissions *  Decimal('0.00220462')
            carbon_emissions = round((co2_emissions_lb * miles_year) / mpg, 2)
            trees = round(carbon_emissions / 48)
            return render_template('result2.html', make=name, model=model,carbon_emissions=carbon_emissions, miles=miles, trees=trees)
        else:
            # Show an error message if no data is found for the given make and model
            error_message = f"No data found for make '{name}' and model '{model}'"
            return render_template('index2.html', error_message=error_message)

    # Retrieve the available makes from the MySQL database and pass them to the template
    cursor.execute("SELECT DISTINCT make FROM cars_11 ORDER BY make")
    makes = [row[0] for row in cursor.fetchall()]

    # Close the cursor and the database connection
    cursor.close()
    cnx.close()

    return render_template('index2.html', makes=makes)

@app.route('/models', methods=['GET'])
def models():
    # Connect to the MySQL database
    cnx = mysql.connector.connect(user='root', password='Mysql#001', host='localhost', database='offset')
    cursor = cnx.cursor()

    make = request.args.get('make')

    # Execute the query to retrieve the available models for the given make
    query = "SELECT DISTINCT model FROM cars_11 WHERE make = %s ORDER BY model"
    cursor.execute(query, (make,))
    models = [row[0] for row in cursor.fetchall()]

    # Close the cursor and the database connection
    cursor.close()
    cnx.close()

    return jsonify(models)

ee.Initialize()
def add_ndvi(image):
    ndvi=image.normalizedDifference(['B4','B3']).rename('NDVI')
    return image.addBands(ndvi)
def add_ee_layer(self,ee_image_object,vis_params,name):
    map_id_dict=ee.Image(ee_image_object).getMapId(vis_params)
    folium.raster_layers.TileLayer(
        tiles=map_id_dict['tile_fetcher'].url_format,
        attr='Map Data &copy; <a href="https://earthengine.google.com/">Google Earth Engine</a>',
        name=name,
        overlay=True,
        control=True
    ).add_to(self)
folium.Map.add_ee_layer=add_ee_layer


landsat7=ee.ImageCollection("LANDSAT/LE07/C02/T1_TOA")
@app.route("/mappage")
def homepage():
    return render_template('map.html')
@app.route("/map",methods=['POST'])
def map():
    long=float(request.form['longitude'])
    lat=float(request.form['latitude'])
    year=int(request.form['year'])
    my_map=folium.Map((lat,long),zoom_start=12)
    start_date=date(year,1,1)
    end_date=date(year,12,31)
    point=ee.Geometry.Point(long,lat)
    temporalFiltered=landsat7.filterDate(str(start_date),str(end_date))
    spacialFiltered=temporalFiltered.filterBounds(point)
    ndvi_images=spacialFiltered.map(add_ndvi)
    ndvi_vis_arams={'bands':'NDVI','min':-1,'max':1,'palette':['red','yellow','green']}
    maskImage=ee.Image("UMD/hansen/global_forest_change_2021_v1_9")
    datamask=maskImage.select("datamask")
    mask=datamask.eq(1)
    my_map.add_ee_layer(ndvi_images.qualityMosaic('NDVI').updateMask(mask),ndvi_vis_arams,'land cover')
    folium.Marker([lat,long]).add_to(my_map)
    folium.Circle([lat,long],radius=1000).add_to(my_map)
    return my_map.get_root().render()


if __name__=='__main__':
	app.run(debug=True)