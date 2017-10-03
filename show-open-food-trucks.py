"""
Write a command line program that prints out a list of food trucks that are open at the current date,
when the program is being run. So if I run the program on Friday, May 5 at noon, I should see a list
of all the food trucks that are open then.

This program uses The San Francisco Government's API found at
https://dev.socrata.com/foundry/data.sfgov.org/bbb8-hzi6
"""
import os
import requests
from tabulate import tabulate
from lib.query import QueryCurrentFoodTrucks


def query_api(offset):
    """
    This function calls the external API and returns a request object.
    """
    base_url = "http://data.sfgov.org/resource/bbb8-hzi6.json"
    query = QueryCurrentFoodTrucks(
        offset=offset
    ).build_query()
    url = "{0}{1}".format(base_url, query)

    if os.environ.get('FT_APP_TOKEN') is not None:
        header={'X-App-Token': os.environ.get('FT_APP_TOKEN')}
        request = requests.get(url, headers=header)
    else:
        request = requests.get(url)

    return request

def go_to_page(page, num):
    """
    This function calls to the API to retrieve the next page of data.
    """
    request = query_api(page)
    page += num
    keep_paging = True
    return (page, request, keep_paging)

def print_results_to_terminal(results):
    """
    This function uses the `tabulate` Python addon to print a well-formatted
    table of food trucks to the console.
    """
    trucks = []
    for foodtruck in data:
        trucks.append([foodtruck['applicant'], foodtruck['location']])
    columns = ["NAME", "ADDRESS"]
    table_format = "simple"
    print "\n", tabulate(trucks, columns, tablefmt=table_format)
    print "------PAGE {0}------\n".format(page)


keep_paging = True
page = 1
request = query_api(0)

while keep_paging:
    if request.ok:
        data = request.json()
        if len(data) == 0:
            print "\nYou've reached the end. Thanks!\n"
            break

        print_results_to_terminal(data)

        if page == 1:
            user_input = raw_input("See more results? (Y/N): ").lower()
            if user_input == "y" or user_input == "next":
                user_input = "next"
            elif user_input == "n":
                user_input = "exit"
            else:
                user_input = raw_input("I didn't get that. See more results? (Y/N): ").lower()
        else:
            user_input = raw_input("Where to? (next, prev or exit): ").lower()

        if user_input == "next":
            (page, request, keep_paging) = go_to_page(page, 1)
        elif user_input == "prev":
            (page, request, keep_paging) = go_to_page(page, -1)
        elif user_input == "exit":
            keep_paging = False
            break
        else:
            user_input = raw_input("I didn't get that. Where to? (next, prev or exit): ").lower()

    else:
        print "Something with awry with the request."

print "Goodbye!"
