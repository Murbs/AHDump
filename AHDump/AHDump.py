import json
import requests
import datetime
from CRS import CRS
import pandas as pd

def main():
    
    realm_json = open('RealmList.json', encoding="utf8")
    realm_data = json.load(realm_json)
    realm_slug = []

    for x in range(len(realm_data['results'])):
        for y in range(len(realm_data['results'][x]['data']['realms'])):
                realm_slug.append(realm_data['results'][x]['data']['realms'][y]['slug'])

    def get_realm_id(realm_name):

        for x in range(len(realm_data['results'])):
            for y in range(len(realm_data['results'][x]['data']['realms'])):
                if realm_data['results'][x]['data']['realms'][y]['slug'] == realm_name:
                    realm_id = str(realm_data['results'][x]['data']['id'])

                    init = CRS()
                    cid = init.cfg.token_client_id
                    sec = init.cfg.token_secret
                    realm_api = 'https://us.api.blizzard.com/data/wow/connected-realm/' + realm_id + '/auctions?namespace=dynamic-us&locale=en_US&access_token='

                    def get_access_token(c_id, c_secret, region = 'us'):
                        data = {'grant_type': 'client_credentials'}
                        response = requests.post('https://%s.battle.net/oauth/token' % region, data=data, auth=(c_id, c_secret))
                        return response.json()

                    def server_us(token):
                        search =  realm_api + token
                        response = requests.get(search)
                        return response.json()["auctions"]

                    response = get_access_token(cid, sec)
                    token = response['access_token']
                    server_auction_data = server_us(token)

                    auction_dump_df = pd.DataFrame(server_auction_data)
                    auction_dump_df = auction_dump_df.rename(columns={"id": "auction_id",})
                    auction_dump_df = pd.concat([auction_dump_df.drop(['item'], axis=1), auction_dump_df['item'].apply(pd.Series).filter(items=['id'])], axis=1)
                    auction_dump_df = auction_dump_df.rename(columns={"id": "item_id",})

                    auction_dump_df['cost'] = (auction_dump_df['unit_price'].fillna(0) + auction_dump_df['buyout'].fillna(0)).astype(str)
                    auction_dump_df['price_gold']=auction_dump_df['cost'].astype(str).str[:-6]
                    auction_dump_df['price_silver']=auction_dump_df['cost'].astype(str).str[-6:-4]
                    auction_dump_df['price_copper']=auction_dump_df['cost'].astype(str).str[-4:-2]

                    filename = (str(realm_name) + '_AHDump_' + str(datetime.date.today()) + '.csv')
                    auction_dump_df.to_csv(filename, index=False)

    def input_realm_id():
            user_input = str(input('Input Realm name:')).lower()
            if user_input in realm_slug:
                get_realm_id(user_input)
            else:
                print('Invalid realm name, try again')

    input_realm_id()

if __name__ == "__main__":
    main()
