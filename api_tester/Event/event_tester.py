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

import time
import requests
import shortuuid

# Insert PLATFORM NAME, PLATFORM ID, and Event API key shared by your MOLOCO representative.
PLATFORM_NAME = ''
PLATFORM_ID = ''
API_KEY = ""

URL = "https://" + PLATFORM_NAME +"-evt.rmp-api.moloco.com/rmp/event/v1/platforms/" + PLATFORM_ID + "/userevents"
HEADERS = {
    "Content-Type": "application/json",
    "X-API-Key": API_KEY
}

# Base event payload
PAYLOAD = {
    "event_type": "UNKNOWN_EVENT_TYPE",
    "channel_type": "APP", # the value can be "APP" or "SITE"
    "id": str(shortuuid.ShortUUID().random(length=8)), 
    "timestamp": str(round(time.time()*1000)), # Unix timestamp in milliseconds that the event happened at.
    "user_id": "USER_ID", # Replace the value with your user id. Recommended to hash it before sending for anonymization. The length should not exceed 128.
    "session_id": "SESSION_ID", # Replace the value with your session id. it is for tracking users regardless of sign-in status. The length should not exceed 128.
    "device": {
        "os": "ios", # OS of the device. "ios" or "android" must be included for the App channel type.
        "os_version": "14.4.1" # Device OS version, which is taken from the device without manipulation or normalization. (e.g., "14.4.1")
    }
}

# For each event, there are parameters that required. Below is the sample event of each event type:

HOME = (PAYLOAD | {
    "event_type": "HOME"
})

LAND = (PAYLOAD | {
    "event_type": "LAND",
    "page_id": "app/product/001", # The page id of the user landed. 
    "referrer_page_id": "google.com?q=sample+product" # The page id that brought the user here.
})

PAGE_VIEW = (PAYLOAD |{
    "event_type": "PAGE_VIEW",
    
    # The PAGE_VIEW event requires the page id of the user browsing the page.
    "page_id": "app/productlist/001" 
})

SEARCH = (PAYLOAD | {
    "event_type": "SEARCH",
    "page_id": "app/search", 
    
    # The SEARCH event requires a search_query parameter. If it is missed, the API will return a validation error.
    "search_query": "MEN" 
})

ITEM_PAGE_VIEW = (PAYLOAD |{
    "event_type": "ITEM_PAGE_VIEW",
    "page_id": "app/product/001",
    "referrer_page_id": "app/productlist/001", 

    # The ITEM_PAGE_VIEW event requires the item metadata.
    "items" : [
        { 
            "id": "", # Replace the value with the item id that the user browsing
            "price": "", # The price of the item.
            "quantity": 1
        }
    ]
})

PURCHASE = (PAYLOAD |{
    "event_type": "PURCHASE",
    "page_id": "app/checkout",

    # The PURCHASE event requires the item metadata and revenue object.
    "items" : [
        {
            "id": "", # Replace the value with the item id that the user purchased
            "price": "", # The price of the item. If the item is on discount, please set the discounted price here.
            "quantity": 1 # The quantity of the item purchased.
        },
        {
            "id": "", 
            "price": "", 
            "quantity": 1 
        }
    ],
    "revenue": { 
        "currency": "KRW", # Replace the value with the currency code that the platform uses.
        "amount": "" # The amount should be SUM(item.price * item.quantity).
    },
})

ADD_TO_CART = (PAYLOAD |{
    "event_type": "ADD_TO_CART",
    "page_id": "app/product/001",

    # The ADD_TO_CART event requires the item metadata.
    "items" : [
        { 
            "id": "", # Replace the value with the item id that the user browsing
            "price": "", # The price of the item.
            "quantity": 1
        }
    ]
})

ADD_TO_WISHLIST = (PAYLOAD |{
    "event_type": "ADD_TO_WISHLIST",
    "page_id": "app/product/001",

    # The ADD_TO_WISHLIST event requires the item metadata.
    "items" : [
        { 
            "id": "", # Replace the value with the item id that the user browsing
            "price": "", # The price of the item.
            "quantity": 1
        }
    ]
})


def main():
    request_payload = HOME # Replace the value with one of the event types above.
    print(request_payload)
    response = requests.post(URL, json=request_payload, headers=HEADERS)
    return(response)

if __name__ == '__main__':
    response = main()
    print(response)