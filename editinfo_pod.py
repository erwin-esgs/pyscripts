import pandas as pd
import requests
import time
import os
from dotenv import load_dotenv

def main():
    df = pd.read_excel('Bundar.xlsx', sheet_name='Detection Kit Unit Mapping',converters={'Code': lambda x: f'{x:04}' , 'IMEI': lambda x: f'{x:04}' })
    df = df.dropna(subset=["Simcard Number"])
    df["Simcard Number"] = df["Simcard Number"].str.slice(start=0, stop=19)
    
    for index, row in df.iterrows():
        if(index >= 3908 and index <= 3968):
            print(str(index)+"========================================================================")
            headers={'x-access-token': os.getenv('X_ACCESS_TOKEN')}
            
            name = row["Code"]+'_'+row["IMEI"]
            URL = 'https://api.podiotsuite.com/v3/assets/'+row["Simcard Number"]
            r = requests.put('https://api.podiotsuite.com/v3/assets/'+row["Simcard Number"] , headers=headers, data={"name": name,"accountId": "364547dc-73dc-51a0-b9ee-8e7ea8a20733"}).json()
            print(r)
            time.sleep(0.1)
            URL = URL+'/groupname'
            groupname = row["Allocation"]
            if(groupname == "DKI Jakarta"):
                groupname = "DKI"
            r = requests.put('https://api.podiotsuite.com/v3/assets/'+row["Simcard Number"]+"/groupname" , headers=headers, data={"groupname": groupname,"accountId": "364547dc-73dc-51a0-b9ee-8e7ea8a20733"}).json()
            print(r)
            print("========================================================================")
            time.sleep(0.1)

    # <Code>_<IMEI>
if __name__ == "__main__":
    load_dotenv()
    main()