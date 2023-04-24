#!/usr/bin/python3
""" Script that uses JSONPlaceholder API to get information about an employee """

import requests
import sys

def get_employee_data(employee_id):
    url = 'https://jsonplaceholder.typicode.com/'

    user = f"{url}users/{employee_id}"
    res = requests.get(user)
    json_o = res.json()

    todos = f"{url}todos?userId={employee_id}"
    res = requests.get(todos)
    tasks = res.json()

    completed_tasks = [task for task in tasks if task.get("completed")]

    return json_o, completed_tasks, tasks


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 employee_data.py <employee_id>")
        sys.exit(1)

    employee_id = sys.argv[1]
    json_o, completed_tasks, tasks = get_employee_data(employee_id)

    print(f"Employee {json_o.get('name')} is done with tasks ({len(completed_tasks)}/{len(tasks)}):")
    for task in completed_tasks:
        print(f"\t{task.get('title')}")
