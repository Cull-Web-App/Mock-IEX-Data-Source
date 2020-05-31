from . import aws_service


def get_all_symbols():
    # Simply get all the uniq symbols in the symbols table and return them
    print('Attempting to get all unique symbols from the symbol table')

    # Bascially just return the entire symbols table to the user
    return aws_service.symbolsTable.scan()['Items']
