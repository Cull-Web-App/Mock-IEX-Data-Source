import random
from datetime import datetime
from decimal import Decimal

from boto3.dynamodb.conditions import Key

from .aws_service import quoteTable


# Get the next quote from the current quote
def get_next_quote(previous_quote: dict) -> dict:
    random_percent_change_price: Decimal = Decimal(random.uniform(-0.05, 0.05)) # using 5% as max DAILY change for now
    random_percent_change_volume: Decimal = Decimal(random.uniform(-0.02, 0.02)) # assuming that volume changes less than price

    # Calculate the open and close prices using the previous day as a reference
    open_price: Decimal = previous_quote['close']
    close_price: Decimal = previous_quote['close'] * (1 + random_percent_change_price)

    # Now figure out where the highs and lows lie -- random with the 3's but basically there is only the situations where the price
    # increased or decreased for the day that we care about, if they are equal it doesnt matter where the low/highs are as long as they
    # are in the range.
    high_price: Decimal = max(open_price, open_price * (1 + Decimal(random.uniform(0, 0.03)))) if open_price > close_price else max(close_price, close_price * (1 + Decimal(random.uniform(0, 0.03))))
    low_price: Decimal = min(open_price, open_price * (1 + Decimal(random.uniform(-0.03, 0)))) if open_price < close_price else min(close_price, close_price * (1 + Decimal(random.uniform(-0.03, 0))))

    new_date: str = datetime.today().isoformat()

    return {
        **previous_quote,
        'open': open_price,
        'close': close_price,
        'low': low_price,
        'high': high_price,
        'volume': Decimal(previous_quote['volume'] * (1 + random_percent_change_volume)),
        'dateTime': new_date
    }

def get_previous_quote(symbol: str) -> dict:
    # Extract the last quote from the dynamodb quote table for this stage
    print('Attempting to retrieve last record from the quote table for {0}'.format(symbol))

    try:
        return quoteTable.query(
            KeyConditionExpression=Key('symbol').eq(symbol),
            Limit=1, # Get just one entry
            ScanIndexForward=False # This will get item that is at the top in reverse sorted order on the sort key (iso timestamps are sorted like numbers do to their ordering)
        )['Items'][0]
    except Exception as err:
        print('Failed to retrieve last record for {0} with following error'.format(symbol))
        print(err)


def generate_updated_quote(symbol: str) -> dict:
    return get_next_quote(
        previous_quote=get_previous_quote(symbol=symbol)
    )
