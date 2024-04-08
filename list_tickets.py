import re
import os
import datetime
import time
import numpy as np
import pandas as pd


path = "C:\\Users\\2204546\\Downloads\\ArconQueryResults\\"
download_path = "C:\\Users\\2204546\\Downloads\\Querylist\\"

# Listing the files in ArconQueryResult
dir_path = os.listdir(path=path)
file_name_np_array = np.array(dir_path)

# Getting the current time
# use this when required for a date prior than the current date.
current_time = datetime.datetime.now() - datetime.timedelta(days=0)
# current_time = datetime.datetime.today()


# Final list of the ticket for the current date
today_tickets = {"Ticket": [], "Assigned To": [], "modified at": []}

# Getting the today's date in dd_mm_yy format
today_date_format = f"{current_time.day}_{current_time.month}_{datetime.datetime.now().strftime('%y')}"
# print(current_time.day)


def filter(file_names):
    print("reading files...")
    for file_name in file_names:
        # print(file_name)
        # Selecting the file only for current date.
        # print(re.search(pattern=r"_\d{0,}_\d{0,}_\d{2}", string=file_name))
        if f"_{today_date_format}" in file_name:
            # getting the file creation/modification time
            time_stamp_unix = os.path.getmtime(path+file_name)
            time_stamp_local = time.ctime(time_stamp_unix)
            # print(time_stamp_local)
            # filtering out the ticket number and assignee name from the file name.
            ticket_start, ticket_end = re.search(
                pattern=r"GEM[a-bA-Z]*-\d+", string=file_name).span()
            ticket_number = file_name[ticket_start:ticket_end]
            assigned_to = re.search(r"\[(.*)\]", string=file_name).groups()[0]

            # Adding ticket number and their respective assignee in the to the final list.
            today_tickets["Ticket"].append(ticket_number)
            today_tickets["Assigned To"].append(assigned_to)
            today_tickets["modified at"].append(time_stamp_local)
            # today_tickets["Ticket"] = list(set(today_tickets["Ticket"]))
            # today_tickets["Assigned To"] = list(set(today_tickets["Assigned To"]))
    print("getting tickets...")
    return today_tickets


# Getting the file names in correct format and creating csv for them.
today_tickets = filter(file_name_np_array)
# print(today_tickets)
df = pd.DataFrame(today_tickets)
print("saving tickets to file...")
df.to_csv(f'{download_path}QueryTickets_{today_date_format}.csv', index=True)


# Example format
# file_name = "GEMPRODSUP-36814_10_11_23-1.txt.txt"
