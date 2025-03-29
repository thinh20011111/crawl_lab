import requests
import json
import os
import logging
import json
import jsonpath

class BaseApi:
    def __init__(self):
        self.api_url = "https://lab-sn.emso.vn/api/v1"
        self.oauth_url = "https://lab-sn.emso.vn/oauth"
        if not self.api_url:
            raise Exception("API_URL not set in environment variables.")
        if not self.oauth_url:
            raise Exception("OAUTH_URL not set in environment variables.")
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

    def get_access_token(self, username, password):
        data = {
            "username": username,
            "password": password,
            "grant_type": "password",
            "client_id": "Ev2mh1kSfbrea3IodHtNd7aA4QlkMbDIOPr4Y5eEjNg",
            "client_secret": "f2PrtRsNb7scscIn_3R_cz6k_fzPUv1uj7ZollSWBBY",
            "scope": "write read follow"
        }
        uri = f"{self.oauth_url}/token"
        response = requests.post(uri, headers=self.headers, data=json.dumps(data))
        if response.status_code == 200:
            response_dict = response.json()
            access_token = response_dict.get("access_token")
            return access_token
        else:
            self.log_response(response)
            response.raise_for_status()

    def set_headers(self, headers):
        self.headers.update(headers)

    def get(self, endpoint, params=None):
        uri = f"{self.api_url}{endpoint}"
        response = requests.get(uri, headers=self.headers, params=params)
        self.log_response(response)
        return response

    def post(self, endpoint, data=None):
        uri = f"{self.api_url}{endpoint}"
        response = requests.post(uri, headers=self.headers, data=json.dumps(data))
        self.log_response(response)
        return response

    def put(self, endpoint, data=None):
        uri = f"{self.api_url}{endpoint}"
        response = requests.put(uri, headers=self.headers, data=json.dumps(data))
        self.log_response(response)
        return response

    def delete(self, endpoint):
        uri = f"{self.api_url}{endpoint}"
        response = requests.delete(uri, headers=self.headers)
        self.log_response(response)
        return response

    def log_response(self, response):
        """Log the details of the HTTP response."""
        logging.info(f"URL: {response.url}")
        logging.info(f"Status Code: {response.status_code}")
        try:
            response_json = response.json()
            logging.info(f"Response JSON: {json.dumps(response_json, indent=2)}")
        except ValueError:  # Handle cases where response is not JSON
            logging.info(f"Response Text: {response.text}")

    def compare_response_status(self, response, expected_status_code):
        """Compare the response status code to the expected status code."""
        actual_status_code = response.status_code
        if actual_status_code == expected_status_code:
            logging.info(f"Test Case Passed: Status code {actual_status_code} matches the expected value {expected_status_code}")
        else:
            error_message = (
                f"Test Case Failed: Expected status code {expected_status_code}, "
                f"but got {actual_status_code}. URL: {response.url}, Response: {response.text}"
            )
            logging.error(error_message)
            raise AssertionError(error_message)

    def get_value_from_json(self, response_data, json_path):
        try:
            values = jsonpath.jsonpath(response_data, json_path)
            return values
        except Exception as e:
            logging.error(f"Error applying JSONPath: {e}")
            return None
        
    def marketplace_post(self, endpoint, data=None):
        uri = f"{self.marketplace_api_url}{endpoint}"
        response = requests.post(uri, headers=self.headers, data=json.dumps(data))
        self.log_response(response)
        return response
