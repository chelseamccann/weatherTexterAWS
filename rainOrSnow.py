from flask import Flask, render_template, request
import requests
#import json
from text_updates import client
#import boto3

app = Flask(__name__)

@app.route('/precipitation', methods=['POST'])
def precipitation():
    zipcode = request.form['zip']
    r = requests.get('https://api.openweathermap.org/data/2.5/weather?zip='+zipcode+',us&appid=APIKEY')
        ##json_object = r.text
    json_object = r.json()
    precip = (json_object['weather'][0]['description'])
    kelv_temp = float(json_object['main']['temp'])
    fahr_temp = int((kelv_temp - 273.15) * 1.8 + 32)

#only send text if its raining or snowing
    if ('rain' in precip) or ('snow' in precip):
        client.publish(
            PhoneNumber="0123456789", 
            Message="The forecast is currently {} and {} degrees.".format(precip, fahr_temp)
        )

#render to web page regardless of precipitation
    return render_template('precipitation.html', precip=precip, temp=fahr_temp)


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True,port=8080)
