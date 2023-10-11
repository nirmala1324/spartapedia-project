# Handle the server -> server creation and its functions

#Additional Dependency for Deployment
import os
from os.path import join, dirname
from dotenv import load_dotenv

# General Dependency
from http import client
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup

# Read the .env file
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Read credential data about database from .env file
MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME = os.environ.get("DB_NAME")

# ITS HARDCORE CODE
""" client = MongoClient('mongodb+srv://nirmalapusparatna20031107:npr20031107@cluster0.cqhgovi.mongodb.net/')
db = client.dbsparta """
# Turned into this
conn = MongoClient(MONGODB_URI)
db = conn[DB_NAME]

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/movie", methods=["POST"])
def movie_post():
    receive_url = request.form['given_url']
    receive_rate = request.form['given_rate']
    receive_comm = request.form['given_comment']
    
    
    # meta webscraping code
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

    raw_data = requests.get(receive_url, headers=headers)
    processed_data = BeautifulSoup(raw_data.text, 'html.parser')

    og_image = processed_data.select_one('meta[property = "og:image"]')
    og_title = processed_data.select_one('meta[property = "og:title"]')
    og_description = processed_data.select_one('meta[name = "description"]')   

    image = og_image['content']
    title = og_title['content'].split(' (')[0]
    description = og_description['content'].split(': ')[1] 
    
    # add to document for 'movie' collection
    movie_doc = {
        'title': title,
        'img': image,
        'desc': description,
        'rate': receive_rate,
        'comment': receive_comm
    }
    
    db.movies.insert_one(movie_doc)
    
    return jsonify({'msg':'POST request success!'})

@app.route("/movie", methods=["GET"])
def movie_get():
    movie_list = list(db.movies.find({},{'_id':False}))
    return jsonify({'movies':movie_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)