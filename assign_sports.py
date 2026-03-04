import requests
import csv

csv_file = "sport_newsletter.csv"
new_file = "edited_sports.csv"
nl_list = ["sport_newsletter.csv"]
# nl_list = ["sport_newsletter.csv", "tech_newsletter.csv", "gardening_newsletter.csv", "celebrity_newsletter.csv", "diet_newsletter.csv", "food_newsletter.csv", "travel_newsletter.csv", "health_newsletter.csv", "property_newsletter.csv", "opinion_newsletter.csv", "politics_newsletter.csv", "motoring_newsletter.csv", "news_newsletter.csv", "royal_newsletter.csv"]

column_headings = ["Emails", "Status"]
# column_headings = ["Emails", "Status", "Newsletters"]
emails = []
email_index = {}

# similar set up to assign_mailing_list but just for sports newsletters
def read_csv(nl_list):
    for i in range(len(nl_list)):
        # get newsletter name
        newsletter_name = nl_list[i].split("_")[0]
        with open(nl_list[i], "r", encoding="utf-8-sig") as file:
            reader = csv.reader(file)
            header = next(reader)

            for row in reader:
                if row[header.index("Status")] == "1":
                    email = row[header.index("Email")]

                    if email in email_index:
                        user = emails[email_index[email]]
                        if newsletter_name not in user["Newsletters"]:
                            user["Newsletters"].append(newsletter_name)
                    else:
                        email_index[email] = len(emails)
                        emails.append({
                            "Emails": email,
                            "Status": "1",
                            # "Newsletters": [newsletter_name]
                        })
                newsletter_name = nl_list[i].split("_")[0]

   

    return emails
read_csv(nl_list)
print(emails, "emails")

with open(new_file, "w", encoding="utf-8-sig") as new_doc:
    writer = csv.DictWriter(new_doc, fieldnames=column_headings)
    writer.writeheader()
    writer.writerows(emails)




