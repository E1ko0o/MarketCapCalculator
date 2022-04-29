from yahoofinancials import YahooFinancials

symbol_cap_price = [[]]


def read_csv_and_fill_data():
    import os
    import re
    root_dir = os.getcwd()
    regex = re.compile('.*csv$')

    for root, dirs, files in os.walk(root_dir):
        index = 0
        for file in files:
            if regex.match(file):
                with open(file, 'r', encoding='utf8') as f:
                    for line in f:
                        if line.__contains__('price (USD)'):
                            continue
                        symbol_cap_price.append([])
                        _, _1, symbol, cap, price = list(line.split(','))
                        symbol_cap_price[index].append(symbol)
                        symbol_cap_price[index].append(int(cap))
                        symbol_cap_price[index].append(float(price))
                        index += 1


if __name__ == '__main__':
    # companies = ['AAPL', 'MSFT', 'GOOG', 'AMZN', 'TSLA', 'BRK-A']
    # yf = YahooFinancials(companies)
    # print(yf.get_market_cap())
    # print(yf.get_pe_ratio())
    read_csv_and_fill_data()
    print(symbol_cap_price)
