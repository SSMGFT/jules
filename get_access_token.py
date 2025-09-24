import logging
from kiteconnect import KiteConnect

# --- User-configurable variables ---
# Replace with your actual API key and secret
API_KEY = "YOUR_API_KEY"
API_SECRET = "YOUR_API_SECRET"
ACCESS_TOKEN_FILE = "access_token.txt"


def main():
    """
    Main function to handle the login flow and get the access token.
    """
    logging.basicConfig(level=logging.INFO)

    # Initialize KiteConnect
    try:
        kite = KiteConnect(api_key=API_KEY)
    except Exception as e:
        logging.error(f"Failed to initialize KiteConnect: {e}")
        return

    # --- 1. Get the login URL ---
    login_url = kite.login_url()
    logging.info(f"Please go to the following URL to log in: {login_url}")

    # --- 2. Get the request token from the user ---
    request_token = input("Please enter the request_token from the redirect URL: ")

    # --- 3. Generate the access token ---
    try:
        data = kite.generate_session(request_token, api_secret=API_SECRET)
        access_token = data["access_token"]
        logging.info("Successfully generated access token.")
    except Exception as e:
        logging.error(f"Failed to generate access token: {e}")
        return

    # --- 4. Save the access token to a file ---
    try:
        with open(ACCESS_TOKEN_FILE, "w") as f:
            f.write(access_token)
        logging.info(f"Access token saved to {ACCESS_TOKEN_FILE}")
    except Exception as e:
        logging.error(f"Failed to save access token to file: {e}")


if __name__ == "__main__":
    main()