#!/usr/bin/env python3

# Author: Dhyey Patel
# Description: A simple command-line REST client using JSONPlaceholder API.

import argparse
import requests
import sys
import json
import csv
import os


class RestClient:
    BASE_URL = "https://jsonplaceholder.typicode.com"

    def __init__(self, method, endpoint, data=None, output=None):
        self.method = method.lower()
        self.endpoint = endpoint
        self.data = data
        self.output = output

    def send_request(self):
        """
        Sends the HTTP request (GET or POST) to the specified endpoint.
        """
        url = f"{self.BASE_URL}{self.endpoint}"
        try:
            if self.method == "get":
                response = requests.get(url)
            elif self.method == "post":
                if not self.data:
                    raise ValueError("For POST requests, data is required.")
                response = requests.post(url, json=json.loads(self.data))
            else:
                raise ValueError(f"Unsupported HTTP method: {self.method}")
            self.handle_response(response)

        except requests.RequestException as e:
            print(f"Network error: {e}")
            sys.exit(1)
        except ValueError as e:
            print(f"Invalid input: {e}")
            sys.exit(1)

    def handle_response(self, response):
        """
        Processes the HTTP response from the server.
        """
        print(f"HTTP Status Code: {response.status_code}")

        if not response.ok:
            print("Error: Request was not successful.")
            sys.exit(1)
        if self.output:
            self.save_response(response.json())
        else:
            print(json.dumps(response.json(), indent=4))

    def save_response(self, data):
        """
        Saves the response data to a file in JSON or CSV format.
        """
        _, ext = os.path.splitext(self.output)

        if ext == ".json":
            self.save_json(data)
        elif ext == ".csv":
            self.save_csv(data)
        else:
            print(f"Error: Unsupported file format '{ext}'.")
            sys.exit(1)

    def save_json(self, data):
        """
        Saves data to a JSON file.
        """
        try:
            with open(self.output, "w") as f:
                json.dump(data, f, indent=4)
            print(f"Response successfully saved to {self.output}")
        except Exception as e:
            print(f"File write error: {e}")
            sys.exit(1)

    def save_csv(self, data):
        """
        Saves data to a CSV file.
        """
        if not isinstance(data, list):
            data = [data]

        try:
            with open(self.output, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
            print(f"Response successfully saved to {self.output}")
        except Exception as e:
            print(f"File write error: {e}")
            sys.exit(1)


def main():
    """
    Entry point for the script. Parses command-line arguments and starts the RestClient.
    """
    parser = argparse.ArgumentParser(
        description="A simple command-line REST client using JSONPlaceholder API."
    )
    parser.add_argument(
        "method", choices=["get", "post"], help="HTTP request method (GET or POST)"
    )
    parser.add_argument("endpoint", help="API endpoint URI fragment (e.g., /posts/1)")
    parser.add_argument(
        "-d", "--data", help="Data payload for POST request (JSON format)"
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Save response to a .json or .csv file (default: print to console)",
    )

    args = parser.parse_args()
    client = RestClient(args.method, args.endpoint, args.data, args.output)
    client.send_request()


if __name__ == "__main__":
    main()
