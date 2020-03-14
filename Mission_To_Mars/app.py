from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pymongo
import mars_scrape


app = Flask(__name__)

# Use PyMongo to establish Mongo connection
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.mars_db
#mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_data")


# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    #mars_data = mongo.db.mars_data.find_one()
    db_data = db.mars.find_one()
    db_data

    # Return template and data
    return render_template("index.html", mars_data=db_data)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    db_data = mars_scrape.scrape()

    print(db_data)

    # Update the Mongo database using update and upsert=True
    db.mars.update({}, db_data, upsert=True)

    # Redirect back to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)