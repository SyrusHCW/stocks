#!/usr/bin/env python3
import math
from datetime import datetime
import csv
import requests


finnhub_token = ''
tiingo_token = ''

stock_list = ['GNUS', 'LPCN', 'CHFS', 'SLS', 'ZSAN', 'ZOM', 'SVM', 'IAG', 'USAS', 'FSM', 'ASM']

stock_list_count = len(stock_list)


finnhub_headers = {'X-Finnhub-Token': finnhub_token}


available_balance = 1000
transaction_fee = 1.75


def stock_quantity(**kwargs):
        buy_sell_total_fee = kwargs['transaction_fee'] * 2
        purchase_credit = kwargs['available_balance'] - buy_sell_total_fee
        stock_quantity = purchase_credit / kwargs['ask_price']
        return(int(stock_quantity))



def tiingo_ask_price(stock, tiingo_token):
        #print('ttingo_ask_price ', stock)
        stock_url = '{0}{1}{2}{3}'.format('https://api.tiingo.com/iex/?tickers=', stock.lower(), '&token=', tiingo_token)
        #print(stock_url)
        stock_response = requests.get(stock_url)
        return(stock_response.json()[0]['last'])



def stock_gain(**kwargs):
        sell_total = kwargs['ask_price'] * kwargs['stock_quantity']
        purchase_total = kwargs['purchase_price'] * kwargs['stock_quantity']
        sell_gain = sell_total - purchase_total
        return(sell_gain)



def truncate(number, decimals=0):
    if not isinstance(decimals, int):
        raise TypeError("decimal places must be an integer.")
    elif decimals < 0:
        raise ValueError("decimal places has to be 0 or more.")
    elif decimals == 0:
        return math.trunc(number)
    factor = 10.0 ** decimals
    return(math.trunc(number * factor) / factor)


def csv_write_datapoints(**kwargs):
    print(kwargs)
    csv_name = '{0}{1}'.format(kwargs['stock'], '.csv')
    with open(csv_name, 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow([kwargs['now'], kwargs['ask_price']])


for stock in range(0,stock_list_count):
        stock_url = '{0}{1}'.format('https://finnhub.io/api/v1/quote?symbol=', stock_list[stock])
        stock_response = requests.get(stock_url, headers = finnhub_headers)
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        stock_low = stock_response.json()['l']
        #print(stock_low)
        #print(stock_list[stock])
        ask_price = tiingo_ask_price(stock_list[stock], tiingo_token)
        #stock_quantity_data = { 'available_balance': available_balance, 'ask_price': ask_price, 'transaction_fee': transaction_fee }
        #purchase_stock_quantity = stock_quantity(**stock_quantity_data)
        #print(purchase_stock_quantity)
        #stock_gain_data = {'ask_price': ask_price, 'stock_quantity': purchase_stock_quantity, 'purchase_price': stock_low}
        #net_stock_gain = stock_gain(**stock_gain_data)
        #truncate_net_stock_gain = truncate(net_stock_gain, decimals=2)
        #print(stock_list[stock], truncate_net_stock_gain)
        csv_data = {'stock': stock_list[stock], 'now': current_time, 'ask_price': ask_price}
        print(csv_data)
        csv_write_datapoints(**csv_data)
