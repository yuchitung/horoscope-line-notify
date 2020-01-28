from flask import Flask
from flask import render_template
from flask import jsonify
from flask import request
from google.cloud import firestore
from google.cloud.exceptions import NotFound
import requests
import json

app = Flask(__name__,instance_relative_config=True)
app.config['JSON_AS_ASCII'] = False
app.config.from_pyfile('config.py') 
global luck_collection

@app.route('/',methods=['GET'])
def index():
    if request.args.get('subscribe'):
        horoscope = request.args.get('subscribe')
        config = {'ClientId': app.config['CLIENT_ID'] , 'CallbackURL': app.config['CALLBACK_URL'] +'?subscribe=' + horoscope}
        return render_template("subscribe.html", config = config)
    else:
        return 'Please provide your zodiac sign'
        
@app.route('/callback',methods=['GET'])
def callback():
    horoscope= request.args.get('subscribe')
    code = request.args.get('code')
    if horoscope and code:
        response = requests.post('https://notify-bot.line.me/oauth/token',
                    data = {
                        'grant_type':'authorization_code',
                        'code':code,
                        'redirect_uri': app.config['CALLBACK_URL'] + '?subscribe='+ horoscope,
                        'client_id': app.config['CLIENT_ID'],
                        'client_secret': app.config['CLIENT_SECRET'],
                    })

        response = response.json()
        if response['access_token']:
            token= response['access_token']
            account = 'service_account.json'
            #db = firestore.Client('Good-luck') // for gcp env 
            db= firestore.Client.from_service_account_json(account)
            dict = {
                    'aries':'牡羊',
                    'taurus':'金牛',
                    'gemini':'雙子',
                    'cancer':'巨蟹',
                    'leo':'獅子',
                    'virgo':'處女',
                    'libra':'天秤',
                    'scorpio':'天蠍',
                    'sagittarius':'射手',
                    'capricorn':'摩羯',
                    'aquarius':'水平',
                    'pisces':'雙魚', 
            }
            doc_ref = db.collection(u'notify').document(dict[horoscope])
            doc_ref.set({
                token: token
            })
        return 'Success'
    else:
        return "No subscribe topic or authorization code does not exist"

@app.route('/daily-notify',methods=['GET'])
def daily_notify():
    global luck_collection
    response = requests.get(app.config['HOROSCOPE_API_URL'])
    luck_collection=json.loads(response.text)
    try:
        account = 'service_account.json'
        db = firestore.Client.from_service_account_json(account)
        docs = db.collection(u'notify').get()
        for doc in docs:
            horoscope = doc.id
            tokens = doc.to_dict()
            if tokens: 
                for token in tokens: 
                    push(token,get_todays_luck(horoscope+'座'))
         
        return 'Success'   
    except google.cloud.exceptions.NotFound:
        print(u'No such document!')

def get_todays_luck(horoscope):
    print(horoscope)
    luck = luck_collection[horoscope]
    todays_luck='今日短評：'+luck['TODAY_WORD']+'\n' \
                    +'幸運色：'+ luck['LUCKY_COLOR']+'\n\n' \
                    + luck['STAR_ENTIRETY']+ luck['DESC_ENTIRETY']+'\n\n' \
                    + luck['STAR_LOVE'] + luck['DESC_LOVE']+'\n\n' \
                    + luck['STAR_MONEY'] + luck['DESC_MONEY'] +'\n\n'\
                    + luck['STAR_WORK'] + luck['DESC_WORK'] +'\n\n'\
                    + 'Reference - 紫微科技網'
    return todays_luck  

def push(token,message):
    requests.post('https://notify-api.line.me/api/notify',
                    headers={'Authorization': 'Bearer ' + token},
                    data = {
                        'message':message
                    })
if __name__ == "__main__":
    app.run()

