from flask import Flask, render_template, url_for, redirect, request
import requests
import sys
from argparse import ArgumentParser
from flask import Flask, request, abort
from asyncio import futures
from datetime import datetime as date
from requests.exceptions import HTTPError
import time
import base64
import json
from email.mime import image
from requests_toolbelt.multipart.encoder import MultipartEncoder

import re,random
import datetime
import urllib.request
from wordpress_xmlrpc import WordPressPage
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost ,EditPost
from wordpress_xmlrpc.methods.media import UploadFile
from wordpress_xmlrpc.methods.users import GetUserInfo
from wordpress_xmlrpc import Client, WordPressPost , WordPressComment
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media, posts  ,comments
from wordpress_xmlrpc import WordPressTerm
from wordpress_xmlrpc.methods import taxonomies
#import mimetypes
#from fetch import Fetch
from googletrans import Translator
from bs4 import BeautifulSoup


now = datetime.datetime.now()
user = "admin"
password = "Takumi@2533"
url = "https://avfreex24.com/wp-json/wp/v2"
data_string = user + ':' + password
token = base64.b64encode(data_string.encode())
headers = {'Authorization': 'Basic ' + token.decode('utf-8')}

from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem

class UserAgents:
    def __init__(self):
        pass

    def get_user_agent(self, driver):
        return driver.execute_script("return navigator.userAgent")

    def change_user_agent(self, driver):
        driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent":"python 3.10", "platform":"Windows"})

    def random_user_agent(self):
        software_names = [SoftwareName.CHROME.value]
        operating_systems = [OperatingSystem.WINDOWS.value]
        user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)
        user_agent = user_agent_rotator.get_random_user_agent()
        return user_agent

useragents = UserAgents()
user_agent = useragents.random_user_agent()
app = Flask(__name__)
app.config["DEBUG"] = True

class POSTWP:
    def xmjsup(vod_id, namefile, urlFileimg):
        from urllib import request
        wp_url = "https://javhubpremium.com/changyedfilm.php"
        wp_username = "admin"
        wp_password = "Takumi@2533"
        client = Client(wp_url, wp_username, wp_password)
        nameImg = str(vod_id)+"-"+namefile.replace(" ", "")[0:25]
        print(nameImg)
        header = {
            "User-Agent": user_agent,
            "Referer": "https://google.com/"
        }
        try:
            req = request.Request(urlFileimg, headers=header)
            data = request.urlopen(req).read()
            with open('temp/'+nameImg+'.jpg', 'wb') as f:
                f.write(data)
                f.flush()
                f.close()
            print("download imgVID finished %s " % ('temp/'+nameImg+'.jpg'))
            #nameImg = str(vod_id)+"-"+namefile.replace(" ", "")[0:25]
            filename = './temp/'+nameImg+'.jpg'
            data = {
                'name': nameImg+'.jpg',
                'type': 'image/jpg',  # mimetype
            }

            # read the binary file and let the XMLRPC library encode it into base64
            with open(filename, 'rb') as img:
                data['bits'] = xmlrpc_client.Binary(img.read())
            response = client.call(media.UploadFile(data))
            attachment_id = response['id']
            print(attachment_id)
            return attachment_id
        except Exception as e:
            print(str(e))

    def VIDEOPOST(vod_id,vod_title,type_name,AVmessage,vod_pic,vpath,pub):
        #ggtext = genTEXT()
        description = '<h2>javhubpremium นำเสนอ คลิปหลุดเอเชีย <b style="color:#FF69B4">'+ vod_title+'</b></h2><p>'+AVmessage+'</p>\n'
        meta_title = vod_title + " " + "หนังAV มีรหัส" + " " + type_name
        ppid = str(vod_id)
        #IDPOSTim = upImgVID("หนังAV",ppid,vod_pic)
        IDPOSTim = POSTWP.xmjsup("หนังAV มีรหัส",ppid, vod_pic)
        #vid_post = '[fvplayer src="'+vpath+'" ]'
        print(vod_title,"OK")
        POSTWP.mainPostVIDEO(vod_id,description,meta_title,vod_title,IDPOSTim,vpath,pub)

    def mainPostVIDEO(vod_id,description,meta_title,vod_title,IDPOSTim,vpath,pub):
        wp_url = "https://javhubpremium.com/changyedfilm.php"
        wp_username = "admin"
        wp_password = "Takumi@2533"
    
        wp = Client(wp_url, wp_username, wp_password)
        post = WordPressPost()
        post.slug = vod_title[:21] +"-"+str(vod_id)
        post.title = vod_title[:40]
        post.content = meta_title +'<br/>'+ description
        post.post_status = pub
        post.thumbnail = IDPOSTim
        post.Large = IDPOSTim
        post.excerpt = meta_title
        muviquality = ["AVHD", "HDAV", "คลิปAV", "คลิปAVหลุด", "หลุดAV", "เสียงAV", "เขี่ยหีAV", "AVเซ็กซี่","นักแสดงAV",
                       "AVเบ็ดน้ำแตก", "AVเย็ดมัน", "คลิปหลุดเอเชีย","แอบถ่ายเอเชีย","AVเย็ดสด","หนังAVเต็มเรื่อง", "AVเล่นเสียว", "AVแตกปาก", "AVแตกใน", "โชว์นมAV", "AVโดนรุม", "AVน้อง", "AVโอนลี่แฟน"]
        post.terms_names = {
            'post_tag': [random.choice(muviquality), random.choice(muviquality)],
            'category': [random.choice(muviquality)],
        }
        post.custom_fields = []
        post.custom_fields.append({
            'key': 'vm_video_url',
            'value': vpath,
        })
        wp.call(NewPost(post))

@app.route("/")
def show_landing_page():

    return render_template("error404.html")

@app.route("/callback", methods=['POST'])
def callback():
    #body = request.get_data()
    body = json.loads(request.get_data(as_text=True))
   
    #app.logger.info("Request body: " + body)
    vod_pic = body["imageZ"]
    vpath = body["m3u8"]
    vod_title = body["title"]
    type_name = body["cat"]
    AVmessage = body["AVmessage"]
    vod_id = body["vod_ID"]
    pub = body["pub"]
    try:
        print(body["imageZ"])
        POSTWP.VIDEOPOST(vod_id,vod_title,type_name,AVmessage,vod_pic.replace("http://", "https://"),vpath.replace("http://", "https://"),pub)
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 
    except:
        abort(400)

@app.route("/search", methods=['POST'])
def form_submit():
    user_query = request.form['search_query']  # matches name attribute of query string input (HTML)
    redirect_url = url_for('.search_imdb', query_string=user_query)  # match search_imdb function name (Python flask)
    return redirect(redirect_url)


@app.route("/search/<query_string>", methods=['GET'])
def search_imdb(query_string):
    API_KEY = '2a51d78da56f66254cc2e2a5acf1f712'
    search_movies_url = f"https://yed.moviefreex24.com/javmovie"
    movie_metadata_url = f"https://mgzyz1.com/api.php/provide/vod/?ac=detail&ids="

    try:
        search_movies_response = requests.get(search_movies_url)
        movie = search_movies_response.json()['results'][0]
        #print(movie)
        movie_info_response = requests.get(movie_metadata_url + movie['id'])
        print(movie_info_response.json())
        return render_template(
            "search-result.html", 
            movie=movie,
            movie_info=movie_info_response.json()
            
        )
        
    except:
        return render_template("error404.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5500")
