import csv

new_file = "sub-log.csv"

my_list = []

temp_headings = ["Uids", "First_Name", "Last_Name", "Newsletters", "Is_Member", "Marketing_Consent", "Access_Status", "Email", "Resource_Name"]

with open(new_file, "r", encoding="utf-8-sig", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        if "jamal.davis+" in row["User email"]:
            my_list.append({
                "Uids": row["User ID (UID)"], 
                "First_Name": row["First name"],
                "Last_Name": row["Last name"],
                "Is_Member": "", 
                "Marketing_Consent": "", 
                "Access_Status": "", 
                "Email": row["User email"], 
                "Resource_Name": row["Resource ID (RID)"]
            })

with open("migration_test.csv", "w", encoding="utf-8-sig", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=temp_headings)
    writer.writeheader()
    writer.writerows(my_list)
        