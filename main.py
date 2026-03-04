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
temp_headings = ["Uids", "First_Name", "Last_Name", "Newsletters", "Is_Member", "Marketing_Consent", "Access_Status", "Email", "Resource_Name"]

csv_file = "user_test.csv"

data_csv = "my-report.csv"

sub_csv = "migration_test.csv"

newsletter_csv = "clean-test.csv"


# read values from csv (includes resource names, custom field values, & generic user information)
with open(sub_csv, "r", encoding="utf-8-sig") as new_read_file:
    reader = csv.reader(new_read_file)
    header = next(reader)

    for row in reader:
        # first_name = row[header.index("Name")].split()[0]
        # last_name = None
        # if (len(row[header.index("Name")].split()) == 2):
        #     last_name = row[header.index("Name")].split()[1]
        # if (row[header.index("I would like to receive emails providing details of selected offers, promotions and services from GB News and its group companies")] == "checked"):
        #     marketing_consent = True
        # if (row[header.index("Access Count")] != "1" and row[header.index("Money Spent")] != "0 USD"):
        #     access_status = "member"
        #     is_member = True


        users.append({
            "Uids": row[header.index("Uids")], 
             "First_Name": row[header.index("First_Name")],
             "Last_Name": row[header.index("Last_Name")],
             "Newsletters": "",
             "Is_Member": "", 
             "Marketing_Consent": "", 
             "Access_Status": "", 
             "Email": row[header.index("Email")], 
             "Resource_Name": row[header.index("Resource_Name")]
        })

# format newsletter array
def handleList(lean_newsletters):
    lean_map = lean_newsletters.replace("[", "").replace("]", "").replace("'", "")
    return lean_map

def read_csv(next_csv, encode, column1, column2, column3, email_map, obj_list):
    # STEP 1: Build the map first (Flat loop - 500k operations)
    with open(next_csv, mode="r", encoding=encode) as file:
        reader = csv.DictReader(file)
        for row in reader:
            email_map[row[column1]] = row[column2]
    
    # STEP 2: Create a set of emails we already have for lightning-fast lookup
    existing_emails = {obj.get("Email") for obj in obj_list if obj.get("Email")}

    # STEP 3: Update existing users (Flat loop - 500k operations)
    for obj in obj_list:
        email = obj.get("Email")
        if email in email_map:            
            obj[column3] = handleList(email_map[email])

    # STEP 4: Add new users that were in the CSV but NOT in our list
    # We loop through the map keys to find "strangers"
    for email, newsletters in email_map.items():
        if email not in existing_emails:
            lean_newsletters = handleList(newsletters)
            obj_list.append({
                "Uids": "", 
                "First_Name": "",
                "Last_Name": "",
                "Newsletters": lean_newsletters,
                "Is_Member": "", 
                "Marketing_Consent": "", 
                "Access_Status": "", 
                "Email": email, 
                "Resource_Name": ""
            })
    
    return obj_list


email_map = {}

read_csv(newsletter_csv, 'utf-8-sig', 'Email', 'Newsletters', 'Newsletters', email_map, users)

# write the final csv final
with open(csv_file, "w", encoding="utf-8-sig", newline='') as f:
    writer = csv.DictWriter(f, fieldnames=temp_headings)
    writer.writeheader()
    writer.writerows(users)