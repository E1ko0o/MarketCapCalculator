import time


def get_current_time_milliseconds():
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
        f.write('Symbol,Market Cap,P/E Ratio,Current/last price in USD,Number of stocks,Industry-Sector\n')
        for j in range(len(companies)):
            f.write(f'{companies[j][0]},{companies[j][2]},{companies[j][3]},'
                    f'{companies[j][4]},{companies[j][5]},{companies[j][1]}\n')


def sort_by_cap():
    companies.sort(key=lambda x: x[2], reverse=True)


def get_data_yf():
    import yfinance as yfl
    j = 0
    while j < len(companies):
        symbol = yfl.Ticker(companies[j][0]).info
        if symbol.keys().__contains__('netIncomeToCommon'):
            if symbol.get('netIncomeToCommon') < 0:
                print('Skip due to negative net income: ' + companies[j][0])
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

        if symbol.keys().__contains__('ebitda') and symbol['ebitda'] is not None:
            if symbol['ebitda'] < 1_000_000_000:
                print('Skip due to low ebitda: ' + companies[j][0])
                companies.remove(companies[j])
                continue

        if symbol.keys().__contains__('totalDebt') and symbol['totalDebt'] is not None:
            if symbol['totalDebt'] > 1_000_000_000_000:  # decrease
                print('Skip due to high total debt: ' + companies[j][0])
                companies.remove(companies[j])
                continue

        if symbol.keys().__contains__('trailingPegRatio') and symbol['trailingPegRatio'] is not None:
            if symbol['trailingPegRatio'] > 4:
                print('Skip due to high peg ratio: ' + companies[j][0])
                companies.remove(companies[j])
                continue

        if symbol.keys().__contains__('returnOnEquity') and symbol['returnOnEquity'] is not None:
            if symbol['returnOnEquity'] < 0.1:  # 0.08
                print('Skip due to low return on equity: ' + companies[j][0])
                companies.remove(companies[j])
                continue

        if symbol.keys().__contains__('returnOnAssets') and symbol['returnOnAssets'] is not None:
            if symbol['returnOnAssets'] < 0.05:  # 0.04
                print('Skip due to low return on assets: ' + companies[j][0])
                companies.remove(companies[j])
                continue

        # @todo update function get_data_yf
        # netIncomeToCommon
        # marketCap
        # currentPrice
        # ebitda
        # totalDebt
        # trailingPegRatio
        # returnOnEquity
        # returnOnAssets

        # from yahoofinancials import YahooFinancials
        # yf = YahooFinancials(companies[j][0])

        # net_income = yf.get_net_income()
        # if net_income < 0:
        #     print('Skip and remove: ' + companies[j][0])
        #     companies.remove(companies[j])
        #     continue

        # market_cap = yf.get_market_cap()
        # if market_cap is not None:
        #     companies[j].append(market_cap)
        # else:
        #     companies[j].append(0)

        # pe_ratio = yf.get_pe_ratio()
        # if pe_ratio is not None:
        #     companies[j].append(round(pe_ratio, 2))
        # else:
        #     import yfinance as yfl
        #     symbol = yfl.Ticker(companies[j][0]).info
        #     if symbol.keys().__contains__('trailingPE'):
        #         trailing_pe = symbol["trailingPE"]
        #         if trailing_pe is not None:
        #             companies[j].append(round(trailing_pe, 2))
        #     else:
        #         forward_pe = symbol["forwardPE"]
        #         companies[j].append(round(forward_pe, 2))

        # price = yf.get_current_price()
        # if price is not None:
        #     companies[j].append(round(price, 2))
        # else:
        #     companies[j].append(0)
        print(companies[j])
        j += 1


def count_number_of_stocks(amount_in_usd: int):
    sum_cap = 0
    for i in range(len(companies)):
        sum_cap += companies[i][2]
    for i in range(len(companies)):
        percentage = round((int(companies[i][2]) / sum_cap), 5)
        amount_for_company = round(amount_in_usd * percentage, 5)
        number_of_stocks = float(amount_for_company) // float(companies[i][4])
        companies[i].append(int(number_of_stocks))


def update_data():
    read_csv_and_fill_data()
    get_data_yf()
    sort_by_cap()
    count_number_of_stocks(15000)
    write_output()


if __name__ == '__main__':
    start_timer = get_current_time_milliseconds()

    # companies = [['AAPL'], ['GE'], ['XOM']]
    # import yfinance as yfl
    # for j in range(len(companies)):
    #     symbol = yfl.Ticker(companies[j][0]).info
    #     print(symbol)
    #     if symbol.keys().__contains__('trailingPE'):
    #         trailing_pe = symbol["trailingPE"]
    #         if trailing_pe is not None:
    #             companies[j].append(round(trailing_pe, 2))
    #     else:
    #         forward_pe = symbol["forwardPE"]
    #         companies[j].append(round(forward_pe, 2))
    # get_data_yf()
    # count_number_of_stocks(10000)
    # print(companies)

    update_data()
    # read_csv_results()

    end_timer = get_current_time_milliseconds()
    time_of_running = end_timer - start_timer
    print('Time of running in milliseconds: ' + str(time_of_running))
