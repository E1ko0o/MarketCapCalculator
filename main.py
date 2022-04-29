import time
from yahoofinancials import YahooFinancials


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
                        if line.__contains__(',Symbol'):
                            continue
                        companies.append([])
                        _, _1, symbol = list(line.split(','))
                        symbol = symbol.replace('\n', '')
                        companies[index].append(symbol)
                        index += 1


def check_pe_ratio(target: float):
    j = 0
    while j < len(companies):
        if companies[j][2] is not None:
            if float(companies[j][2]) > target:
                companies.remove(companies[j])
        else:
            companies[j][2] = 1.0
        j += 1


def write_output():
    # csv to txt
    with open('results.csv', 'w') as f:
        f.write('Symbol,Market Cap,P/E Ratio\n')
        for j in range(len(companies)):
            f.write(f'{companies[j][0]},{companies[j][1]},{companies[j][2]}\n')


def sort_by_cap():
    companies.sort(key=lambda x: x[1], reverse=True)


if __name__ == '__main__':
    start_timer = get_current_time_milliseconds()
    # companies = [['AAPL'], ['TSLA'], ['BRK-B'], ['LI']]
    read_csv_and_fill_data()
    sum_cap = 0
    for i in range(len(companies)):
        print(companies[i][0])
        yf = YahooFinancials(companies[i][0])
        market_cap = yf.get_market_cap()
        pe_ratio = yf.get_pe_ratio()

        companies[i].append(market_cap)
        companies[i].append(pe_ratio)
        print(companies[i])
    sort_by_cap()
    check_pe_ratio(50)
    write_output()
    # print(companies)
    # for i in range(len(companies)):
    #     sum_cap += companies[i][1]
    # for i in range(len(companies)):
    #     print(int(companies[i][1])/sum_cap)
    end_timer = get_current_time_milliseconds()
    time_of_running = end_timer - start_timer
    print('Time of running in milliseconds: ' + str(time_of_running))
