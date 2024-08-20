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

# Create ad account based on the data provided at the file
def CreateAdAccount(base_url, ad_account_id, ad_account_title, token):
    url = base_url + "/ad-accounts"
    payload = {
        "ad_account": {
            "state_info": {
                "state": "ACTIVE",
                "state_case": "INIT_BY_PLATFORM",
                "ad_account_id": ad_account_id
            },
            "id": ad_account_id,
            "title": ad_account_title,
            "timezone": TIMEZONE
        }
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": "Bearer " + token
    }
    response = requests.post(url, json=payload, headers=headers)
    json_formatted = json.loads(response.text)
    return (json_formatted)

# Create single campaign
def CreateCampaign(base_url, ad_account_id, campaign_title, goal_setting, daily_budget, start_date, end_date,
                   catalog_item_ids, enabling_state, token):
    url = base_url + "/ad-accounts/" + ad_account_id + "/campaigns"
    payload = {
        "campaign": {
            "title": campaign_title,
            "ad_account_id": ad_account_id,
            "ad_type": "ITEM",
            "schedule": {
                "start": start_date,
                "end": end_date
            },
            "daily_budget": {
                "currency": CURRENCY,
                "amount_micro": daily_budget
            },
            "goal": {
                "type": "FIXED_CPC",
                "optimize_fixed_cpc": {
                    "target_cpc": {
                        "currency": CURRENCY,
                        "amount_micro": goal_setting,
                    }
                }
            },
            "catalog_item_ids": catalog_item_ids,
            "enabling_state": enabling_state
        }
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": "Bearer " + token
    }
    response = requests.post(url, json=payload, headers=headers)
    json_formatted = json.loads(response.text)
    print(json.dumps(json_formatted, indent=4))
    return (json_formatted)

# Create campaigns based on the data provided at the file
def BulkCreateCampaignsFromFile(token):
    for row_num, data in enumerate(ParseFile()):
        ad_account_id = data['ad_account_id'].replace('"', '').strip()
        ad_account_title = data['ad_account_title'].replace('"', '').strip()
        campaign_title = data['campaign_title'].replace('"', '').strip()
        goal_setting = data['goal_setting'].replace('"', '').strip()
        daily_budget = data['daily_budget_max'].replace('"', '').strip()
        schedule_start = data['campaign_schedule_start'].replace('"', '').strip()
        schedule_end = data['campaign_schedule_end'].replace('"', '').strip()
        items = [item.replace('[', '').replace(']', '').replace(',', '') for item in data['items'].replace('"', '').strip().split()]
        enabling_state = data['enabling_state'].replace('"', '').strip()

        print("*********************************************")
        print("creating data {0}: {1}".format(row_num, data))
        print("ad account: id {id} / title {title}".format(id=ad_account_id, title=ad_account_title))
        print(CreateAdAccount(BASE_URL, ad_account_id, ad_account_title, token))

        print("campaign: title {title}".format(title=campaign_title))
        print(CreateCampaign(BASE_URL, ad_account_id, campaign_title, goal_setting,
                       daily_budget, schedule_start, schedule_end, items, enabling_state, token))
        print("*********************************************")
    return("Total {0} items are created.".format(row_num+1))


def main():
    token = CreateToken(BASE_URL, EMAIL, PWD)
    response = BulkCreateCampaignsFromFile(token)
    print(response)


if __name__ == '__main__':
    main()