import requests
from colorama import Fore
import datetime
from requests.exceptions import JSONDecodeError
import urllib.parse
W = Fore.RESET
C = "\033[38;2;75;0;130m"
L = Fore.LIGHTYELLOW_EX
V = Fore.GREEN
B = Fore.LIGHTBLACK_EX
I = Fore.LIGHTRED_EX

def headers(token):
    return {
        'Accept': '*/*',
        'Accept-Language': 'en-EN,cs;q=0.9,en;q=0.8',
        'Authorization': token,
        'Cookie': '__dcfduid=bcdcc21048ec11eeb28aadb2936bc589; __sdcfduid=bcdcc21148ec11eeb28aadb2936bc58939681dcd50112431f1dc800e50f374628b27f03a40107a46ebf3a05065becb2c; _ga_Q149DFWHT7=GS1.1.1693589213.1.0.1693589414.0.0.0; __stripe_mid=a614d196-bfdf-4093-be94-44b2567c7c312dff1a; _ga_XXP2R74F46=GS1.2.1702481998.1.0.1702481998.0.0.0; _gid=GA1.2.1957939489.1702654470; _ga_YL03HBJY7E=GS1.1.1702654469.11.0.1702654469.0.0.0; _ga=GA1.1.1994256083.1693589213; OptanonConsent=isIABGlobal=false&datestamp=Fri+Dec+15+2023+16%3A34%3A29+GMT%2B0100+(czas+%C5%9Brodkowoeuropejski+standardowy)&version=6.33.0&hosts=&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A0%2CC0003%3A0&AwaitingReconsent=false; __cfruid=7c526e008192466f8ca27de600811cb9f9a9b039-1702664289; _cfuvid=ut98lvE6CAZQkcpuAaMXk7oTUSVGktwTdF16TRtT.EQ-1702664289884-0-604800000; cf_clearance=G65_tgviKwqVw0qNdhw0byG9ATZLTfAEAszCfqd.CMk-1702664599-0-1-3b6189e5.cb55b875.78db4fb0-0.2.1702664599; locale=en',
        'Referer': 'https://discord.com/channels/@me',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.199 Safari/537.36',
        'X-Debug-Options': 'bugReporterEnabled',
        'X-Discord-Locale': 'en',
        'X-Discord-Timezone': 'Europe/London',
        'X-Super-Properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6InBsLVBMIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzExOS4wLjYwNDUuMTk5IFNhZmFyaS81MzcuMzYiLCJicm93c2VyX3ZlcnNpb24iOiIxMTkuMC42MDQ1LjE5OSIsIm9zX3ZlcnNpb24iOiIxMCIsInJlZmVycmVyIjoiIiwicmVmZXJyaW5nX2RvbWFpbiI6IiIsInJlZmVycmVyX2N1cnJlbnQiOiIiLCJyZWZlcnJpbmdfZG9tYWluX2N1cnJlbnQiOiIiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfYnVpbGRfbnVtYmVyIjoyNTQ4ODgsImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGx9'
}

def get_messages(token, channel_id):
    try:
        resp = requests.get(f"https://discord.com/api/v9/channels/{channel_id}/messages?limit=50", headers=headers(token))
        resp.raise_for_status()
        data = resp.json()
        return data
    except requests.exceptions.HTTPError as e:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"{W}{current_time}{C}||{I}Failed to get messages {e.response.status_code}")
        return []
    except JSONDecodeError:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"{W}{current_time}{C}||{I}Failed to decode JSON response")
        return []
         
def react(token, channel_id, message_id, index):
    try:
        messages = get_messages(token, channel_id)
        for message in messages:
            if message["id"] == message_id:
                try:
                    reaction = message["reactions"][index]
                except IndexError:
                    return {"status": 404, "response": "No reactions on message :()"}
                    
                emoji = reaction["emoji"]["id"]
                if reaction["emoji"]["id"] == None:    
                    emoji = urllib.parse.quote(reaction["emoji"]["name"])
                resp = requests.put(f"https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}/reactions/{emoji}/@me?location=Message&type=0", headers=headers(token))
                if resp.status_code == 204:
                    current_time = datetime.datetime.now().strftime("%H:%M:%S")
                    print(f"{W}{current_time}{C}||{V}Reacted {resp.status_code}")
                else:
                    current_time = datetime.datetime.now().strftime("%H:%M:%S")
                    print(f"{W}{current_time}{C}||{I}Failed to react {resp.status_code}")
    except TypeError as e:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"{W}{current_time}{C}||{I}Error occurred:", e)