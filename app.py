from flask import Flask
from flask_restful import Api, Resource, reqparse
from rake_nltk import Rake
from bs4 import BeautifulSoup
import requests
import html5lib


app = Flask(__name__)
api = Api(app)

keyword_data_args = reqparse.RequestParser()
keyword_data_args.add_argument("keyword", type=str, help="the keyword is required to send")

class keyword_stats(Resource):
    def get(self,keyword):

        page_url = "https://fivlytics.com/keyword-analytics"
        sess = requests.Session()
        r = sess.get(page_url)
        soup = BeautifulSoup(r.content,'html5lib')
        csrf = soup.find('meta', attrs={'name': 'csrf-token'})['content']
        header = {
            'x-csrf-token': csrf
        }
        url = page_url
        keyword = keyword
        data = {
            'keyword': keyword
        }
        r = sess.post(url, data=data, headers=header)
        return r.json()


class gig_description(Resource):
    def get(self,desc):

        gig_data = desc
        result = Rake()
        result.extract_keywords_from_text(gig_data)
        desc_keyword = result.get_ranked_phrases()[0:10]

        return desc_keyword

        
class keyword_rank(Resource):
    def get(self,keyword,profile):

        page_url = "https://fivlytics.com/find-fiverr-gig-rank"
        sess = requests.Session()
        r = sess.get(page_url)
        soup = BeautifulSoup(r.content,'html5lib')
        csrf = soup.find('meta', attrs={'name': 'csrf-token'})['content']
        header = {
        'x-csrf-token': csrf
        }
        url = page_url
        username = profile
        kws = keyword
        data = {
            'keyword': kws,
            'username': username
            }
        r = sess.post(url, data=data, headers=header)
        return r.json()


api.add_resource(keyword_stats,"/fiverrseotoolkeyword/<string:keyword>")
api.add_resource(gig_description,"/fiverrseotoolgigdesc/<string:desc>")
api.add_resource(keyword_rank,"/fiverrseotoolkeyword_rank/<string:keyword>/<string:profile>")

if __name__ == '__main__':
    app.run(debug=True, port=8080)
