import csv

my_csv = "edited3.csv"
new_csv = "clean-test.csv"
column_headings = ["Email", "Newsletters"]

my_list = []

with open(my_csv, mode="r", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    for row in reader:
        if "jamal.davis" in row["Emails"]:
            my_list.append({
                "Email": row["Emails"],
                "Newsletters": row["Newsletters"]
            })

 
with open(new_csv, "w", encoding="utf-8-sig", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=column_headings)
    writer.writeheader()
    writer.writerows(my_list)
