import csv
import requests
import json
from pprint import pprint
import time
import ast

import os

# handle checkpoint in case program crashes or runs into an error

CHECKPOINT_FILE = "migration_progress.txt"

def get_last_processed_index():
    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE, "r") as f:
            return int(f.read().strip())
    return 0

def save_checkpoint(index):
    with open(CHECKPOINT_FILE, "w") as f:
        f.write(str(index))

# newsletter_csv = "edited_sports.csv"
test_csv = "clean-test.csv"
test_emails = []
users_in_pw = []

# read newsletter values from csv
with open(test_csv, mode="r", encoding="utf-8-sig", newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if "jamal.davis+test" in row["Email"]:
            email = row["Email"]
            test_emails.append({
                "Email": email,
                "Newsletter": row["Newsletters"]
                })

headers = {
  'Content-Type': 'application/json'
}

# check if user is already in PW
def get_user(test_emails, sample):
    get_req_body = json.dumps({
        "request": {
            "application": "AB023-DEB30",
            "hwid": test_emails[sample]["Email"]
        }
    })
    get_url = "https://api.pushwoosh.com/json/1.3/getTags"

    get_req_info = requests.post(get_url, headers=headers, data=get_req_body)

    get_req_response = get_req_info.json()

    return get_req_response

get_user(test_emails, 4)

for i in range(len(test_emails)):
    temp = get_user(test_emails, i)
    if temp["response"]["result"]:
        users_in_pw.append(get_user(test_emails, i))

# for i in range(len(users_in_pw)):
#     try: 
#         if users_in_pw[i]["response"]["result"]["newsletters"]:
#             print(users_in_pw[i], "user has nl")
#             print(" ")
#             url = "https://api.pushwoosh.com/json/1.3/setTags"



#             req_body = json.dumps({
#                 "request" : {
#                     "application" : "AB023-DEB30",
#                     "hwid": test_emails[i]["Email"],
#                     "tags": {
#                         "newsletters": {
#                             "operation": "append",
#                             "value": [
#                                 test_emails[i]["Newsletters"]
#                             ]
#                         }
#                     }
#                 }
#             })

#             req = requests.post(url, headers=headers, data=req_body)

#             response = req.json()
#             print(test_emails[i])


#     except Exception as e:
#         print(e)


# update user in pushwoosh in batches, with sufficient wait time between calls
def update_user(user_data):
    retries = 5
    wait_time = 2 

    # Convert the string "['news', 'tech']" into a real Python list ['news', 'tech']
    try:
        newsletter_list = ast.literal_eval(user_data["Newsletter"])
        if not isinstance(newsletter_list, list):
            newsletter_list = [user_data["Newsletter"]]
    except:
        newsletter_list = [user_data["Newsletter"]]

    # Construct the actual PushWoosh payload inside the function
    payload = {
        "request": {
            "application": "AB023-DEB30",
            "hwid": user_data["Email"],
            "tags": {
                "newsletters": {
                    "operation": "append", # This ensures you don't overwrite
                    "value": [user_data["Newsletter"]]
                }
            }
        }
    }
    
    for i in range(retries):
        response = requests.post("https://api.pushwoosh.com/json/1.3/setTags", headers=headers, json=payload)
        
        if response.status_code == 200:
            return True
        elif response.status_code == 429:  # Rate Limited
            print(f"Rate limited! Sleeping for {wait_time}s...")
            time.sleep(wait_time)
            wait_time *= 2  # Exponential backoff
        else:
            print(f"Error {response.status_code}: {response.text}")
            break
    return False

start_index = get_last_processed_index()

# Process in chunks of 100 to report progress
for i, user in enumerate(test_emails):
    if i < start_index:
        continue
    success = update_user(user)
    if success:
        save_checkpoint(i) # Update the file after every successful migration
    if i % 100 == 0:
        print(f"Progress: {i}/500,000")
