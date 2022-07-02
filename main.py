import os
import time
from tkinter.ttk import Combobox
from tkinter import Label, Entry, Button, Radiobutton, StringVar, PhotoImage, LEFT, Frame, messagebox, Tk

from utils_ui import Table

companies = []
results_file = 'results.csv'
symbols_file = 'symbols.csv'
all_data_file = 'all_data.txt'

# Filters
target_pe = 30
sign_pe = '<'  # less is better
target_ps = 10
sign_ps = '<'  # less is better
target_eps = 1
sign_eps = '>'  # more is better
target_ebitda = 10_000_000
sign_ebitda = '>'  # more is better
target_rps = 1
sign_rps = '>'  # more is better
target_roe = 0.1
sign_roe = '>'  # more is better
target_roa = 0.05
sign_roa = '>'  # more is better
target_pb = 3
sign_pb = '<'  # less is better
target_market_cap = 1_000_000_000
sign_market_cap = '>'  # more is better

target_payout_ratio = 0
sign_payout_ratio = '>'  # more is better
target_dividend_yield = 0
sign_dividend_yield = '>'  # more is better
target_operating_cashflow = 0
sign_operating_cashflow = '>'  # more is better
target_free_cashflow = 0
sign_free_cashflow = '>'  # more is better
target_quick_ratio = 0
sign_quick_ratio = '>'  # more is better
# summaryDetail(payoutRatio, dividendYield)
# financialData(operatingCashflow, freeCashflow, quickRatio)

# Colors for print
color_green_to_print = '\033[1;92m'
color_red_to_print = '\033[1;91m'

# For ui
placeholder = 'Input a number'
less_text = 'less'
more_than_text = 'more than'
ascending_text = 'Ascending'
descending_text = 'Descending'
global_x = 0
global_width = []
default_columns = ['№', 'Symbol', 'Sector', 'Industry', 'Current/last price in USD', 'Number of stocks']


def on_focus_in(entry):
    if entry.cget('state') == 'disabled':
        entry.configure(state='normal')
        entry.delete(0, 'end')


def on_focus_out(entry, placeholder_inner):
    if entry.get() == "":
        entry.insert(0, placeholder_inner)
        entry.configure(state='disabled')


def create_label(master, text, row, column, columnspan=None):
    label = Label(master=master, text=text)
    if columnspan is None:
        label.grid(row=row, column=column, sticky='w')
    else:
        label.grid(row=row, column=column, columnspan=columnspan, sticky='w')


def create_radio_buttons(master, row, column):
    var = StringVar()
    less_rb = Radiobutton(master=master, text=less_text, value=less_text, variable=var)
    less_rb.select()
    less_rb.grid(row=row, column=column, sticky='w')
    more_rb = Radiobutton(master=master, text=more_than_text, value=more_than_text, variable=var)
    more_rb.grid(row=row, column=column + 1, sticky='w')
    return var


def create_entry(master, row, column, columnspan=None):
    entry = Entry(master=master)
    if columnspan is None:
        entry.grid(row=row, column=column, sticky='w')
    else:
        entry.grid(row=row, column=column, columnspan=columnspan, sticky='w')
    entry.insert(0, placeholder)
    entry.configure(state='disabled')
    entry.bind('<Button-1>', lambda x_: on_focus_in(entry))
    entry.bind('<FocusOut>', lambda x_: on_focus_out(entry, placeholder))
    return entry


def create_filter(master, filter_text):
    global counter_row, counter_column
    create_label(master, filter_text, counter_row, counter_column)
    counter_column += 1

    rb = create_radio_buttons(master, counter_row, counter_column)
    counter_column += 2

    e = create_entry(master, counter_row, counter_column)
    counter_row += 1
    counter_column = 0
    return rb, e


def create_calculate_part_of_ui(master):
    global counter_row, counter_column
    create_label(master, 'Calculate number of stocks for $', counter_row, counter_column, 3)
    counter_column += 3

    e = create_entry(master, counter_row, counter_column, 2)
    counter_row += 1
    counter_column = 0
    return e


def get_current_time_milliseconds():
    return round(time.time() * 1000)


def read_csv_symbols():
    index = 0
    with open(symbols_file, 'r') as f:
        for line in f:
            if line.__contains__('Symbol') or line.strip().__eq__(''):
                continue
            companies.append([])
            _, symbol = list(line.split(','))
            symbol = symbol.replace('\n', '')
            companies[index].append(symbol)
            index += 1


def read_csv_results():
    index = 0
    with open(results_file, 'r') as f:
        for line in f:
            companies.append([])
            num, symbol, sector, industry, price, nums = list(line.split(','))
            if line.__contains__('Symbol'):
                companies[index].append(num)
                companies[index].append(symbol)
                companies[index].append(sector)
                companies[index].append(industry)
                companies[index].append(price)
                companies[index].append(nums)
            else:
                companies[index].append(int(num))
                companies[index].append(symbol)
                companies[index].append(sector)
                companies[index].append(industry)
                companies[index].append(float(price))
                companies[index].append(int(nums))
            index += 1


def prepare_output_file():
    with open(results_file, 'w') as f:
        f.write('№,Symbol,Sector,Industry,Current/last price in USD,Number of stocks\n')


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
        f.write(f'{company[0]},{company[1]},{company[2]},{company[3]},{company[4]}\n')


def write_full_output():
    with open(results_file, 'w') as f:
        f.write('№,Symbol,Sector,Industry,Current/last price in USD,Number of stocks\n')
        # Sector include industry
        for j in range(len(companies)):
            f.write(f'{companies[j][0]},{companies[j][1]},{companies[j][2]},'
                    f'{companies[j][3]},{companies[j][4]},{companies[j][5]}\n')


def sort(event):
    global var_sort
    if var_sort.get() == ascending_text:
        reverse = False
    else:
        reverse = True
    if combobox.get() == default_columns[0]:
        companies.sort(key=lambda x: x[0], reverse=reverse)
    elif combobox.get() == default_columns[1]:
        companies.sort(key=lambda x: x[1], reverse=reverse)
    elif combobox.get() == default_columns[2]:
        companies.sort(key=lambda x: x[2], reverse=reverse)
    elif combobox.get() == default_columns[3]:
        companies.sort(key=lambda x: x[3], reverse=reverse)
    elif combobox.get() == default_columns[4]:
        companies.sort(key=lambda x: x[4], reverse=reverse)
    else:
        companies.sort(key=lambda x: x[5], reverse=reverse)
    table.clear()
    table.set_data(companies)


def alert(title, message):
    show_method = getattr(messagebox, 'show{}'.format('info'))
    show_method(title, message)


def check_roe_roa_pb(data):
    # financialData - returnOnEquity, returnOnAssets - raw
    symbol = data['quoteType']['symbol']
    try:
        if sign_roe == '<':
            if float(data['financialData']['returnOnEquity']['raw']) > target_roe:
                print(color_red_to_print + 'Skip due to high return on equity: ' + symbol)
                return True
        else:
            if float(data['financialData']['returnOnEquity']['raw']) < target_roe:
                print(color_red_to_print + 'Skip due to low return on equity: ' + symbol)
                return True
        if sign_roa == '<':
            if float(data['financialData']['returnOnAssets']['raw']) > target_roa:
                print(color_red_to_print + 'Skip due to high return on assets: ' + symbol)
                return True
        else:
            if float(data['financialData']['returnOnAssets']['raw']) < target_roa:
                print(color_red_to_print + 'Skip due to low return on assets: ' + symbol)
                return True
        if sign_roe == '>' and sign_roa == '>':
            if (float(data['financialData']['returnOnEquity']['raw']) < 2 * target_roe or
                    float(data['financialData']['returnOnAssets']['raw']) < 2 * target_roa):
                # defaultKeyStatistics - priceToBook - raw
                if sign_pb == '>':
                    if float(data['defaultKeyStatistics']['priceToBook']['raw']) < target_pb:
                        print(color_red_to_print + 'Skip due to low P/B: ' + symbol)
                        return True
                else:
                    if float(data['defaultKeyStatistics']['priceToBook']['raw']) > target_pb:
                        print(color_red_to_print + 'Skip due to high P/B: ' + symbol)
                        return True
        else:
            print(color_red_to_print + 'P/B should be considered only if ROE and ROA'
                                       ' are searched with a less than sign (<): ' + symbol)
            return True
    except KeyError:
        print(color_red_to_print + 'Skip due to unavailable ROE or ROA or P/B: ' + symbol)
        return True
    return False


def check_raw(data, param1, param2, subject, target, sign):
    symbol = data['quoteType']['symbol']
    try:
        if not str(data[param1][param2]).__contains__('-'):
            if sign == '<':
                if float(data[param1][param2]['raw']) > target:
                    print(color_red_to_print + f'Skip due to high {subject}: ' + symbol)
                    return True
            else:
                if float(data[param1][param2]['raw']) < target:
                    print(color_red_to_print + f'Skip due to low {subject}: ' + symbol)
                    return True
        else:
            print(color_red_to_print + f'Skip due to negative {subject}: ' + symbol)
            return True
    except KeyError:
        print(color_red_to_print + f'Skip due to unavailable {subject}: ' + symbol)
        return True
    return False


def get_data_file():
    global companies
    companies = []
    data_to_function = []
    with open(all_data_file, 'r') as f:
        for line in f:
            data_to_function.append(line)
    get_data_requests(data_to_function)


def get_data_requests(data_outer=None):
    import requests
    import json
    global table, window, companies, e_calculate
    j = 0
    i = 1
    try:
        int(e_calculate.get())
    except ValueError:
        alert('Error!', 'You should type an integer number of $.')
        return
    table.clear()
    if table.number_of_rows != 0:
        r = table.number_of_rows
        while r > 0:
            table.delete_row(r)
            r -= 1
    if data_outer is None:
        url = "https://yh-finance.p.rapidapi.com/stock/v2/get-summary"
        headers = {
            "X-RapidAPI-Host": "yh-finance.p.rapidapi.com",
            "X-RapidAPI-Key": "c14ba60263msh1d75ac31f7bbeeap1f679ejsn684e4f6dccb8"
        }
        # "X-RapidAPI-Key": "f761bc90aemsh14894d87cb4757ap1851d5jsn8e91db991e16" = 0
        # https://smailpro.com/advanced
        while j < len(companies):
            querystring = {"symbol": f'{companies[j][1]}'}
            symbol = requests.request("GET", url, headers=headers, params=querystring)
            data = json.loads(symbol.text)
            with open('all_data.txt', 'a', encoding='utf8') as f:
                f.write(symbol.text + '\n')
            # summaryDetail - priceToSalesTrailing12Months - raw
            # defaultKeyStatistics - trailingEps - raw
            # price - marketCap - raw
            # defaultKeyStatistics - forwardPE - raw
            # financialData - ebitda - raw
            # financialData - revenuePerShare - raw
            if check_raw(data, 'summaryDetail', 'priceToSalesTrailing12Months', 'P/S', target_ps, sign_ps) \
                    or check_raw(data, 'price', 'marketCap', 'market cap', target_market_cap, sign_market_cap) \
                    or check_raw(data, 'defaultKeyStatistics', 'trailingEps', 'EPS', target_eps, sign_eps) \
                    or check_raw(data, 'defaultKeyStatistics', 'forwardPE', 'P/E', target_pe, sign_pe) \
                    or check_raw(data, 'financialData', 'ebitda', 'EBITDA', target_ebitda, sign_ebitda) \
                    or check_raw(data, 'financialData', 'revenuePerShare', 'RPS', target_rps, sign_rps) \
                    or check_raw(data, 'summaryDetail', 'payoutRatio', 'Payout ratio', target_payout_ratio, sign_payout_ratio) \
                    or check_raw(data, 'summaryDetail', 'dividendYield', 'Dividend yield', target_dividend_yield, sign_dividend_yield) \
                    or check_raw(data, 'financialData', 'operatingCashflow', 'Operating Cashflow', target_operating_cashflow, sign_operating_cashflow) \
                    or check_raw(data, 'financialData', 'freeCashflow', 'Free Cashflow', target_free_cashflow, sign_free_cashflow) \
                    or check_raw(data, 'financialData', 'quickRatio', 'Quick Ratio', target_quick_ratio, sign_quick_ratio):
                companies.remove(companies[j])
                continue

            # financialData - returnOnEquity, returnOnAssets - raw
            if check_roe_roa_pb(data):
                companies.remove(companies[j])
                continue

            companies[j].insert(0, i)

            # summaryProfile - sector
            companies[j].append(data['summaryProfile']['sector'].replace('—', '-').replace(',', '-'))
            # summaryProfile - industry
            companies[j].append(data['summaryProfile']['industry'].replace('—', '-').replace(',', '-'))
            # financialData - currentPrice - raw
            companies[j].append(float(data['financialData']['currentPrice']['raw']))
            print(color_green_to_print + str(companies[j]))
            table.insert_row([companies[j][0], companies[j][1], companies[j][2], companies[j][3], companies[j][4], '-'])
            window.update()

            append_company_output(companies[j])
            j += 1
            i += 1
    else:
        while j < len(data_outer):
            if len(data_outer) != 0:
                data = json.loads(data_outer[j])
                companies.append([data['quoteType']['symbol']])
            else:
                break
            # summaryDetail - priceToSalesTrailing12Months - raw
            # defaultKeyStatistics - trailingEps - raw
            # price - marketCap - raw
            # defaultKeyStatistics - forwardPE - raw
            # financialData - ebitda - raw
            # financialData - revenuePerShare - raw
            if check_raw(data, 'summaryDetail', 'priceToSalesTrailing12Months', 'P/S', target_ps, sign_ps) \
                    or check_raw(data, 'price', 'marketCap', 'market cap', target_market_cap, sign_market_cap) \
                    or check_raw(data, 'defaultKeyStatistics', 'trailingEps', 'EPS', target_eps, sign_eps) \
                    or check_raw(data, 'defaultKeyStatistics', 'forwardPE', 'P/E', target_pe, sign_pe) \
                    or check_raw(data, 'financialData', 'ebitda', 'EBITDA', target_ebitda, sign_ebitda) \
                    or check_raw(data, 'financialData', 'revenuePerShare', 'RPS', target_rps, sign_rps) \
                    or check_raw(data, 'summaryDetail', 'payoutRatio', 'Payout ratio', target_payout_ratio, sign_payout_ratio) \
                    or check_raw(data, 'summaryDetail', 'dividendYield', 'Dividend yield', target_dividend_yield, sign_dividend_yield) \
                    or check_raw(data, 'financialData', 'operatingCashflow', 'Operating Cashflow', target_operating_cashflow, sign_operating_cashflow) \
                    or check_raw(data, 'financialData', 'freeCashflow', 'Free Cashflow', target_free_cashflow, sign_free_cashflow) \
                    or check_raw(data, 'financialData', 'quickRatio', 'Quick Ratio', target_quick_ratio, sign_quick_ratio):
                data_outer.remove(data_outer[j])
                companies.remove(companies[j])
                continue

            # financialData - returnOnEquity, returnOnAssets - raw
            if check_roe_roa_pb(data):
                data_outer.remove(data_outer[j])
                companies.remove(companies[j])
                continue

            companies[j].insert(0, i)
            # summaryProfile - sector
            companies[j].append(data['summaryProfile']['sector'].replace('—', '-').replace(',', '-'))
            # summaryProfile - industry
            companies[j].append(data['summaryProfile']['industry'].replace('—', '-').replace(',', '-'))
            # financialData - currentPrice - raw
            companies[j].append(float(data['financialData']['currentPrice']['raw']))
            print(color_green_to_print + str(companies[j]))

            append_company_output(companies[j])
            j += 1
            i += 1

    try:
        amount_in_usd = int(e_calculate.get())
        percentage = round(1 / len(companies), 5)
        amount_for_company = round(amount_in_usd * percentage, 5)
        for i in range(len(companies)):
            number_of_stocks = float(amount_for_company) // float(companies[i][4])
            companies[i].append(int(number_of_stocks))
            table.insert_row(
                [companies[i][0], companies[i][1], companies[i][2], companies[i][3], companies[i][4], companies[i][5]])
            window.update()
    except ValueError:
        alert('Error!', 'You should type an integer number.')
    except ZeroDivisionError:
        alert('Error!', 'No companies to calculate number of stocks. \nFirstly, You should find some companies.')

    create_label(frame_settings, f'Total number of companies: {len(companies)}', counter_row, counter_column, 3)
    alert('Done!', 'Companies analyzed!')


def print_data(event):
    global rb_pe, pe, rb_ps, ps, rb_pb, pb, rb_eps, eps, rb_ebitda, ebitda, rb_rps, rps, \
        rb_roe, roe, rb_roa, roa, rb_cap, cap, target_pe, sign_pe, target_ps, sign_ps, target_pb, sign_pb, \
        target_eps, sign_eps, target_roe, sign_roe, target_roa, sign_roa, target_market_cap, sign_market_cap, \
        target_ebitda, sign_ebitda, target_rps, sign_rps, rb_pay, pay, target_payout_ratio, sign_payout_ratio, div, \
        rb_div, target_dividend_yield, sign_dividend_yield, rb_operation, operation, target_operating_cashflow, \
        sign_operating_cashflow, free, rb_free, target_free_cashflow, sign_free_cashflow, quick, rb_quick, \
        target_quick_ratio, sign_quick_ratio
    if rb_pe.get() == less_text:
        sign_pe = '<'
    else:
        sign_pe = '>'
    if pe.get() != 'Input a number':
        target_pe = float(pe.get())

    if rb_ps.get() == less_text:
        sign_ps = '<'
    else:
        sign_ps = '>'
    if ps.get() != 'Input a number':
        target_ps = float(ps.get())

    if rb_pb.get() == less_text:
        sign_pb = '<'
    else:
        sign_pb = '>'
    if pb.get() != 'Input a number':
        target_pb = float(pb.get())

    if rb_eps.get() == less_text:
        sign_eps = '<'
    else:
        sign_eps = '>'
    if eps.get() != 'Input a number':
        target_eps = float(eps.get())

    if rb_roe.get() == less_text:
        sign_roe = '<'
    else:
        sign_roe = '>'
    if roe.get() != 'Input a number':
        target_roe = float(roe.get())

    if rb_roa.get() == less_text:
        sign_roa = '<'
    else:
        sign_roa = '>'
    if roa.get() != 'Input a number':
        target_roa = float(roa.get())

    if rb_cap.get() == less_text:
        sign_market_cap = '<'
    else:
        sign_market_cap = '>'
    if cap.get() != 'Input a number':
        target_market_cap = float(cap.get())

    if rb_ebitda.get() == less_text:
        sign_ebitda = '<'
    else:
        sign_ebitda = '>'
    if ebitda.get() != 'Input a number':
        target_ebitda = float(ebitda.get())

    if rb_rps.get() == less_text:
        sign_rps = '<'
    else:
        sign_rps = '>'
    if rps.get() != 'Input a number':
        target_rps = float(rps.get())

    if rb_pay.get() == less_text:
        sign_payout_ratio = '<'
    else:
        sign_payout_ratio = '>'
    if pay.get() != 'Input a number':
        target_payout_ratio = float(pay.get())

    if rb_div.get() == less_text:
        sign_dividend_yield = '<'
    else:
        sign_dividend_yield = '>'
    if div.get() != 'Input a number':
        target_dividend_yield = float(div.get())

    if rb_operation.get() == less_text:
        sign_operating_cashflow = '<'
    else:
        sign_operating_cashflow = '>'
    if operation.get() != 'Input a number':
        target_operating_cashflow = float(operation.get())

    if rb_free.get() == less_text:
        sign_free_cashflow = '<'
    else:
        sign_free_cashflow = '>'
    if free.get() != 'Input a number':
        target_free_cashflow = float(free.get())

    if rb_quick.get() == less_text:
        sign_quick_ratio = '<'
    else:
        sign_quick_ratio = '>'
    if quick.get() != 'Input a number':
        target_quick_ratio = float(quick.get())

    # @todo
    # read_csv_symbols()
    prepare_output_file()
    # get_data_requests()
    get_data_file()


def print_data_default(event):
    # @todo
    # read_csv_symbols()
    prepare_output_file()
    # get_data_requests()
    get_data_file()


if __name__ == '__main__':
    # start_timer = get_current_time_milliseconds()
    # end_timer = get_current_time_milliseconds()
    # time_of_running = end_timer - start_timer
    # print(color_green_to_print + 'Time of running in milliseconds: ' + str(time_of_running))
    # print(color_green_to_print + 'Time of running in seconds: ' + str(time_of_running / 1000))

    window = Tk()
    window.title('Market stocks screener')
    window.minsize(400, 250)
    window.maxsize(2880, 1620)
    window.iconphoto(False, PhotoImage(file='logo.png'))

    table = Table(master=window, height=600,
                  column_headers=default_columns,
                  column_min_widths=[6, 6, 6, 8, 150, 120])
    table.pack(side=LEFT)

    frame_settings = Frame()
    counter_row = 0
    counter_column = 0

    create_label(master=frame_settings, text='Filters', row=counter_row, column=counter_column + 1)
    counter_row += 1
    create_label(master=frame_settings, text='I\'m finding a company which has...', row=counter_row,
                 column=counter_column, columnspan=4)
    counter_row += 1

    rb_pe, pe = create_filter(frame_settings, 'P/E:')
    rb_ps, ps = create_filter(frame_settings, 'P/S:')
    rb_eps, eps = create_filter(frame_settings, 'EPS:')
    rb_ebitda, ebitda = create_filter(frame_settings, 'EBITDA:')
    rb_rps, rps = create_filter(frame_settings, 'RPS:')
    rb_roe, roe = create_filter(frame_settings, 'ROE:')
    rb_roa, roa = create_filter(frame_settings, 'ROA:')
    rb_pb, pb = create_filter(frame_settings, 'P/B:')
    rb_cap, cap = create_filter(frame_settings, 'Market cap:')
    rb_pay, pay = create_filter(frame_settings, 'Payout ratio:')
    rb_div, div = create_filter(frame_settings, 'Dividend yield:')
    rb_operation, operation = create_filter(frame_settings, 'Operating CF:')
    rb_free, free = create_filter(frame_settings, 'Free CF:')
    rb_quick, quick = create_filter(frame_settings, 'Quick ratio:')

    e_calculate = create_calculate_part_of_ui(frame_settings)

    btn_confirm = Button(master=frame_settings, text='Confirm')
    btn_confirm.grid(row=counter_row, column=counter_column, sticky='w')
    btn_confirm.bind('<Button-1>', print_data)
    counter_column += 1

    btn_confirm_default = Button(master=frame_settings, text='Confirm with default filters')
    btn_confirm_default.grid(row=counter_row, column=counter_column, columnspan=2, sticky='w')
    btn_confirm_default.bind('<Button-1>', print_data_default)
    counter_row += 1
    counter_column = 0
    create_label(frame_settings, ' ', counter_row, counter_column)
    counter_row += 1
    counter_column = 0

    combobox = Combobox(master=frame_settings, values=default_columns, state='readonly')
    combobox.set(default_columns[0])
    combobox.grid(row=counter_row, column=counter_column, columnspan=2, sticky='w')
    counter_column += 2

    var_sort = StringVar()
    asc_rb = Radiobutton(master=frame_settings, text=ascending_text, value=ascending_text, variable=var_sort)
    asc_rb.select()
    asc_rb.grid(row=counter_row, column=counter_column, sticky='w')
    counter_column += 1
    desc_rb = Radiobutton(master=frame_settings, text=descending_text, value=descending_text, variable=var_sort)
    desc_rb.grid(row=counter_row, column=counter_column, sticky='w')
    counter_row += 1
    counter_column = 0
    btn_confirm_sort = Button(master=frame_settings, text='Sort')
    btn_confirm_sort.grid(row=counter_row, column=counter_column, sticky='w')
    btn_confirm_sort.bind('<Button-1>', sort)
    counter_row += 1
    counter_column = 0
    create_label(frame_settings, ' ', counter_row, counter_column)
    counter_row += 1
    counter_column = 0

    frame_settings.pack()
    window.state('zoomed')
    window.mainloop()
