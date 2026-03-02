import csv

uids = []
names = []
newsletters = []
is_member = False
marketing_consent = False
email = []
resource_name = []
check = None
users = []
subbed_emails = []


column_headings = ["first_name", "last_name", "newsletters", "is_Member", "marketing_consent","access_status", "email", "uid", "uid", "resource_name"]
temp_headings = ["Uids", "First_Name", "Last_Name", "Newsletters", "Status", "Is_Member", "Marketing_Consent", "Access_Status", "Email", "Resource_Name"]

csv_file = "new_report.csv"

data_csv = "my-report.csv"

sub_csv = "sub-log.csv"

with open(data_csv, "r", encoding="utf-8-sig") as new_read_file:
    reader = csv.reader(new_read_file)
    header = next(reader)

    for row in reader:
        first_name = row[header.index("Name")].split()[0]
        last_name = None
        if (len(row[header.index("Name")].split()) == 2):
            last_name = row[header.index("Name")].split()[1]
        if (row[header.index("I would like to receive emails providing details of selected offers, promotions and services from GB News and its group companies")] == "checked"):
            marketing_consent = True
        if (row[header.index("Access Count")] != "1" and row[header.index("Money Spent")] != "0 USD"):
            access_status = "member"
            is_member = True


        users.append({
            "Uids": row[header.index("User ID")], 
             "First_Name": first_name,
             "Last_Name": last_name,
             "Newsletters": "",
             "Status": "1",
             "Is_Member": is_member, 
             "Marketing_Consent": marketing_consent, 
             "Access_Status": access_status, 
             "Email": row[header.index("Email")], 
             "Resource_Name": ""
        })


def read_csv(next_csv, encode, column1, column2, column3, map, obj_list):
    with open(next_csv, mode="r", encoding=encode) as file:
        reader = csv.DictReader(file)
        for row in reader:
            map[row[column1]] = row[column2]
    for obj in obj_list:
        email = obj.get("Email")
        if email in map:
            obj[column3] = map[email]
    return obj_list

resource_map = {}

read_csv(sub_csv, 'utf-8', 'User email', 'Resource ID (RID)', 'Resource_Name', resource_map, users)

# with open(sub_csv, mode='r', encoding='utf-8') as f:
#     reader = csv.DictReader(f)
#     for row in reader:
#         # Store email as key for instant lookup
#         resource_map[row['User email']] = row['Resource ID (RID)']

# # 2. Update your objects (assuming they are in a list called 'my_objects')
# for obj in users:
#     email = obj.get("Email")
    
#     # Check if this email exists in our map
#     if email in resource_map:
#         obj["Resource_Name"] = resource_map[email]

# print(users, "users") 

# email_map = {}

# read_csv("edited3.csv", 'utf-8-sig', 'Emails', 'Newsletters', 'Newsletters', email_map, users)

# with open("edited3.csv", mode="r", encoding='utf-8-sig') as file:
#     reader = csv.DictReader(file)
#     for row in reader:
#         email_map[row["Emails"]] = row["Newsletters"]

# for user in users:
#     email = user.get("Email")

#     if email in email_map:
#         user["Newsletters"] = email_map[email]

# print(users, "edited object")


# clean fields (remove users not subscribed to anything)
# users = [u for u in users if u.get("Newsletters") and u["Newsletters"].strip() != ""]

# clean_users = []

# for user in users:
#     nl = user.get("Newsletters", "")
#     if nl and nl.strip():
#         clean_users.append(user)

# users = clean_users

with open(csv_file, "w", encoding="utf-8-sig", newline='') as f:
    writer = csv.DictWriter(f, fieldnames=temp_headings)
    writer.writeheader()
    writer.writerows(users)