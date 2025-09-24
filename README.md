# Kite Connect Trading Application

This application uses the Kite Connect API to find and trade Natural Gas futures and options on the MCX exchange.

## How to Use

Follow these steps to set up and run the application:

### 1. Prerequisites

- You need a Zerodha Kite developer account with an API key and secret.
- You must have Python 3.13.5 installed.

### 2. Installation

The necessary `kiteconnect` library has already been installed for you.

### 3. Generate Your Access Token

Before you can use the trading application, you need to generate an access token. This is a one-time process for each day you use the app.

1.  **Fill in your credentials**: Open the `get_access_token.py` file and replace `"YOUR_API_KEY"` and `"YOUR_API_SECRET"` with your actual Kite Connect API key and secret.

2.  **Run the script**:
    ```bash
    python get_access_token.py
    ```

3.  **Log in**: The script will print a login URL. Copy and paste this URL into your web browser and log in with your Kite credentials.

4.  **Get the request token**: After logging in, you will be redirected to a URL that contains a `request_token`. Copy this token.

5.  **Enter the request token**: Paste the `request_token` into the terminal where the script is running and press Enter.

The script will then generate an `access_token.txt` file. This file is used by the main trading application to authenticate with the Kite API.

### 4. Run the Trading Application

1.  **Fill in your API key**: Open the `trading_app.py` file and replace `"YOUR_API_KEY"` with your actual Kite Connect API key.

2.  **Run the script**:
    ```bash
    python trading_app.py
    ```

The application will then:
- Connect to the Kite API using your access token.
- Find the Natural Gas future for October.
- Determine the at-the-money (ATM) strike price.
- Place market orders for one lot of the corresponding Call (CE) and Put (PE) options.
- Display the server's response for each order.
- Wait for you to press Enter before closing.

**Important Notes:**

- The access token is valid for a single day. You will need to run `get_access_token.py` each day you want to use the application.
- This script is for educational purposes and demonstrates how to use the Kite Connect API. Trading in financial markets involves risk. Please use this script responsibly.