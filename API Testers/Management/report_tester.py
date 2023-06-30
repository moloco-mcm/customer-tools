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

import json
import requests

PLATFORM_NAME = "" # Platform name. e.g. MOLOCO
PLATFORM = "" # Platform ID e.g. MOLOCO_TEST

# Provide PLATFORM_OWNER credential to get token and call management APIs
EMAIL = ""
PW = ""

# Specify ad account id to get report from. If it is empty, QueryPlatformSummary will be called.
AD_ACCOUNT_ID = "" 

# Put report API payload specification here.
# For detailed spec, please refer below urls:
# https://moloco-rmp.readme.io/reference/rmpmanagementapi_queryadaccountsummary
# https://moloco-rmp.readme.io/reference/rmpmanagementapi_queryplatformsummary  
TIMEZONE = "Asia/Seoul" 
DATE_START = "2023-06-05" 
DATE_END = "2023-06-18"
GROUP_BY = ["DATE", "CURRENCY"]
ORDER_BY = ["TIME_DATE"]

URL = "https://" + PLATFORM_NAME + "-mgmt.rmp-api.moloco.com/rmp/mgmt/v1/platforms/" + PLATFORM 

# Get token based on the credential
def CreateToken(base_url, email, pw):
    url = base_url + "/tokens"
    print(url)
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
    print(json.dumps(json_formatted,indent=4))
    return(json_formatted["token"])

# To query report for an ad account
def QueryAdAccountSummary(base_url, token, ad_account_id):
    url = base_url + "/ad-accounts/" + ad_account_id + "/report"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + token
        }
    payload = {
        "timezone": TIMEZONE,
        "date_start": DATE_START,
        "date_end": DATE_END,
        "group_by": GROUP_BY,
        "order_by": ORDER_BY
    }
    response = requests.post(url, json=payload, headers=headers)
    return(response.text)

# To query report for the platform
def QueryPlatformSummary(base_url, token):
    url = base_url + "/report"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + token
        }
    payload = {
        "timezone": TIMEZONE,
        "date_start": DATE_START,
        "date_end": DATE_END,
        "group_by": GROUP_BY,
        "order_by": ORDER_BY
    }
    response = requests.post(url, json=payload, headers=headers)
    return(response.text)


def main():
    # Get token to call management APIs
    token = CreateToken(URL, EMAIL, PW)

    # If the ad account id is not provided, then call QueryPlatformSummary. 
    # Else call QueryAdAccountSummary with given ad account id.
    if AD_ACCOUNT_ID == "": 
        response = QueryPlatformSummary(URL, token)
        json_formatted = json.loads(response)
        print(json.dumps(json_formatted,indent=4))
    else:
        response = QueryAdAccountSummary(URL, token, AD_ACCOUNT_ID)
        json_formatted = json.loads(response)
        print(json.dumps(json_formatted,indent=4))


if __name__ == '__main__':
    main()

