import simplejson as json

from .services import quote_generation_service, symbols_service


def symbols(event, context):
    print('Retrieving all the symbols')

    return {
        "statusCode": 200,
        'headers': {
            'Content-Type': 'application/json',
        },
        "body": json.dumps(symbols_service.get_all_symbols())
    }


def quote(event, context):
    print(event)

    # Extract the quote from the path parameter -- should be on the event
    symbol = event['pathParameters']['symbol']

    updated_quote = quote_generation_service.generate_updated_quote(symbol=symbol)

    print('New quote is ' + str(updated_quote))

    return {
        "statusCode": 200,
        'headers': {
            'Content-Type': 'application/json',
        },
        "body": json.dumps({
            **updated_quote
        })
    }
