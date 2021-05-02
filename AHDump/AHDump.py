import json
import requests
import datetime
from CRS import CRS
import pandas as pd

def main():
    
    realmJSON = open('RealmList.json', encoding="utf8")
    realm_data = json.load(realmJSON)
    realm_slug = []

    for x in range(len(realm_data['results'])):
        for y in range(len(realm_data['results'][x]['data']['realms'])):
                realm_slug.append(realm_data['results'][x]['data']['realms'][y]['slug'])

    def get_realmID(realm_name):

        for x in range(len(realm_data['results'])):
            for y in range(len(realm_data['results'][x]['data']['realms'])):
                if realm_data['results'][x]['data']['realms'][y]['slug'] == realm_name:
                    realmID = str(realm_data['results'][x]['data']['id'])

                    init = CRS()
                    cid = init.cfg.token_client_id
                    sec = init.cfg.token_secret
                    realmAPI = 'https://us.api.blizzard.com/data/wow/connected-realm/' + realmID + '/auctions?namespace=dynamic-us&locale=en_US&access_token='

                    def get_access_token(c_id, c_secret, region = 'us'):
                        data = {'grant_type': 'client_credentials'}
                        response = requests.post('https://%s.battle.net/oauth/token' % region, data=data, auth=(c_id, c_secret))
                        return response.json()

                    def server_US(token):
                        search =  realmAPI + token
                        response = requests.get(search)
                        return response.json()["auctions"]

                    response = get_access_token(cid, sec)
                    token = response['access_token']
                    server_AHdata = server_US(token)

                    AHdump_df = pd.DataFrame(server_AHdata)
                    AHdump_df = AHdump_df.rename(columns={"id": "auction_id",})
                    AHdump_df = pd.concat([AHdump_df.drop(['item'], axis=1), AHdump_df['item'].apply(pd.Series).filter(items=['id'])], axis=1)
                    AHdump_df = AHdump_df.rename(columns={"id": "item_id",})

                    AHdump_df['cost'] = (AHdump_df['unit_price'].fillna(0) + AHdump_df['buyout'].fillna(0)).astype(str)
                    AHdump_df['price_gold']=AHdump_df['cost'].astype(str).str[:-6]
                    AHdump_df['price_silver']=AHdump_df['cost'].astype(str).str[-6:-4]
                    AHdump_df['price_copper']=AHdump_df['cost'].astype(str).str[-4:-2]

                    filename = (str(realm_name) + '_AHDump_' + str(datetime.date.today()) + '.csv')
                    AHdump_df.to_csv(filename, index=False)

    def input_realmID():
            user_input = str(input('Input Realm name:')).lower()
            if user_input in realm_slug:
                get_realmID(user_input)
            else:
                print('Invalid realm name, try again')

    input_realmID()

if __name__ == "__main__":
    main()