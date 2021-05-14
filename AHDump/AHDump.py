import json
import requests
import datetime
from CRS import Config
import pandas as pd

def build_slug_dict(file_name='RealmList.json'):

    realm_json = open(file_name, encoding="utf8")
    realm_data = json.load(realm_json)
    realm_slug_dict = {}

    for x in range(len(realm_data['results'])):
        for y in range(len(realm_data['results'][x]['data']['realms'])):
            slug = realm_data['results'][x]['data']['realms'][y]['slug']
            id = realm_data['results'][x]['data']['id']
            realm_slug_dict[slug] = id
            
    return realm_data, realm_slug_dict

def validate_realm_slug(realm_slug_dict):
    
    while True:
        realm_slug = str(input('Input realm name:')).lower()
        if realm_slug not in realm_slug_dict.keys(): 
            print("Invalid realm name, please try again")
            continue
        else:
            return realm_slug

def get_access_token(c_id, c_secret, region = 'us'):
    
    data = {'grant_type': 'client_credentials'}
    response = requests.post('https://%s.battle.net/oauth/token' % region, data = data, auth = (c_id, c_secret))
    return response.json()

def fetch_auctions(realm_api, token):
    
    search = realm_api + token
    response = requests.get(search)
    return response.json()["auctions"]

def format_data(realm_slug, realm_id):
    
    cfg = Config()
    cid = cfg.token_client_id
    sec = cfg.token_secret
    realm_api = 'https://us.api.blizzard.com/data/wow/connected-realm/' + str(realm_id) + '/auctions?namespace=dynamic-us&locale=en_US&access_token='

    token_response = get_access_token(cid, sec)
    token = token_response['access_token']
    server_auction_data = fetch_auctions(realm_api, token)

    auction_dump_df = pd.DataFrame(server_auction_data)
    auction_dump_df = auction_dump_df.rename(columns={"id": "auction_id",})
    auction_dump_df = pd.concat([auction_dump_df.drop(['item'], axis=1), auction_dump_df['item'].apply(pd.Series).filter(items=['id'])], axis=1)
    auction_dump_df = auction_dump_df.rename(columns={"id": "item_id",})

    auction_dump_df['cost'] = (auction_dump_df['unit_price'].fillna(0) + auction_dump_df['buyout'].fillna(0)).astype(str)
    auction_dump_df['price_gold']=auction_dump_df['cost'].astype(str).str[:-6]
    auction_dump_df['price_silver']=auction_dump_df['cost'].astype(str).str[-6:-4]
    auction_dump_df['price_copper']=auction_dump_df['cost'].astype(str).str[-4:-2]

    filename = (str(realm_slug) + '_AHDump_' + str(datetime.date.today()) + '.csv')
    auction_dump_df.to_csv(filename, index=False)
        
def main():
    
    #Load JSON and build slug/id pair dictionary
    (realm_data, realm_slug_dict) = build_slug_dict()
    
    #Check user input against dictionary until valid realm slug is provided
    realm_slug = validate_realm_slug(realm_slug_dict)
    
    #Return realm id matching valid input for Blizzard API call
    realm_id = realm_slug_dict[realm_slug]
    
    #Retrieves auction data, formats with pd and exports to .csv
    format_data(realm_slug,realm_id)
    
if __name__ == "__main__":
    main()
