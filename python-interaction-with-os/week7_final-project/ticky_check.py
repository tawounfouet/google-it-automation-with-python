#!/usr/bin/env python3

import re
import operator
import csv

per_user = {}
error = {}

with open("syslog.log") as file:
    for log in file.readlines():
        username = re.search(r"\((.*)\)", log).group(1)
        log_type = re.search(r"(INFO|ERROR)", log).group(1)
        if username not in per_user:
            per_user[username] = {"INFO": 0, "ERROR": 0}
        per_user[username][log_type] += 1
        if log_type == "ERROR":
            error_msg = re.search(r"ERROR (.*) ", log).group(1)
            if error_msg not in error:
                error[error_msg] = 0
            error[error_msg] += 1

sorted_per_user = sorted(per_user.items(), key=operator.itemgetter(0))
sorted_error = sorted(error.items(), key=operator.itemgetter(1), reverse=True)

with open("error_message.csv", "w") as error_file:
    writer = csv.writer(error_file)
    writer.writerow(["Error", "Count"])
    writer.writerows(sorted_error)

with open("user_statistics.csv", "w") as user_file:
    writer = csv.writer(user_file)
    writer.writerow(["Username", "INFO", "ERROR"])
    for item in sorted_per_user:
        writer.writerow([item[0], item[1]["INFO"], item[1]["ERROR"]])