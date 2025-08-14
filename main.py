import json
import argparse
from tabulate import tabulate

parse = argparse.ArgumentParser()
parse.add_argument("--file", required=True, nargs="+")
parse.add_argument("--report", choices=["average"])

parsed = parse.parse_args()

data = {}

#Group by handler
for i in parsed.file:
    with open(i, "r", encoding="UTF-8") as f:
        for line in f:
            line_dict = json.loads(line)
            url = line_dict["url"]
            if url not in data:
                data[url] = {"total": 0, "response_time_sum": 0}
            data[url]["total"] += 1
            data[url]["response_time_sum"] += line_dict["response_time"]

#converting for print
table_data = []
if parsed.report == "average":
    for url, stats in data.items():
        avg_time = stats["response_time_sum"] / stats["total"]
        table_data.append([url, stats["total"], round(avg_time, 3)])
    headers = ["handler", "total", "avg_response_time"]
else:
    for url, stats in data.items():
        table_data.append([url, stats["total"]])
    headers = ["handler", "total"]

table_data.sort(key=lambda x: x[1], reverse=True)
table_data = [[ind] + infor for ind, infor in enumerate(table_data)]

print(tabulate(table_data, headers=headers, tablefmt="psql"))