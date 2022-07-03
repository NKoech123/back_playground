import pandas as pd
import gspread
from datetime import datetime


from validateEthAddress import get_clean_ResolvedETHAddress

#assuming  data is an json REST API response with fields :  'userName' and 'userAddress' (just a wallet)
def get_Users_with_invalid_wallets(data):
    list = []
    for row in data:
        address = row['fields']['userAddress'] if 'userAddress' else None
       
        
        #if wallet not found
        if  not address : #fields['wallet'].startswith('0x') and not valid   #fields['wallet'].endswith('.eth')
            list.append((data['fields']['userName'],
                         data['fields']['userAddress'],
                        str(datetime.now())
                          
                        ))   
        
        #wallet exists, let's check if valid. If invalid, let's log it to Gsheets
        else:
            address = data['fields']['userName']
            res = get_clean_ResolvedETHAddress(address)

            if (res == "INVALID_or_UNREGISTERED_ENS.ETH" or
                res == "INVALID_hexadecimal_ADDRESS!!!!"):

                list.append((data['fields']['userName'],
                         data['fields']['userAddress'],
                        str(datetime.now())
                          
                        ))  
                    
    return list

             
api_data = {
       {
            "id": "recw1NwERnW9kfgHU",
            "createdTime": "2022-05-15T19:39:50.000Z",
            "fields": {
                "userName": "0xCryptoStefan",
                "userAdrress": "chumbachumba.eth",
               
            }
        },

       {
            "id": "recw1rerfgHU",
            "createdTime": "2022-05-15T19:38:50.000Z",
            "fields": {
                "userName": "EthereumApeMan",
                "userAdrress": "0x234hj42t524t25t25t25677774905",
               
            }
        }
}

data = get_Users_with_invalid_wallets(api_data)

#create dataframe
df = pd.DataFrame(data, columns =['userName', 'userAddress','GSheet_update_date'])

       
def upload_dataframe_to_gsheet(GSHEET_NAME: str, GSHEET_KEY: str, df) -> None:
   
    gc = gspread.service_account(filename = '/Users/username/Downloads/invalidaddresses-b99df9a4as08.json')
    sh = gc.open_by_key(GSHEET_KEY)
    worksheet = sh.sheet1
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())


'''
Get them from google apis (Gsheets)
MY_GSHEET_NAME=??
MY_GSHEET_KEY = ??
'''
upload_dataframe_to_gsheet(GSHEET_NAME = MY_GSHEET_NAME , 
                           GSHEET_KEY = MY_GSHEET_KEY , 
                           df=df
                        )

'''
python invalidaddresstoGsheets.py
'''