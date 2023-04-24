#!/usr/bin/python3
"""Script that uses JSONPlaceholder API to get information about an employee"""
import csv
import requests
import argparse


def get_employee_data(user_id: int, base_url: str = 'https://jsonplaceholder.typicode.com/') -> tuple:
    """
    Returns a tuple with the employee's name and a list of their completed tasks.
    """
    user_endpoint = f'{base_url}users/{user_id}'
    todos_endpoint = f'{base_url}todos?userId={user_id}'
    
    response = requests.get(user_endpoint)
    response.raise_for_status()  # Raise an exception if the request fails.
    user_data = response.json()
    name = user_data['username']

    response = requests.get(todos_endpoint)
    response.raise_for_status()
    tasks_data = response.json()
    tasks = [[user_id, name, task['completed'], task['title']] for task in tasks_data]
    
    return name, tasks


def save_employee_data_to_csv(data: tuple):
    """
    Saves employee data to a CSV file.
    """
    user_id, name, tasks = data
    filename = f'{user_id}.csv'
    with open(filename, mode='w', newline='') as employee_file:
        employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        for task in tasks:
            employee_writer.writerow(task)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get employee data from JSONPlaceholder API and save it to a CSV file.')
    parser.add_argument('user_id', type=int, help='The ID of the user to retrieve data for.')
    args = parser.parse_args()

    employee_data = get_employee_data(args.user_id)
    save_employee_data_to_csv((args.user_id, *employee_data))

