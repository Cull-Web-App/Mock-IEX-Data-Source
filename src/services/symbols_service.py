from .aws_service import quoteTable


def get_all_symbols():
    # Simply get all the uniq symbols in the quote table and return them
    print('Attempting to get all unique symbols from the quote table')

    scan_response = quoteTable.scan(ProjectionExpression='symbol')['Items']

    # Get only the uniq symbols from the scan -- not sure if this is the best method...
    # map returns iterators not lists in python!
    return list(
        map(
            lambda symbol: { 'symbol': symbol },
            set(
                map(lambda item: item['symbol'], scan_response)
            )
        )
    )
