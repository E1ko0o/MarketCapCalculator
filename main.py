def get_current_time_milliseconds():
    import time
    return round(time.time() * 1000)


companies = []


def read_csv_and_fill_data():
    import os
    import re
    root_dir = os.getcwd()
    if os.path.exists('results.csv'):
        os.remove('results.csv')
    regex = re.compile('.*csv$')

    for root, dirs, files in os.walk(root_dir):
        index = 0
        for file in files:
            if regex.match(file):
                with open(file, 'r', encoding='utf8') as f:
                    for line in f:
                        if line.__contains__('Symbol'):
                            continue
                        companies.append([])
                        _, _1, symbol, sector = list(line.split(','))
                        sector = sector.replace('\n', '')
                        companies[index].append(symbol)
                        companies[index].append(sector)
                        index += 1


def read_csv_results():
    # @todo refactor
    index = 0
    with open('results.csv', 'r', encoding='utf8') as f:
        for line in f:
            if line.__contains__('Symbol'):
                continue
            companies.append([])
            symbol, cap, pe, price, sector = list(line.split(','))
            cap = int(cap)
            pe = float(pe.replace('\n', ''))
            companies[index].append(symbol)
            companies[index].append(cap)
            companies[index].append(pe)
            companies[index].append(price)
            companies[index].append(sector)
            del symbol, cap, pe, price, sector
            index += 1


def write_output():
    with open('results.csv', 'w') as f:
        f.write('Symbol,Market Cap,P/E Ratio,'
                'Current/last price in USD,Number of shares,Percentage,Industry-Sector\n')
        for j in range(len(companies)):
            f.write(f'{companies[j][0]},{companies[j][2]},{companies[j][3]},'
                    f'{companies[j][4]},{companies[j][5]},{companies[j][6]},{companies[j][1]}\n')


def sort_by_cap():  # @todo sort by symbol and sector
    companies.sort(key=lambda x: x[2], reverse=True)


def get_data_yf():
    import yfinance as yfl
    j = 0
    while j < len(companies):
        symbol = yfl.Ticker(companies[j][0]).info
        if symbol.keys().__contains__('netIncomeToCommon'):
            if symbol.get('netIncomeToCommon') < 0:  # @todo get out from functions 0 to 'net_income_target' and others
                print('Skip due to negative net income: ' + companies[j][0])
                companies.remove(companies[j])
                continue

        if symbol.keys().__contains__('ebitda') and symbol['ebitda'] is not None:
            if symbol['ebitda'] < 1_000_000_000:  # @todo research
                print('Skip due to low ebitda: ' + companies[j][0])
                companies.remove(companies[j])
                continue

        if symbol.keys().__contains__('priceToBook') and symbol['priceToBook'] is not None:
            if symbol['priceToBook'] > 50:  # @todo research
                print('Skip due to high p/b: ' + companies[j][0])
                companies.remove(companies[j])
                continue

        if symbol.keys().__contains__('totalDebt') and symbol['totalDebt'] is not None:
            if symbol['totalDebt'] > 1_000_000_000_000:  # @todo research
                print('Skip due to high total debt: ' + companies[j][0])
                companies.remove(companies[j])
                continue

        if symbol.keys().__contains__('priceToSalesTrailing12Months') \
                and symbol['priceToSalesTrailing12Months'] is not None:
            if symbol['priceToSalesTrailing12Months'] > 10:
                print('Skip due to high p/s: ' + companies[j][0])
                companies.remove(companies[j])
                continue

        if symbol.keys().__contains__('trailingEps') \
                and symbol['trailingEps'] is not None \
                and symbol.keys().__contains__('forwardEps') \
                and symbol['forwardEps'] is not None:
            if symbol['trailingEps'] < 1 or symbol['forwardEps'] < 1:
                print('Skip due to low eps: ' + companies[j][0])
                companies.remove(companies[j])
                continue

        if symbol.keys().__contains__('returnOnEquity') and symbol['returnOnEquity'] is not None:
            if symbol['returnOnEquity'] < 0.1:
                print('Skip due to low return on equity: ' + companies[j][0])
                companies.remove(companies[j])
                continue

        if symbol.keys().__contains__('returnOnAssets') and symbol['returnOnAssets'] is not None:
            if symbol['returnOnAssets'] < 0.05:
                print('Skip due to low return on assets: ' + companies[j][0])
                companies.remove(companies[j])
                continue

        if symbol.keys().__contains__('marketCap'):
            companies[j].append(symbol['marketCap'])

        if symbol.keys().__contains__('trailingPE'):
            pe = symbol['trailingPE']
            if pe is not None:
                if pe > 30:
                    print('Skip due to high p/e: ' + companies[j][0])
                    companies.remove(companies[j])
                    continue
                companies[j].append(round(pe, 2))
            del pe
        elif symbol.keys().__contains__('forwardPE'):
            pe = symbol['forwardPE']
            if pe is not None:
                if pe > 30:
                    print('Skip due to high p/e: ' + companies[j][0])
                    companies.remove(companies[j])
                    continue
                companies[j].append(round(pe, 2))
            del pe
        else:
            print('Skip due to unavailable p/e: ' + companies[j][0])
            companies.remove(companies[j])
            continue

        if symbol.keys().__contains__('currentPrice'):
            companies[j].append(symbol['currentPrice'])

        print(companies[j])
        j += 1


def count_number_of_shares_using_number_of_companies(amount_in_usd: int):
    percentage = round(1 / len(companies), 5)
    amount_for_company = round(amount_in_usd * percentage, 5)
    for i in range(len(companies)):
        number_of_shares = float(amount_for_company) // float(companies[i][4])
        companies[i].append(int(number_of_shares))
        companies[i].append(percentage)


def count_number_of_shares_using_market_cap(amount_in_usd: int):
    sum_cap = 0
    for i in range(len(companies)):
        sum_cap += companies[i][2]
    for i in range(len(companies)):
        percentage = round((int(companies[i][2]) / sum_cap), 5)
        amount_for_company = round(amount_in_usd * percentage, 5)
        number_of_shares = float(amount_for_company) // float(companies[i][4])
        companies[i].append(int(number_of_shares))
        companies[i].append(percentage)


def update_data():
    read_csv_and_fill_data()
    get_data_yf()
    sort_by_cap()
    # count_number_of_shares_using_market_cap(16000)
    count_number_of_shares_using_number_of_companies(16000)
    write_output()


if __name__ == '__main__':
    start_timer = get_current_time_milliseconds()

    # companies = [['AAPL'], ['GE'], ['XOM'], ['BABA'], ['TSLA'], ['SPCE'], ['GOOG'], ['BRK-B']]
    # get_data_yf()
    # count_number_of_shares_using_number_of_companies(16000)
    # write_output()
    # import yfinance as yfl
    # for j in range(len(companies)):
    #     symbol = yfl.Ticker(companies[j][0]).info
    #     print(symbol)
    # print(companies)

    update_data()
    # read_csv_results()

    end_timer = get_current_time_milliseconds()
    time_of_running = end_timer - start_timer
    print('Time of running in milliseconds: ' + str(time_of_running))
