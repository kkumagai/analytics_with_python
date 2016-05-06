import random
import json
from time import sleep
from datetime import datetime
from pymongo import MongoClient
# import requests
from bs4 import BeautifulSoup

# words 
# words.next()

class wordlist:
    def __init__(self, user):
        self.client = MongoClient()
        self.collection = self.client["words"][user]
        self.list = self.collection.find({"recent_date": {"$ne": None}}).sort("recent_date", -1).limit(1000)

class words:
    def __init__(self, user):
        self.client = MongoClient()
        self.collection = self.client["words"][user]
        self.user = user
        self.select()

    def select(self, word = None):
        if word:
            self.cursor = self.collection.find({"word": word}).next()
        else:
            index =random.randint(0, self.collection.find({"recent":{"$ne":[1,1,1,1,1]}}).count())
            self.cursor = self.collection.find({"recent":{"$ne":[1,1,1,1,1]}}).skip(
                   index 
                ).next()

        self.word = self.cursor["word"]
        self.meaning = self.cursor["meaning"]

        try:
            self.memo = self.cursor["memo"]
        except:
            self.memo = ""

        self.recent = self.cursor["recent"]
        self.url_image = "https://www.google.co.jp/search?q={}&tbm=isch".format(self.cursor["word"])
        self.url_ejdict = "http://ejje.weblio.jp/content/{}".format(self.cursor["word"])
        self.url_sentence = "http://ejje.weblio.jp/sentence/content/{}".format(self.cursor["word"])
        self.url_thesaurus = "http://www.thesaurus.com/browse/{}".format(self.cursor["word"])
        self.url_eedict = "https://www.vocabulary.com/dictionary/{}".format(self.cursor["word"])
        return self

    def create(self, word, meaning):
        self.collection.insert_one({"word": word, "meaning": meaning, "recent":[]})
        self.select(word)
        return self

    def update(self, word, meaning):
        self.collection.update_one({"word": word}, {"$set":{"meaning": meaning}})
        self.select(word)
        return self


    def completed(self):
        return self.collection.find({"recent":[1,1,1,1,1]}).sort("word")

    def weak(self):
        return " ".join(
            [i["word"] for i in self.collection.find({"recent":[1,1,1,1,1]}).sort("word")]
            )


    def delete(self, word):
        res = self.collection.delete_one({"word":word})
        if res.deleted_count > 0:
            print("Delete {}".format(word))
        else:
            print("単語帳に登録されていません。")
    
    def count(self):
        return self.collection.count()

    def show(self):

        print(self.cursor["word"], flush = True)
        sleep(1.5)
        print("\n" * 4, flush = True)
        print(self.cursor["meaning"], flush = True)
        print("\n", flush = True)
        print("image: {}".format(self.url_image), flush = True)
        print("dict: {}".format(self.url_dict), flush = True)
        print("sentence: {}".format(self.url_sentence), flush = True)

    def add_recent(self, word, result):
        recent = self.collection.find_one({"word":word})["recent"]
        recent.append(result)
        self.collection.update_one({"word":word}, {"$set":{"recent":recent[-5:], "recent_date": datetime.now()}})
        
        recent = self.collection.find_one({"word":word})["recent"]
        return recent    

    def counter(self, word, target):
        try:
            count = self.collection.find_one({"word":word})[target]
        except:
            count = 0
        count += 1
        self.collection.update_one({"word":word}, {"$set": {target: count, target +"_date": datetime.now()}})
        # 日付が更新されない
        return self.collection.find_one({"word":word})

    def add_memo(self, word, memo):
        self.collection.update_one({"word":word}, {"$set": {"memo": memo}})
        # 日付が更新されない
        return self.collection.find_one({"word":word})