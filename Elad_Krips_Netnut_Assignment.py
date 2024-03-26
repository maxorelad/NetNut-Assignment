import requests
from datetime import datetime
import time
import logging

# Configure logging
logging.basicConfig(filename='currency_fetcher.log', level=logging.INFO)

# Constants
API_KEY = '903da0d54db4499ea51f1f73152ddda7'
# oxr doc: https://docs.openexchangerates.org/reference/api-introduction
API_LINK = f'https://openexchangerates.org/api/latest.json?app_id={API_KEY}'
HOURS_TO_FETCH = 24
RETRY_MAX_ATTEMPTS = 3
RETRY_DELAY_SECONDS = 5


def unix_timestamp_to_datetime(unix_timestamp):
    dt_object = datetime.fromtimestamp(unix_timestamp)
    return dt_object.strftime('%d/%m/%Y %H:%M:%S')


def fetch_currency_data():
    retry = 0
    headers = {'Accept': 'application/json'}
    while retry < RETRY_MAX_ATTEMPTS:
        try:
            # Make API request
            req = requests.get(API_LINK, headers=headers, timeout=10)
            req.raise_for_status()  # Raise an exception for bad status codes

            # Parse response
            con_dict = req.json()
            timestamp = con_dict['timestamp']
            formatted_date_time = unix_timestamp_to_datetime(timestamp)
            USD2ILS = con_dict['rates']['ILS']
            return USD2ILS, formatted_date_time
        except requests.exceptions.RequestException as e:
            # Log error and retry
            logging.error(f"An error occurred: {e}")
            logging.info(f"Retrying in {RETRY_DELAY_SECONDS} seconds...")
            retry += 1
            time.sleep(RETRY_DELAY_SECONDS)
    logging.error("Maximum retries exceeded. Exiting program.")
    exit()


def main():
    """Main function to fetch currency data for 24 hours."""
    for hour in range(HOURS_TO_FETCH):
        USD2ILS, formatted_date_time = fetch_currency_data()
        # Print and log fetched data
        info = f'USD value in ILS: {USD2ILS}, timestamp: {formatted_date_time}'
        print(info)
        logging.info(info)

        # Sleep for an hour
        time.sleep(3600)
    logging.info("Currency data fetched for 24 hours.")


if __name__ == "__main__":
    main()
