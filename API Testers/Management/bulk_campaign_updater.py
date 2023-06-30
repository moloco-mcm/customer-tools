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

PLATFORM_NAME = "" # Platform name. e.g. MOLOCO
PLATFORM_ID = "" # Platform ID e.g. MOLOCO_TEST
BASE_URL = "https://{NAME}-mgmt.rmp-api.moloco.com/rmp/mgmt/v1/platforms/{ID}".format(NAME=PLATFORM_NAME, ID=PLATFORM_ID)

TIMEZONE = "Asia/Seoul"
CURRENCY = "KRW"

# Provide csv file path which contains bulk campaign create data. For reference, please check the sample_campaign_list.csv
FILE_PATH = ""

# Provide PLATFORM_OWNER credential to get token and call management APIs
EMAIL = ""
PWD = ""


def ParseFile():
    return csv.DictReader(open(FILE_PATH, 'r'), delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL, skipinitialspace=True)

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

# Read current campaign data
def ReadCampaign(base_url, ad_account_id, campaign_id, token):
    url = base_url + "/ad-accounts/" + ad_account_id + "/campaigns/" + campaign_id
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + token
    }
    response = requests.get(url, headers=headers)
    return (response.text)

# Update single campaign
def UpdateCampaign(base_url, ad_account_id, campaign_id, payload, token):
    url = base_url + "/ad-accounts/" + ad_account_id + "/campaigns/" + campaign_id
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": "Bearer " + token
    }
    campaign_payload = payload
    response = requests.put(url, json=campaign_payload, headers=headers)
    json_formatted = json.loads(response.text)
    return (json_formatted)

# Update campaigns based on the data provided at the file
def BulkUpdateCampaignsFromFile(token):
    for row_num, data in enumerate(ParseFile()):
        # Reads campaign settings from the file
        ad_account_id = data['ad_account_id'].replace('"', '').strip()
        campaign_id = data['campaign_id'].replace('"', '').strip()
        campaign_title = data['campaign_title'].replace('"', '').strip()
        schedule_start = data['campaign_schedule_start'].replace('"', '').strip()
        schedule_end = data['campaign_schedule_end'].replace('"', '').strip()
        goal_setting = data['goal_setting'].replace('"', '').strip()
        daily_budget = data['daily_budget_max'].replace('"', '').strip()
        items = [item.replace('[', '').replace(']', '').replace(',', '') for item in data['items'].replace('"', '').strip().split()]
        enabling_state = data['enabling_state'].replace('"', '').strip()

        # Reads current campaign info based on the campaign_id given from the file
        loaded_payload = json.loads(ReadCampaign(BASE_URL, ad_account_id, campaign_id, token))
        
        # Overwrites campaign settings 
        loaded_payload['campaign']['title'] = campaign_title
        loaded_payload['campaign']['schedule']['start'] = schedule_start
        loaded_payload['campaign']['schedule']['end'] = schedule_end
        loaded_payload['campaign']['daily_budget']['currency'] = CURRENCY
        loaded_payload['campaign']['daily_budget']['amount_micro'] = daily_budget
        loaded_payload['campaign']['goal']['optimize_fixed_cpc']['target_cpc']['currency'] = CURRENCY
        loaded_payload['campaign']['goal']['optimize_fixed_cpc']['target_cpc']['amount_micro'] = goal_setting
        loaded_payload['campaign']['catalog_item_ids'] = items
        loaded_payload['campaign']['enabling_state'] = enabling_state

        print("*********************************************")
        print("updating campaign {0} - id: {1}".format(row_num, campaign_id))
        print(UpdateCampaign(BASE_URL, ad_account_id, campaign_id, loaded_payload, token))
        print("*********************************************")

    return("Total {0} items are updated.".format(row_num))


def main():
    token = CreateToken(BASE_URL, EMAIL, PWD)
    response = BulkUpdateCampaignsFromFile(token)
    print(response)


if __name__ == '__main__':
    main()