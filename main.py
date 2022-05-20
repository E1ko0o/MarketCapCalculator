from tkinter import *


# import os
#
#
# def get_current_time_milliseconds():
#     import time
#     return round(time.time() * 1000)
#
#
# companies = []
# target_net_income = 0
# target_pb = 3
# target_ps = 10
# target_eps = 1
# target_roe = 0.1
# target_roa = 0.05
# target_pe = 30
# target_market_cap = 1_000_000_000
# coefficient_net_income_divided_total_debt = 0.25
#
# color_green_to_print = '\033[1;92m'
# color_red_to_print = '\033[1;91m'
# results_file = 'results.csv'
#
#
# def read_csv_and_fill_data():
#     import re
#     root_dir = os.getcwd()
#     regex = re.compile('tikers.csv')
#     index = 0
#     for file in os.listdir(root_dir):
#         if os.path.isfile(os.path.join(root_dir, file)) and regex.match(file):
#             with open(file, 'r', encoding='utf8') as f:
#                 for line in f:
#                     if line.__contains__('Symbol'):
#                         continue
#                     companies.append([])
#                     _, symbol = list(line.split(','))
#                     symbol = symbol.replace('\n', '')
#                     companies[index].append(symbol)
#                     index += 1
#
#
# def read_csv_results():
#     index = 0
#     with open(results_file, 'r', encoding='utf8') as f:
#         for line in f:
#             if line.__contains__('Symbol'):
#                 continue
#             companies.append([])
#             symbol, sector, industry, price, nums = list(line.split(','))
#             price = float(price)
#             nums = int(nums)
#             companies[index].append(symbol) \
#                 .append(sector) \
#                 .append(industry) \
#                 .append(price) \
#                 .append(nums)
#             index += 1
#
#
# def prepare_output_file():
#     with open(results_file, 'w') as f:
#         f.write('Symbol,Sector,Industry,Current/last price in USD,Number of stocks\n')
#
#
# def append_number_of_stocks_output():
#     from shutil import copy as sh_copy
#     input_f = 'buf.csv'
#     sh_copy(results_file, input_f)
#     with open(results_file, 'w') as out_file:
#         with open(input_f, 'r') as in_file:
#             j = 0
#             for line in in_file:
#                 if line.__contains__('Symbol'):
#                     out_file.write(line)
#                     continue
#                 s = line.rstrip('\n') + ',' + str(companies[j][4]) + '\n'
#                 out_file.write(s)
#                 j += 1
#     os.remove('buf.csv')
#
#
# def append_company_output(company):
#     with open(results_file, 'a') as f:
#         f.write(f'{company[0]},{company[1]},{company[2]},{company[3]}\n')
#
#
# def write_full_output():
#     with open(results_file, 'w') as f:
#         f.write('Symbol,Sector,Industry,Current/last price in USD,Number of stocks\n')
#         # Sector include industry
#         for j in range(len(companies)):
#             f.write(f'{companies[j][0]},{companies[j][1]},{companies[j][2]},'
#                     f'{companies[j][3]},{companies[j][4]}\n')
#
#
# def sort_by_symbol():
#     companies.sort(key=lambda x: x[0], reverse=True)
#
#
# def sort_by_sector():
#     companies.sort(key=lambda x: x[1], reverse=False)
#
#
# def sort_by_industry():
#     companies.sort(key=lambda x: x[2], reverse=False)
#
#
# def get_data_yf():
#     import yfinance as yfl
#     j = 0
#     while j < len(companies):
#         symbol = yfl.Ticker(companies[j][0]).info
#         if symbol.keys().__contains__('netIncomeToCommon'):
#             if symbol['netIncomeToCommon'] < target_net_income:
#                 print(color_red_to_print + 'Skip due to negative net income: ' + companies[j][0])
#                 companies.remove(companies[j])
#                 continue
#
#         if symbol.keys().__contains__('totalDebt'):
#             if symbol['totalDebt'] is not None and symbol['totalDebt'] != 0:
#                 if symbol['netIncomeToCommon'] / symbol['totalDebt'] < coefficient_net_income_divided_total_debt:
#                     print(color_red_to_print + 'Skip due to low coefficient net income/total debt: ' + companies[j][0])
#                     companies.remove(companies[j])
#                     continue
#             elif symbol['totalDebt'] is not None and symbol['totalDebt'] == 0:
#                 print(color_red_to_print + 'Skip due to unavailable total debt: ' + companies[j][0])
#                 companies.remove(companies[j])
#                 continue
#
#         if symbol.keys().__contains__('priceToSalesTrailing12Months') \
#                 and symbol['priceToSalesTrailing12Months'] is not None:
#             if symbol['priceToSalesTrailing12Months'] > target_ps:
#                 print(color_red_to_print + 'Skip due to high p/s: ' + companies[j][0])
#                 companies.remove(companies[j])
#                 continue
#
#         if symbol.keys().__contains__('trailingEps') \
#                 and symbol['trailingEps'] is not None \
#                 and symbol.keys().__contains__('forwardEps') \
#                 and symbol['forwardEps'] is not None:
#             if symbol['trailingEps'] < 1 or symbol['forwardEps'] < target_eps:
#                 print(color_red_to_print + 'Skip due to low eps: ' + companies[j][0])
#                 companies.remove(companies[j])
#                 continue
#
#         if symbol.keys().__contains__('returnOnEquity') and symbol['returnOnEquity'] is not None and \
#                 symbol.keys().__contains__('returnOnAssets') and symbol['returnOnAssets'] is not None:
#             if symbol['returnOnEquity'] < target_roe or symbol['returnOnAssets'] < target_roa:
#                 print(color_red_to_print + 'Skip due to low return on equity/assets: ' + companies[j][0])
#                 companies.remove(companies[j])
#                 continue
#             elif (symbol['returnOnEquity'] < 2 * target_roe or symbol['returnOnAssets'] < 2 * target_roa) and \
#                     symbol.keys().__contains__('priceToBook') and symbol['priceToBook'] is not None:
#                 if symbol['priceToBook'] > target_pb:
#                     print(color_red_to_print + 'Skip due to high p/b: ' + companies[j][0])
#                     companies.remove(companies[j])
#                     continue
#
#         if symbol.keys().__contains__('marketCap') and symbol['marketCap'] is not None:
#             if symbol['marketCap'] < target_market_cap:
#                 print(color_red_to_print + 'Skip due to low market cap: ' + companies[j][0])
#                 companies.remove(companies[j])
#                 continue
#
#         if symbol.keys().__contains__('trailingPE') and symbol['trailingPE'] is not None:
#             if symbol['trailingPE'] > target_pe:
#                 print(color_red_to_print + 'Skip due to high p/e: ' + companies[j][0])
#                 companies.remove(companies[j])
#                 continue
#         elif symbol.keys().__contains__('forwardPE') and symbol['forwardPE'] is not None:
#             if symbol['forwardPE'] > target_pe:
#                 print(color_red_to_print + 'Skip due to high p/e: ' + companies[j][0])
#                 companies.remove(companies[j])
#                 continue
#         else:
#             print(color_red_to_print + 'Skip due to unavailable p/e: ' + companies[j][0])
#             companies.remove(companies[j])
#             continue
#
#         if symbol.keys().__contains__('sector'):
#             symbol['sector'] = symbol['sector'].replace(',', '')
#             symbol['sector'] = symbol['sector'].replace('-', ' ')
#             symbol['sector'] = symbol['sector'].replace('—', ' ').strip()
#             companies[j].append(symbol['sector'])
#
#         if symbol.keys().__contains__('industry'):
#             symbol['industry'] = symbol['industry'].replace(',', '')
#             symbol['industry'] = symbol['industry'].replace('-', ' ')
#             symbol['industry'] = symbol['industry'].replace('—', ' ')
#             symbol['industry'] = symbol['industry'].replace(symbol['sector'], '').strip()
#             companies[j].append(symbol['industry'])
#
#         if symbol.keys().__contains__('currentPrice'):
#             companies[j].append(symbol['currentPrice'])
#
#         print(color_green_to_print + str(companies[j]))
#         append_company_output(companies[j])
#         j += 1
#
#
# def count_number_of_stocks_using_number_of_companies(amount_in_usd: int):
#     percentage = round(1 / len(companies), 5)
#     amount_for_company = round(amount_in_usd * percentage, 5)
#     for i in range(len(companies)):
#         number_of_stocks = float(amount_for_company) // float(companies[i][3])
#         companies[i].append(int(number_of_stocks))
#
#
# def update_data():
#     read_csv_and_fill_data()
#     prepare_output_file()
#     get_data_yf()
#     count_number_of_stocks_using_number_of_companies(16000)
#     append_number_of_stocks_output()
#
#
# if __name__ == '__main__':
#     start_timer = get_current_time_milliseconds()
#     # update_data()
#     end_timer = get_current_time_milliseconds()
#     time_of_running = end_timer - start_timer
#     print(color_green_to_print + 'Time of running in milliseconds: ' + str(time_of_running))
#     print(color_green_to_print + 'Time of running in seconds: ' + str(time_of_running / 1000))


class TkinterTable:
    def __init__(self, root, rows, columns, data):
        length_of_columns = []
        for x in range(columns):
            m = 0
            for y in range(rows):
                m = max(m, len(str(data[y][x])))
            length_of_columns.append(m)
        for x in range(rows):
            for y in range(columns):
                self.e = Entry(master=root, width=length_of_columns[y], fg='black', font=('Arial', 11, 'normal'))
                self.e.grid(row=x, column=y)
                self.e.insert(END, data[x][y])
                self.e.config(state='readonly')

    def add_entry(self, root, entry):
        # @TODO make x and y global in grid
        pass


def on_focus_in(entry):
    if entry.cget('state') == 'disabled':
        entry.configure(state='normal')
        entry.delete(0, 'end')


def on_focus_out(entry, placeholder_inner):
    if entry.get() == "":
        entry.insert(0, placeholder_inner)
        entry.configure(state='disabled')


def create_label(master, text, row, column):
    label = Label(master=master, text=text)
    label.grid(row=row, column=column)


def create_radiobuttons(master, row, column):
    # @todo check
    var = StringVar()
    less_rb = Radiobutton(master=master, text=less_text, value=less_text, variable=var)
    less_rb.select()
    less_rb.grid(row=row, column=column)
    more_rb = Radiobutton(master=master, text=more_than_text, value=more_than_text, variable=var)
    more_rb.grid(row=row, column=column + 1)
    return var


def create_entry(master, row, column):
    entry = Entry(master=master)
    entry.grid(row=row, column=column)
    entry.insert(0, placeholder)
    entry.configure(state='disabled')
    entry.bind('<Button-1>', lambda x: on_focus_in(entry))
    entry.bind('<FocusOut>', lambda x: on_focus_out(entry, placeholder))
    return entry


def create_filter(master, filter_text):
    global counter_row, counter_column
    create_label(master, filter_text, counter_row, counter_column)
    counter_column += 1

    rb = create_radiobuttons(master, counter_row, counter_column)
    counter_column += 2

    e = create_entry(master, counter_row, counter_column)
    counter_row += 1
    counter_column = 0
    return rb, e


def print_data(event):
    global rb_pe, pe
    print(rb_pe.get())
    print(pe.get())


placeholder = 'Input a number'
less_text = 'less'
more_than_text = 'more than'

window = Tk()
window.title('Market stocks calculator')
window.minsize(400, 250)
window.maxsize(2880, 1620)
window.iconphoto(False, PhotoImage(file='logo.png'))

frame_results = Frame()
label_results = Label(master=frame_results, text='Results')
# @todo replace with actual data
d = [['Symbol', 'Sector', 'Industry', 'Current/last price in USD', 'Number of stocks'],
     ['TSM', 'Technology', 'Semiconductors', 90.53, 3],
     ['COIN', 'Technology', 'Software Application', 63.03, 4],
     ['AAPL', 'Technology', 'Consumer Electronics', 140.82, 2]]
t = TkinterTable(frame_results, len(d), len(d[0]), d)

frame_settings = Frame()
counter_row = 0
counter_column = 0

rb_pe, pe = create_filter(frame_settings, 'P/E:')
rb_ps, ps = create_filter(frame_settings, 'P/S:')
rb_pb, pb = create_filter(frame_settings, 'P/B:')
rb_eps, eps = create_filter(frame_settings, 'EPS:')
rb_ebitda, ebitda = create_filter(frame_settings, 'EBITDA:')
rb_debt, debt = create_filter(frame_settings, 'Total debt:')
rb_coefficient, coefficient = create_filter(frame_settings, 'Coefficient net income/total debt:')
rb_roe, roe = create_filter(frame_settings, 'ROE:')
rb_roa, roa = create_filter(frame_settings, 'ROA:')
rb_cap, cap = create_filter(frame_settings, 'Market capitalization:')

btn_confirm = Button(master=frame_settings, text='Confirm')
btn_confirm.grid(row=counter_row, column=counter_column)
btn_confirm.bind('<Button-1>', print_data)

frame_results.grid(row=0, column=0)
frame_settings.grid(row=0, column=1)
window.state('zoomed')
window.mainloop()
