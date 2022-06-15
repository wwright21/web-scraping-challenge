from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo

# importing our scrape_phone script
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/phone_app"
mongo = PyMongo(app)
db = mongo.db

@app.route("/")
def index():
    # find one document from our mongo db and return it.
    mars_data = db.mars_db.find_one()
    # pass that listing to render_template
    return render_template("index.html", scraped_data = mars_data)

# set our path to /scrape
@app.route("/scrape")
def scrape():
    # create a database called "mars_db"
    mars_db = db.mars_db

    # call the scrape function in our scrape_phone file. This will scrape and save to mongo.
    scraped_data = scrape_mars.scrape()

    # update our mars_db with the data that is being scraped.
    mars_db.update_many({}, {"$set": scraped_data} , upsert=True)

    # return a message to our page so we know it was successful.
    return redirect("/", code=302)


# boilerplate
if __name__ == "__main__":
    app.run(debug=True)
