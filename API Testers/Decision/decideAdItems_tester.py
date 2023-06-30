# Copyright 2022 Moloco, Inc
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

import requests
import json

# Insert PLATFORM NAME, PLATFORM ID, and Event API key shared by your MOLOCO representative.
PLATFORM_NAME = ''
PLATFORM_ID = ''
API_KEY = ''

URL = 'https://' + PLATFORM_NAME + '-dcsn.rmp-api.moloco.com/rmp/decision/v1/platforms/' + PLATFORM_ID + '/auction'

# Insert INVENTORY_ID. 
INVENTORY_ID = ''


PAYLOAD = {
    "request_id": "", # Required. A unique identifier of the request. Short UUID (16) will be perfectly fit with it.
    "session_id": "", # Required. Session ID from the user session.
    "user": {
        "user_id": "", # Required. User ID that matches with the user ID of the events.
        "year_of_birth": 2000, # Optional
        "gender": "" # Male / Female - optional
    },
    "device": {
        "unique_device_id": "" # Optional
    },
    "inventory": {
        "inventory_id": INVENTORY_ID, # Required. 
        "num_items": 50, # Required. It's highly recommended to set this value under 50.
        "items": [ "001", "002" ], # In case the ad items should be related to certain items, please put id of the certain item at here.
        "categories": [ "Women>Shoes>Sneakers", "Asia>Seoul" ], # In case the ad items should be related to certain category, please use this field.
        "search_query": "" # If the inventory is at the search result page, this field is required.
    },
    "page_id": "" # 
}

HEADERS = {
    "accept": "application/json",
    "content-type": "application/json",
    "X-Api-Key": API_KEY # Insert API key shared by Moloco representative here
}


def main():
    response = requests.post(URL, json=PAYLOAD, headers=HEADERS)
    print("Response headers:")
    print(json.dumps(dict(response.headers), indent=4))

    print("\nResponse body:")
    responded_items = json.loads(response.text)
    list_of_items = []
    for items in responded_items["decided_items"]:
        print(json.dumps(items, indent=4))
        list_of_items.append(items["item_id"])
    
    
    print("\nTotal", len(list_of_items), "items returned")
    print("Item IDs are:", list_of_items)

    return(response)

if __name__ == '__main__':
    main()