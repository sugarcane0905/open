import requests
from bs4 import BeautifulSoup

import firebase_admin
from firebase_admin import credentials, firestore
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/")
def index():
    homepage = "<h1>全台電影院查詢</h1>"
    homepage += "<br><a href=/theater>電影院查詢</a><br>"
    return homepage                   

@app.route("/theater")
def theater():
    url = "https://movies.yahoo.com.tw/theater_list.html"
    Data = requests.get(url)
    Data.encoding = "utf-8"
    sp = BeautifulSoup(Data.text, "html.parser")
    result=sp.select(".theater_content li")
    for item in result:
        if item.find(class_="name") != None:
            title = item.find(class_="name").text
            #theater_id = item.find(class_="name").find("a").get("href").replace("/","").replace("theater", "")
            hyperlink = item.find(class_="name").find("a").get("href")
            adds = item.find(class_="adds").text
            tel = item.find(class_="tel").text
            #info += title + "\n" + hyperlink+ "\n" + adds + "\n"+ tel + "\n" + "\n\n"
            #info += title + "\n"

            doc = {
                "title": title,
                "hyperlink": hyperlink,
                "adds": adds,
                "tel": tel,
            }
            doc_ref = db.collection("全台電影院").document(title)
            doc_ref.set(doc)
    return "資料已更新"         

@app.route("/search", methods=["POST","GET"])
def input():
    if request.method == "POST":
        MovieTitle = request.form["MovieTitle"]
        info = ""
        collection_ref = db.collection("全台電影院")
        for doc in docs:
            if MovieTitle in doc.to_dict()["title"]:
                info += "電影院名稱：" + doc.to_dict()["title"] + "<br>"
                info += "該電影院上映電影連結：" + doc.to_dict()["hyperlink"] + "<br>"
                info += "地址：" + doc.to_dict()["adds"] + " <br>"
                info += "電話：" + doc.to_dict()["tel"] + "<br><br>"
            return info
        else:
            return render_template("input.html")          

if __name__ == "__main__":
    app.run()