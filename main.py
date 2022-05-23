from tkinter import *

# @todo подключаться к мосбирже/аналоги
import os
import time

companies = []
target_net_income = 0
target_pb = 3
target_ps = 10
target_eps = 1
target_roe = 0.1
target_roa = 0.05
target_pe = 30
target_market_cap = 1_000_000_000
coefficient_net_income_divided_total_debt = 0.25

color_green_to_print = '\033[1;92m'
color_red_to_print = '\033[1;91m'
results_file = 'results.csv'


def get_current_time_milliseconds():
    return round(time.time() * 1000)


def read_csv_and_fill_data():
    import re
    root_dir = os.getcwd()
    regex = re.compile('tikers.csv')
    index = 0
    for file in os.listdir(root_dir):
        if os.path.isfile(os.path.join(root_dir, file)) and regex.match(file):
            with open(file, 'r', encoding='utf8') as f:
                for line in f:
                    if line.__contains__('Symbol'):
                        continue
                    companies.append([])
                    _, symbol = list(line.split(','))
                    symbol = symbol.replace('\n', '')
                    companies[index].append(symbol)
                    index += 1


def read_csv_results():
    index = 0
    with open(results_file, 'r', encoding='utf8') as f:
        for line in f:
            if line.__contains__('Symbol'):
                continue
            companies.append([])
            symbol, sector, industry, price, nums = list(line.split(','))
            price = float(price)
            nums = int(nums)
            companies[index].append(symbol) \
                .append(sector) \
                .append(industry) \
                .append(price) \
                .append(nums)
            index += 1


def prepare_output_file():
    with open(results_file, 'w') as f:
        f.write('Symbol,Sector,Industry,Current/last price in USD,Number of stocks\n')


def append_number_of_stocks_output():
    from shutil import copy as sh_copy
    input_f = 'buf.csv'
    sh_copy(results_file, input_f)
    with open(results_file, 'w') as out_file:
        with open(input_f, 'r') as in_file:
            j = 0
            for line in in_file:
                if line.__contains__('Symbol'):
                    out_file.write(line)
                    continue
                s = line.rstrip('\n') + ',' + str(companies[j][4]) + '\n'
                out_file.write(s)
                j += 1
    os.remove('buf.csv')


def append_company_output(company):
    with open(results_file, 'a') as f:
        f.write(f'{company[0]},{company[1]},{company[2]},{company[3]}\n')


def write_full_output():
    with open(results_file, 'w') as f:
        f.write('Symbol,Sector,Industry,Current/last price in USD,Number of stocks\n')
        # Sector include industry
        for j in range(len(companies)):
            f.write(f'{companies[j][0]},{companies[j][1]},{companies[j][2]},'
                    f'{companies[j][3]},{companies[j][4]}\n')


def sort_by_symbol():
    companies.sort(key=lambda x: x[0], reverse=True)


def sort_by_sector():
    companies.sort(key=lambda x: x[1], reverse=False)


def sort_by_industry():
    companies.sort(key=lambda x: x[2], reverse=False)


def get_data_yf():
    from torrequest import TorRequest
    import yahoofinancials as yf
    st = get_current_time_milliseconds()
    aapl = yf.YahooFinancials('AAPL')
    print(aapl.get_market_cap())
    end = get_current_time_milliseconds()
    print(f'Time in milliseconds: {end-st}')

    keys = [
        'IZ97YFC2NES1NJ4Y',
        'UXX87R2JPQH8HJZM',
        'LBN8JWZI6OM0TZ7A',
        'O6SQ1Z4O53LXYDWO',
        '6MSQE0ZTBCZ01KMT',
        'A7PNLK5GFXG284D9',
        'K5OH1H43R79HJJSL',
        'IVRSRHLKLSMT1VQQ',
        'ZI2T9MWM23G38L13',
        'YA5ARUMIEZ6UPF71',
        'LBV1U5G7EKZOF9J0',
        '4WLF89KBDF7855TB',
        'JJMHSYNG7WC91EC2',
        '8E1Q5IQ230LJ5RGU',
        'IUWUM39TIA73TRB9',
        '7ITG8KDEMUOIH0DS',
        'HF4XTKJN2L22PUH4',
        'I383J8XJAHJWU305',
        'DD1A82I4S9SJAVPS',
        'V73SN5D69WWG51NQ',
        'Z8H4JYB6MXTFF5H5',
        '1JMYNQVPYY534GO1',
        'V5OOE342IVF6P93Z',
        'K8LTYQGL5GD71ME0',
        'G2SQTV0D2WLMTLE2',
        'M5OH32NNJ1MUZBZS',
        'SKF1FOX9WW2P38VJ',
        'LSU30R9TFT40GN2L',
        'BZB64VSU8BVS6SC6',
        'DSBH4VZGS7MO5WWM',
        '72RCJTFQC32SBKUL',
        'UG11URMTCZIGMR04',
        'UP1WU4A7A8F08KWO',
        'WE1QO0O7GOU4WDPT',
        'WAU6KYWAUUOWV71O',
        'Q9YHM1HTUAJ5NFXT',
        'DVU5T1JSE3SHP0W4',
        'JM61YITH0V8W8FNV',
        'PGEPDMUWAMATIH6W',
        'L8ZMFDI4GSA6BK70',
        'UW8J2L4QN8UM9B2J',
        'IBYN0HSB8YGGZJEL',
        'ICAMVKHH9TSPWV9P',
        'YJTHGV2ROWV6MU7D',
        '2TDY5MJ7LTCVWREB',
        'B5TA0LAXWJL3K6VY',
        'ETY0IF01ZP16HEFR',
        '5O15SPAKFR3I1RJO',
        'JVFZ7P9UR5MKASVO',
        'O0WC12W3D5CTINF5',
        'USNHHWRRCIMM1BRT',
    ]  # 12/0.3 = 40
    # https://www.alphavantage.co/query?function=OVERVIEW&symbol=IBM&apikey=demo
    # https://www.alphavantage.co/documentation/
    rand = 0
    j = 0
    k = 0
    # while j < len(companies):
    #     tr = TorRequest()
    #     k += 1
    #     if k % 4 == 0:
    #         tr.reset_identity()
    #         tr.ctrl.signal('CLEARDNSCACHE')
    #         print("New Ip Address", tr.get('http://icanhazip.com').text)
    #     function = 'OVERVIEW'
    #     url = f'https://www.alphavantage.co/query?function={function}&symbol={companies[j][0]}' \
    #           f'&interval=1min&apikey={keys[rand]}'
    #     response = tr.get(url)
    #     symbol = response.json()
    #     rand += 1
    #     if rand >= len(keys):
    #         rand = 0
    #
    #     if symbol.__contains__('PriceToSalesRatioTTM'):
    #         if not symbol['PriceToSalesRatioTTM'].__contains__('-'):
    #             if float(symbol['PriceToSalesRatioTTM']) > target_ps:
    #                 print(color_red_to_print + 'Skip due to high P/S: ' + companies[j][0])
    #                 companies.remove(companies[j])
    #                 continue
    #         else:
    #             print(color_red_to_print + 'Skip due to negative P/S: ' + companies[j][0])
    #             companies.remove(companies[j])
    #             continue
    #
    #     if symbol.__contains__('EPS'):
    #         if not symbol['EPS'].__contains__('-'):
    #             if float(symbol['EPS']) < target_eps:
    #                 print(color_red_to_print + 'Skip due to low EPS: ' + companies[j][0])
    #                 companies.remove(companies[j])
    #                 continue
    #         else:
    #             print(color_red_to_print + 'Skip due to negative EPS: ' + companies[j][0])
    #             companies.remove(companies[j])
    #             continue
    #
    #     if symbol.__contains__('ReturnOnEquityTTM') and symbol.__contains__('ReturnOnAssetsTTM'):
    #         if float(symbol['ReturnOnEquityTTM']) < target_roe or float(symbol['ReturnOnAssetsTTM']) < target_roa:
    #             print(color_red_to_print + 'Skip due to low return on equity/assets: ' + companies[j][0])
    #             companies.remove(companies[j])
    #             continue
    #         elif (float(symbol['ReturnOnEquityTTM']) < 2 * target_roe or
    #               float(symbol['ReturnOnAssetsTTM']) < 2 * target_roa) and \
    #                 symbol.__contains__('PriceToBookRatio'):
    #             if float(symbol['PriceToBookRatio']) > target_pb:
    #                 print(color_red_to_print + 'Skip due to high P/B: ' + companies[j][0])
    #                 companies.remove(companies[j])
    #                 continue
    #
    #     if symbol.__contains__('MarketCapitalization'):
    #         if float(symbol['MarketCapitalization']) < target_market_cap:
    #             print(color_red_to_print + 'Skip due to low market cap: ' + companies[j][0])
    #             companies.remove(companies[j])
    #             continue
    #
    #     if symbol.__contains__('PERatio'):
    #         if not symbol['PERatio'].__contains__('-'):
    #             if float(symbol['PERatio']) > target_pe:
    #                 print(color_red_to_print + 'Skip due to high P/E: ' + companies[j][0])
    #                 companies.remove(companies[j])
    #                 continue
    #         else:
    #             print(color_red_to_print + 'Skip due to negative P/E: ' + companies[j][0])
    #             companies.remove(companies[j])
    #             continue
    #
    #     if symbol.__contains__('Sector'):
    #         symbol['Sector'] = symbol['Sector'].strip()
    #         companies[j].append(symbol['Sector'])
    #
    #     if symbol.__contains__('Industry'):
    #         symbol['Industry'] = symbol['Industry'].strip()
    #         companies[j].append(symbol['Industry'])
    #
    #     function = 'TIME_SERIES_INTRADAY'
    #     url = f'https://www.alphavantage.co/query?function={function}&symbol={companies[j][0]}' \
    #           f'&interval=1min&apikey={keys[rand]}'
    #     response = tr.get(url)
    #     symbol = response.json()
    #     rand += 1
    #     if rand >= len(keys):
    #         rand = 0
    #
    #     print(symbol)
    #     companies[j].append(list(list(list(symbol.values())[1].values())[0].values())[3])
    #
    #     print(color_green_to_print + str(companies[j]))
    #     append_company_output(companies[j])
    #     j += 1


def count_number_of_stocks_using_number_of_companies(amount_in_usd: int):
    percentage = round(1 / len(companies), 5)
    amount_for_company = round(amount_in_usd * percentage, 5)
    for i in range(len(companies)):
        number_of_stocks = float(amount_for_company) // float(companies[i][3])
        companies[i].append(int(number_of_stocks))


def update_data():
    read_csv_and_fill_data()
    prepare_output_file()
    get_data_yf()
    # count_number_of_stocks_using_number_of_companies(16000)
    # append_number_of_stocks_output()


if __name__ == '__main__':
    start_timer = get_current_time_milliseconds()
    update_data()
    end_timer = get_current_time_milliseconds()
    time_of_running = end_timer - start_timer
    print(color_green_to_print + 'Time of running in milliseconds: ' + str(time_of_running))
    print(color_green_to_print + 'Time of running in seconds: ' + str(time_of_running / 1000))

# class TkinterTable:
#     def __init__(self, root, rows, columns, data):
#         length_of_columns = []
#         for x in range(columns):
#             m = 0
#             for y in range(rows):
#                 m = max(m, len(str(data[y][x])))
#             length_of_columns.append(m)
#         for x in range(rows):
#             for y in range(columns):
#                 self.e = Entry(master=root, width=length_of_columns[y], fg='black', font=('Arial', 11, 'normal'))
#                 self.e.grid(row=x, column=y)
#                 self.e.insert(END, data[x][y])
#                 self.e.config(state='readonly')
#
#     def add_entry(self, root, entry):
#         # @TODO make x and y global in grid
#         pass
#
#
# def on_focus_in(entry):
#     if entry.cget('state') == 'disabled':
#         entry.configure(state='normal')
#         entry.delete(0, 'end')
#
#
# def on_focus_out(entry, placeholder_inner):
#     if entry.get() == "":
#         entry.insert(0, placeholder_inner)
#         entry.configure(state='disabled')
#
#
# def create_label(master, text, row, column):
#     label = Label(master=master, text=text)
#     label.grid(row=row, column=column)
#
#
# def create_radiobuttons(master, row, column):
#     # @todo check
#     var = StringVar()
#     less_rb = Radiobutton(master=master, text=less_text, value=less_text, variable=var)
#     less_rb.select()
#     less_rb.grid(row=row, column=column)
#     more_rb = Radiobutton(master=master, text=more_than_text, value=more_than_text, variable=var)
#     more_rb.grid(row=row, column=column + 1)
#     return var
#
#
# def create_entry(master, row, column):
#     entry = Entry(master=master)
#     entry.grid(row=row, column=column)
#     entry.insert(0, placeholder)
#     entry.configure(state='disabled')
#     entry.bind('<Button-1>', lambda x: on_focus_in(entry))
#     entry.bind('<FocusOut>', lambda x: on_focus_out(entry, placeholder))
#     return entry
#
#
# def create_filter(master, filter_text):
#     global counter_row, counter_column
#     create_label(master, filter_text, counter_row, counter_column)
#     counter_column += 1
#
#     rb = create_radiobuttons(master, counter_row, counter_column)
#     counter_column += 2
#
#     e = create_entry(master, counter_row, counter_column)
#     counter_row += 1
#     counter_column = 0
#     return rb, e
#
#
# def print_data(event):
#     global rb_pe, pe
#     print(rb_pe.get())
#     print(pe.get())
#
#
# placeholder = 'Input a number'
# less_text = 'less'
# more_than_text = 'more than'
#
# window = Tk()
# window.title('Market stocks calculator')
# window.minsize(400, 250)
# window.maxsize(2880, 1620)
# window.iconphoto(False, PhotoImage(file='logo.png'))
#
# frame_results = Frame()
# label_results = Label(master=frame_results, text='Results')
# # @todo replace with actual data
# d = [['Symbol', 'Sector', 'Industry', 'Current/last price in USD', 'Number of stocks'],
#      ['TSM', 'Technology', 'Semiconductors', 90.53, 3],
#      ['COIN', 'Technology', 'Software Application', 63.03, 4],
#      ['AAPL', 'Technology', 'Consumer Electronics', 140.82, 2]]
# t = TkinterTable(frame_results, len(d), len(d[0]), d)
#
# frame_settings = Frame()
# counter_row = 0
# counter_column = 0
#
# rb_pe, pe = create_filter(frame_settings, 'P/E:')
# rb_ps, ps = create_filter(frame_settings, 'P/S:')
# rb_pb, pb = create_filter(frame_settings, 'P/B:')
# rb_eps, eps = create_filter(frame_settings, 'EPS:')
# rb_ebitda, ebitda = create_filter(frame_settings, 'EBITDA:')
# rb_debt, debt = create_filter(frame_settings, 'Total debt:')
# rb_coefficient, coefficient = create_filter(frame_settings, 'Coefficient net income/total debt:')
# rb_roe, roe = create_filter(frame_settings, 'ROE:')
# rb_roa, roa = create_filter(frame_settings, 'ROA:')
# rb_cap, cap = create_filter(frame_settings, 'Market capitalization:')
#
# btn_confirm = Button(master=frame_settings, text='Confirm')
# btn_confirm.grid(row=counter_row, column=counter_column)
# btn_confirm.bind('<Button-1>', print_data)
#
# frame_results.grid(row=0, column=0)
# frame_settings.grid(row=0, column=1)
# window.state('zoomed')
# window.mainloop()
