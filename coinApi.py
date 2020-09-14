from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from operator import itemgetter
from datetime import datetime
from prettytable import PrettyTable
from colorama import Fore, Back, Style
from datetime import datetime
import re

# parameters = ['BTC', 'XRP', 'ETH', 'LTC', 'LINK']
portfo = 'portfo.txt'

print()
print('MY PORTFOLIO')
print()

portfolio_value = 0.00
last_updated = 0

table = PrettyTable(['Asset', 'Amount Owned', 'Value', 'Price', '1h', '24h', '7d'])
table.align["Asset"] = "l"
table.align["Amount Owned"] = "c"
table.align["Value"] = "l"
table.align["Price"] = "l"
table.align["1h"] = "r"
table.align["24h"] = "r"
table.align["7d"] = "r"
# TODO: fix (am)amount_owned and tk, turn it into a function
try:
    am = []
    tk = []
    parameters = tk
    with open(portfo) as inp:
        for line in inp:
            ticker, amount = line.split()
            ticker = ticker.upper()
            # print("ticker --> ", ticker)
            amount = float(amount)
            am.append(amount)
            tk.append(ticker)
            # print("amount --> ", amount)


        def convert_list_to_string(org_list, seperator=','):
            """ Convert list to string, by joining all item in list with given separator.
                Returns the concatenated string """
            return seperator.join(org_list)


        full_str = convert_list_to_string(parameters)
        # print("THIS IS THE 'full_str' ", full_str)
        ticker_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol=' + full_str

        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': 'add-y0ur-api-key',
        }

        session = Session()
        session.headers.update(headers)

        response = session.get(ticker_url)
        data = json.loads(response.text)
        # print("this is data --> ", data)
        parsedData = json.dumps(response.json())
        currency = data['data']
            # print(currency)
        currency_keys = list(currency.keys())[:]
            # print("currency keys: ", currency_keys)
        currency_key_values = [val for key, val in currency.items()]
            # print("currenvy kwy values --> ", currency_key_values)
            # Currency Values
        id = list(map(itemgetter('id'), currency_key_values))
        name = list(map(itemgetter('name'), currency_key_values))
        # print("this is name --> ", name)
        symbol = list(map(itemgetter('symbol'), currency_key_values))
        # print("this is name --> symbol", symbol)
        # print(len(symbol))
        market_pairs = list(map(itemgetter('num_market_pairs'), currency_key_values))
        tags = list(map(itemgetter('tags'), currency_key_values))
        max_supply = list(map(itemgetter('max_supply'), currency_key_values))
        circulating_supply = list(map(itemgetter('circulating_supply'), currency_key_values))
        total_supply = list(map(itemgetter('total_supply'), currency_key_values))
        rank = list(map(itemgetter('cmc_rank'), currency_key_values))
                # down one 'quote's list
        quote = list(map(itemgetter('quote'), currency_key_values))
        values = list(map(itemgetter('USD'), quote))
        price = list(map(itemgetter('price'), values))
        # print("this is price --> ", price)
        volume_24h = list(map(itemgetter('volume_24h'), values))
        hour_change = list(map(itemgetter('percent_change_1h'), values))
        # print("this is  hour change --> ", hour_change)
        day_change = list(map(itemgetter('percent_change_24h'), values))
        week_change = list(map(itemgetter('percent_change_7d'), values))
        market_cap = list(map(itemgetter('market_cap'), values))
        last_updated = list(map(itemgetter('last_updated'), values))
        # print(last_updated)

        def Extract_row(lst):
            return list(zip(*lst))


        def list_to_float(list_obj):
            ltf = []
            for i in list_obj:
                f = float(i)
                ltf.append(f)

            return ltf


        length = len(price)
        # n = lst[1]
        amount_float = list_to_float(am)
        price_float = list_to_float(price)
        value = [a * b for a, b in zip(amount_float, price_float)]
        value_float = list_to_float(value)

        v = 0
        nl = []
        vl = []
        ao = []
        pc = []
        nv = []
        hc = []
        dc = []
        wc = []
        api = []
        # u_change = last_updated[0]
        # api.append(u_change)

        length = len(price)
        while v < length:
            p_change = price[v]
            npc = '${:,.2f}'.format(p_change)
            pc.append(npc)

            v_change = value[v]
            v_change = '${:,.2f}'.format(v_change)
            nv.append(v_change)


            h_change = hour_change[v]
            if h_change > 0:
                h_change = hour_change[v]
                h_changeF = Fore.GREEN + '{:,}%'.format(round(h_change, 4)) + Style.RESET_ALL
                hc.append(h_changeF)
            else:
                h_change = hour_change[v]
                h_changeF = Fore.RED + '{:,}%'.format(round(h_change, 4)) + Style.RESET_ALL
                hc.append(h_changeF)

            d_change = day_change[v]
            # d_changeF = '{:,}%'.format(round(d_change, 2))
            # dc.append(d_changeF)
            if d_change > 0:
                d_change = day_change[v]
                d_changeF = Fore.GREEN + '{:,}%'.format(round(d_change, 4)) + Style.RESET_ALL
                dc.append(d_changeF)
            else:
                d_change = day_change[v]
                d_changeF = Fore.RED + '{:,}%'.format(round(h_change, 4)) + Style.RESET_ALL
                dc.append(d_changeF)

            w_change = week_change[v]
            # w_changeF = '{:,}%'.format(round(w_change, 2))
            # wc.append(w_changeF)
            if w_change > 0:
                w_change = week_change[v]
                w_changeF = Fore.GREEN + '{:,}%'.format(round(w_change, 4)) + Style.RESET_ALL
                wc.append(w_changeF)
            else:
                w_change = week_change[v]
                w_changeF = Fore.RED + '{:,}%'.format(round(w_change, 4)) + Style.RESET_ALL
                wc.append(w_changeF)

            n_change = name[v]
            s_change = symbol[v]
            asts = str(n_change) + ' (' + str(s_change) + ')'
            nl.append(asts)

            v += 1

        # if float(str(hour_change[0])) > 0:
    lst = [nl, am, nv, pc, hc, dc, wc]
    # get the total value of profile
    vlu = sum((value))
    portfolio_value += vlu


    def add_row(data):
        i = 0
        while i < length:
            table.add_row(data[i])
            i += 1


    row = Extract_row(lst)
    add_row(row)
    print(table)
    print()

    portfolio_value_string = '{:,}'.format(round(portfolio_value, 2))

    # print(table.get_string(fields=["Value"]))

    # grab the last updated string
    last_updated_str = str(last_updated[0])
    # remove the unwanted items on the end
    sstring = '.000Z'
    if last_updated_str.endswith(sstring):
        res = re.sub(sstring, '', last_updated_str)

    td_format = '%Y-%m-%dT%H:%M:%S'
    st = '05:00:00'

    date_obj = datetime.strptime(res, td_format)

    # separate the date and time so we can convert the time
    date_from_obj = date_obj.strftime("%Y-%m-%d")

    # convert time from UTC to CST
    time_utc = date_obj.strftime("%H:%M:%S")
    time_cst = datetime.strptime(time_utc, "%H:%M:%S") - datetime.strptime(st, "%H:%M:%S")

    # put date and time back together
    # TODO: fix time stamp returning at 30:12:000z and throwing error in date:time format
    # cst_time_date_string = str(date_from_obj) + "T" + str(time_cst)
    # convert back to format computer can reed
    # ctds_convert = datetime.strptime(cst_time_date_string, td_format)
    # display it nice for users to read
    # pretty_date_obj = date_obj.strftime("%B %d, %Y at %I:%M %p")
    # pretty_converted_obj = ctds_convert.strftime("%B %d, %Y at %I:%M %p")

    print('Total Portfolio Value: ' + Fore.GREEN + '$' + portfolio_value_string + Style.RESET_ALL)
    print()
    print('API Results Last Updated on: ' + Fore.BLUE + str(date_obj) + Style.DIM + Style.RESET_ALL)
    print()

except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)
