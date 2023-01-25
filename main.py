from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route("/")
def index():
    url = "https://football-prediction-api.p.rapidapi.com/api/v2/predictions"
    querystring = {"market":"classic","iso_date":"2018-12-01","federation":"UEFA"}
    headers = {
        "X-RapidAPI-Key": "9c457fc3eemshb8f49e7ab2b6c2dp120d23jsn0e64203539a3",
        "X-RapidAPI-Host": "football-prediction-api.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.json()['data']
    return render_template('index.html', predictions=data)

if __name__ == '__main__':
    app.run()
