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

URL = 'https://'+ PLATFORM_NAME +'-dcsn.rmp-api.moloco.com/rmp/decision/v1/platforms/' + PLATFORM_ID + '/creative-auction'

# Insert INVENTORY_ID. 
INVENTORY_ID = ''

PAYLOAD = {
    "request_id": "", # Required. A unique identifier of the request. Short UUID (16) will be perfectly fit with it.
    "user": {
        "user_id": "", # Required. User ID that matches with the user ID of the events.
    },
    "inventory": {
        "inventory_id": INVENTORY_ID, # Required.   
    },
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
    print(json.dumps(dict(responded_items), indent=4))

    return(response)

if __name__ == '__main__':
    main()