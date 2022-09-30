from itertools import count
from dotenv import load_dotenv
import json
import pandas as pd
import requests
import time
import os

def main():
    df = pd.read_excel('Bundar.xlsx', sheet_name='Detection Kit Unit Mapping',converters={'Code': lambda x: f'{x:04}' , 'IMEI': lambda x: f'{x:04}' })
    df = df.dropna(subset=["Simcard Number"])
    df["Simcard Number"] = df["Simcard Number"].str.slice(start=0, stop=19)
    area="Jawa Tengah"
    URL = 'https://jateng.kittways.com'
    PATH="/wialon/ajax.html"
    # PATH="/api"
    eid=os.getenv('X_ACCESS_TOKEN')
    list_unit = requests.post(URL+PATH+'?svc=core/search_items&params={"spec":{"itemsType":"avl_unit","propName":"sys_id","propValueMask":"*","sortType":"sys_id","propType":"list"},"force":1,"flags":1,"from":0,"to":0}&sid='+eid).json()
    
    if "items" in list_unit:
        list_unit = list(list_unit["items"])
        # print(list_unit)
        count=0
        for index, row in df.iterrows():
            if(str(row["Code"]).isnumeric()):
                if(int(row["Code"]) >= 2734 and int(row["Code"]) <= 3733 ):
                    if(row["Allocation"] == area ):
                        exist = next((item for item in list_unit if item["nm"] == row["Code"] ), None)
                        count += 1

                        if exist is None:
                            print("==="+str(index+1)+"="+row["Code"]+"=====================================================================")
                            creatorId = 55
                            params = {"creatorId":creatorId,"name":row["Code"],"hwTypeId":"13","dataFlags":1}
                            jsonParams = f'{json.dumps(params)}'
                            ''' '{"creatorId":56,"name":'+row["Code"]+',"hwTypeId":"13","dataFlags":1}' '''
                            
                            
                            r = requests.post(URL+PATH+'?svc=core/create_unit&sid='+eid , data={'params': jsonParams, 'sid' :eid} ).json()
                            time.sleep(0.02)
                            print(r)
                            if "error" in r:
                                if(r["error"] == 6):
                                    continue

                            itemId = str(r["item"]["id"])
                            params = {
                                "params": [
                                    {
                                        "svc": "item/update_profile_field",
                                        "params": {
                                            "itemId": itemId,
                                            "n": "vehicle_class",
                                            "v": "empty_person"
                                        }
                                    },
                                    {
                                        "svc": "item/update_custom_property",
                                        "params": {
                                            "itemId": creatorId,
                                            "name": "used_hw",
                                            "value": "{\"13\":216}"
                                        }
                                    },
                                    {
                                        "svc": "unit/update_device_type",
                                        "params": {
                                            "itemId": itemId,
                                            "deviceTypeId": "13",
                                            "uniqueId": row["IMEI"]
                                        }
                                    },
                                    {
                                        "svc": "unit/update_unique_id2",
                                        "params": {
                                            "itemId": itemId,
                                            "uniqueId2": ""
                                        }
                                    },
                                    {
                                        "svc": "unit/update_access_password",
                                        "params": {
                                            "itemId": itemId,
                                            "accessPassword": ""
                                        }
                                    },
                                    {
                                        "svc": "unit/update_phone",
                                        "params": {
                                            "itemId": itemId,
                                            "phoneNumber": ""
                                        }
                                    },
                                    {
                                        "svc": "unit/update_phone2",
                                        "params": {
                                            "itemId": itemId,
                                            "phoneNumber": ""
                                        }
                                    },
                                    {
                                        "svc": "unit/update_mileage_counter",
                                        "params": {
                                            "itemId": itemId,
                                            "newValue": 0
                                        }
                                    },
                                    {
                                        "svc": "unit/update_eh_counter",
                                        "params": {
                                            "itemId": itemId,
                                            "newValue": 0
                                        }
                                    },
                                    {
                                        "svc": "unit/update_traffic_counter",
                                        "params": {
                                            "itemId": itemId,
                                            "newValue": 0,
                                            "regReset": 0
                                        }
                                    },
                                    {
                                        "svc": "unit/update_calc_flags",
                                        "params": {
                                            "itemId": itemId,
                                            "newValue": 16
                                        }
                                    },
                                    {
                                        "svc": "unit/update_hw_params",
                                        "params": {
                                            "itemId": itemId,
                                            "hwId": "13",
                                            "params_data": {
                                                "reset_all": 1,
                                                "params": [],
                                                "full_data": 0
                                            },
                                            "action": "set"
                                        }
                                    }
                                ],
                                "flags": 0
                            }
                            jsonParams = f'{json.dumps(params)}'
                            r = requests.post(URL+PATH+'?svc=core/batch&sid='+eid , data={"params":jsonParams , "sid":eid} ).json()
                            time.sleep(0.02)
                            print(r)
                            
                        else:
                            list_unit.remove(exist)
                            # print(count , exist)
                            print("exist ", str(index+1) , row["Code"] )

                    else:
                        print( str(index+1)  , row["Allocation"] , " not " , area)


        print(list_unit)
                 

if __name__ == "__main__":
    load_dotenv()
    main()