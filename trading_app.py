import logging
import datetime
from kiteconnect import KiteConnect

# --- User-configurable variables ---
# Replace with your actual API key
API_KEY = "YOUR_API_KEY"
ACCESS_TOKEN_FILE = "access_token.txt"

# --- Constants ---
EXCHANGE = "MCX"
INSTRUMENT_TYPE_FUT = "FUT"
INSTRUMENT_TYPE_CE = "CE"
INSTRUMENT_TYPE_PE = "PE"
PRODUCT = "NRML"  # For Futures and Options
ORDER_TYPE = "MARKET"
VALIDITY = "DAY"
TRANSACTION_TYPE_BUY = "BUY"
FUTURES_SYMBOL_BASE = "NATURALGAS"
MONTH_ABBR = "OCT"


def main():
    """
    Main function to run the trading application.
    """
    logging.basicConfig(level=logging.INFO)

    # --- 1. Read the access token from the file ---
    try:
        with open(ACCESS_TOKEN_FILE, "r") as f:
            access_token = f.read().strip()
        logging.info("Successfully read access token.")
    except FileNotFoundError:
        logging.error(
            f"Access token file '{ACCESS_TOKEN_FILE}' not found. "
            f"Please run `get_access_token.py` first to generate the access token."
        )
        return
    except Exception as e:
        logging.error(f"Failed to read access token: {e}")
        return

    # --- 2. Initialize KiteConnect ---
    try:
        kite = KiteConnect(api_key=API_KEY)
        kite.set_access_token(access_token)
    except Exception as e:
        logging.error(f"Failed to initialize KiteConnect: {e}")
        return

    # --- 3. Fetch all instruments for the specified exchange ---
    try:
        instruments = kite.instruments(EXCHANGE)
        logging.info(f"Successfully fetched {len(instruments)} instruments for {EXCHANGE}.")
    except Exception as e:
        logging.error(f"Failed to fetch instruments: {e}")
        return

    # --- 4. Find the Natural Gas future for the specified month ---
    current_year_short = str(datetime.date.today().year)[-2:]
    # Construct the expected tradingsymbol, e.g., NATURALGAS25OCTFUT
    expected_tradingsymbol = f"{FUTURES_SYMBOL_BASE}{current_year_short}{MONTH_ABBR}FUT"

    natural_gas_future = None
    for instrument in instruments:
        if instrument["tradingsymbol"] == expected_tradingsymbol:
            natural_gas_future = instrument
            break

    if not natural_gas_future:
        logging.error(f"Could not find future with tradingsymbol: {expected_tradingsymbol}.")
        return

    logging.info(f"Found Natural Gas future: {natural_gas_future['tradingsymbol']}")
    # Extract the series identifier from the future's symbol (e.g., "NATURALGAS24OCT")
    future_series = natural_gas_future['tradingsymbol'].replace('FUT', '')


    # --- 5. Get the last traded price (LTP) of the future to determine the ATM strike ---
    try:
        quote = kite.quote(f"{EXCHANGE}:{natural_gas_future['tradingsymbol']}")
        ltp = quote[f"{EXCHANGE}:{natural_gas_future['tradingsymbol']}"]["last_price"]
        logging.info(f"LTP of {natural_gas_future['tradingsymbol']} is {ltp}")
    except Exception as e:
        logging.error(f"Failed to get quote for {natural_gas_future['tradingsymbol']}: {e}")
        return

    # --- 6. Find the ATM CE and PE options ---
    # The strike prices for Natural Gas are in multiples of 1.
    atm_strike = round(ltp)
    atm_ce = None
    atm_pe = None

    for instrument in instruments:
        # Match by checking if the option symbol starts with the future series and matches the strike
        if (
            instrument["tradingsymbol"].startswith(future_series)
            and instrument["strike"] == atm_strike
        ):
            if instrument["instrument_type"] == INSTRUMENT_TYPE_CE:
                atm_ce = instrument
            elif instrument["instrument_type"] == INSTRUMENT_TYPE_PE:
                atm_pe = instrument

    if not atm_ce or not atm_pe:
        logging.error(f"Could not find ATM options for series {future_series} and strike {atm_strike}.")
        return

    logging.info(f"Found ATM CE: {atm_ce['tradingsymbol']}")
    logging.info(f"Found ATM PE: {atm_pe['tradingsymbol']}")

    # --- 7. Place orders for the ATM CE and PE ---
    for option in [atm_ce, atm_pe]:
        try:
            order_id = kite.place_order(
                variety=kite.VARIETY_REGULAR,
                exchange=EXCHANGE,
                tradingsymbol=option["tradingsymbol"],
                transaction_type=TRANSACTION_TYPE_BUY,
                quantity=option["lot_size"],
                product=PRODUCT,
                order_type=ORDER_TYPE,
                validity=VALIDITY,
            )
            logging.info(
                f"Successfully placed order for {option['tradingsymbol']}. Order ID: {order_id}"
            )
            # Fetch and display the order status
            order_details = kite.order_history(order_id)[-1]  # Get the latest status
            logging.info(f"  Order Status: {order_details['status']}")
            if order_details.get("status_message"):
                logging.info(f"  Status Message: {order_details['status_message']}")

        except Exception as e:
            logging.error(f"Failed to place order for {option['tradingsymbol']}: {e}")

    # --- 8. Wait for user input to close the window ---
    input("\nPress Enter to close the application...")


if __name__ == "__main__":
    main()