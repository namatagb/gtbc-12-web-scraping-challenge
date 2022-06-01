from flask import Flask, render_template
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/phone_app"
mongo = PyMongo(app)

@app.route("/")
def index():
    mars_dict = mongo.db.listings.find_one()
    return render_template("index.html", mars_dict=mars_dict)

@app.route("/scrape")
def scraper():
    mars_dict = mongo.db.mars_dict_data
    mars_dict_data = scrape_mars.scrape()
    mars_dict.update_one({}, {"$set": mars_dict_data}, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
