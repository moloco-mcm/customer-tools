# Copyright 2023 Moloco, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import csv
import json
import requests
from datetime import datetime

PLATFORM_NAME = "" # Platform name. e.g. MOLOCO
PLATFORM_ID = "" # Platform ID e.g. MOLOCO_TEST
BASE_URL = "https://{NAME}-mgmt.rmp-api.moloco.com/rmp/mgmt/v1/platforms/{ID}".format(NAME=PLATFORM_NAME, ID=PLATFORM_ID)

# Provide PLATFORM_OWNER credential to get token and call management APIs
EMAIL = ""
PWD = ""

# Put where you want to store the file
FILE_DIR = "./"

# Get token based on the credential
def CreateToken(base_url, email, pw):
    url = base_url + "/tokens"
    payload = {
        "auth_type": "CREDENTIAL",
        "credential_type_payload": {
            "email": email,
            "password": pw
        }
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    json_formatted = json.loads(response.text)
    return (json_formatted['token'])

# Get the list of ad accounts
def ListAdAccount(base_url, token):
    url = base_url + "/ad-accounts"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + token
        }
    response = requests.get(url, headers=headers) # Get list of ad accounts
    return(response.text)

# Get the list of campaigns and campaigned items from certain ad account
def ListCampaigns(base_url, ad_account_id, token):
    url = base_url + "/ad-accounts/" + ad_account_id + "/campaigns?without_catalog_item_ids=false"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + token
        }
    response = requests.get(url, headers=headers) # Get list of campaigns
    return(response.text)


def main():

    # Open a csv file to write campaigned items
    file = FILE_DIR + "/" + datetime.now().strftime('%Y-%m-%dT%H:%M') + "_itemlist.csv"
    csvfile = open(file, 'w', newline='')
    write = csv.writer(csvfile)
    # Column schema
    write.writerow(['ad_account_id','campaign_id','campaigned_item_ids'])

    campaignedItemList = list()
    
    # Gets token based on the credential
    token = CreateToken(BASE_URL, EMAIL, PWD)
    # Gets all the ad account in the platform
    adAccountList = json.loads(ListAdAccount(BASE_URL, token))["ad_accounts"]
    
    for adaccount in adAccountList: 
        # Gets list of campaigns of the ad account
        campaigns = json.loads(ListCampaigns(BASE_URL, adaccount['id'], token))["campaigns"]
        for campaign in campaigns:
            # Gets list of campaigned items
            campaignedItems = campaign["catalog_item_ids"]
            # Checks that list is not empty and the campaign is enabled(active)
            if (len(campaignedItems) != 0 and campaign["enabling_state"] == "ENABLED"):
                print("For ad account:{AD_ACCOUNT_ID} campaign:{CM_ID}, there are {COUNT} items in the campaign".format(AD_ACCOUNT_ID=adaccount['id'], CM_ID=campaign['id'], COUNT=len(campaignedItems)))
                campaignedItemList += campaignedItems
                for item_ids in campaignedItems:
                    write.writerow([adaccount['id'],campaign['id'], item_ids])
        
    print("Total {COUNT} campaigned items found".format(COUNT=len(campaignedItemList)))
    

if __name__ == '__main__':
    main()