import firebase_admin
from firebase_admin import credentials, firestore
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

import requests
from bs4 import BeautifulSoup
url = "https://movies.yahoo.com.tw/theater_list.html"
Data = requests.get(url)
Data.encoding = "utf-8"
sp = BeautifulSoup(Data.text, "html.parser")
result=sp.select(".theater_content li")
#info = ""
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
#print(info)