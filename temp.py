from tradingview_ta import TA_Handler, Interval, Exchange
from datetime import datetime
import time
import tinvest
import asyncio
import os
from multiprocessing import Process
import threading
import pickle
from github import Github
import github

TOKEN = "t.WVpg6thNk00O9Vd8P4vrne6om7zDgWaGIsKH6TqdRKgT2giER_3Lqp7w9DI7NYdjPWF4AXkj6MRNP5G51zp2lQ"
S_TOKEN = "t.gJWIDbsjDOGnbAl2y-pm5kzEIxljV-kWYb1To6Skr4STriOvfDp4q4xwvFzuLzaXxWZt2UzRXysejROedAS1TQ"
client = tinvest.SyncClient(TOKEN)

spis = []
token = ''
with open('token.txt', 'r') as f:
    token = f.read()
    token = token.replace('\n', ' ')
g = Github('ghp_' + token)

repo = g.get_user().get_repo("stock-bot")
contents = repo.get_contents("save.txt")

def save_elem(l):
    s = ''
    for i in l:
        if (type(i) == list):
            for j in i:
                s += str(j) + ' '
            s += '\n'
        else:
            s += str(i) + '\n'
    repo.update_file(contents.path, "save", s, contents.sha, branch='main')

def load_elem():
    l = []
    s = contents.decoded_content.decode()
    f = s.split('\n')
    for i in f:
        if len(i.split()) > 0:
            l.append(list(map(int, i.split())))
    return l

with open('stock_spis.txt', 'r') as stock_spis:
    spis = list(stock_spis.read().split())
    
buy_cnt = [0] * len(spis)
buy_price = [0] * len(spis)
lasts = [1] * len(spis)
lastm = [1] * len(spis)
my_plus = 0
list_print = []
try:
    buy_cnt, buy_price, my_plus = load_elem()
    my_plus = my_plus[0]
except:
    buy_cnt, buy_price, my_plus = load_elem()
    my_plus = my_plus[0]
print(buy_cnt)
print(buy_price)
while len(buy_cnt) < len(spis):
    buy_cnt.append(0)
    buy_price.append(0)
    
def fun(ind, el):
    global my_plus
    global list_print
    ticker = TA_Handler(
        symbol=el,
        screener="russia",
        exchange="MOEX",
        interval=Interval.INTERVAL_15_MINUTES
    )
    flag = True
    while flag:
        try:
            analysis = ticker.get_analysis()
            flag = False
        except:
            flag = True
            time.sleep(0.5)
    mm = analysis.indicators["MACD.macd"]
    ms = analysis.indicators["MACD.signal"]
    sk = analysis.indicators["Stoch.K"]
    sd = analysis.indicators["Stoch.D"]
    close = analysis.indicators["close"]
    s = sk - sd
    m = mm - ms
    if (s > 0 and lasts[ind] < 0) and (m > 0) and (buy_cnt[ind] == 0) and (sk < 79):
        
            
        #request to buy
        try:
            comm(el, 1, 'Buy', close)
            buy_cnt[ind] = 1
            buy_price[ind] = close
            list_print[ind].append([el, 'buy', close])
        except:
            list_print[ind].append([el, 'error buy(1)'])
            random_el = 1
    if (m > 0 and lastm[ind] < 0) and (s > 0) and (buy_cnt[ind] == 0) and (sk < 79):
        
            
        #request to buy
        try:
            comm(el, 1, 'Buy', close)
            buy_cnt[ind] = 1
            buy_price[ind] = close
            list_print[ind].append([el, 'buy', close])  
        except:
            list_print[ind].append([el, 'error buy(2)'])
            random_el = 1
            
    if ((s <= 0) or (m <= 0)) and (buy_cnt[ind] > 0):
        

        #request to sell
        try:
            comm(el, 1, 'Sell', close)
            my_plus += buy_cnt[ind] * close - buy_cnt[ind] * buy_price[ind]
            list_print[ind].append([el, 'sell', close])
            list_print[ind].append([buy_cnt[ind], (buy_cnt[ind] * close - buy_cnt[ind] * buy_price[ind]) / (buy_cnt[ind] * buy_price[ind]), '\n'])
            list_print[ind].append([my_plus])  
            buy_cnt[ind] = 0
        except:
            list_print[ind].append([el, 'error sell'])
            random_el = 1
        
    lasts[ind] = sk - sd
    lastm[ind] = mm - ms
#print(ans)
   
def comm(el, lots, operation, pr):
    instr = client.get_market_search_by_ticker(el)
    fg = instr.payload.instruments[0].figi
    orderbook = client.get_market_orderbook(figi=fg, depth='1').payload.last_price
    request = tinvest.LimitOrderRequest(lots=lots, operation=operation, price=orderbook)
    try:
        resp = client.post_orders_limit_order(fg, request)
    except:
        random_el = 1

def check_stocks():
    global list_print
    list_print = []
    procs = []
    for ind, el in enumerate(spis):
        proc = threading.Thread(target = fun, args = (ind, el))
        list_print.append([])
        proc.start()
        procs.append(proc)
        
    for proc in procs:
        proc.join()
    for i in list_print:
        for j in i:
            for k in j:
                print(k, end = ' ')
            print()
    proc = threading.Thread(target = ddos, args = (l))
    proc.start()

def ddos(l):
    global buy_cnt
    global buy_price
    global my_plus
    tm = time.time()
    while (time.time() - tm <= 7 * 60):
        try:
            save_elem([buy_cnt, buy_price, my_plus])
            return
        except:
            print("error to save")
            time.sleep(30)

def inf_f():  
    while True:
        n = datetime.now().minute
        tm = time.time()
        if n == 14:
            check_stocks()
        if n == 29:
            check_stocks()
        if n == 44:
            check_stocks()
        if n == 59:
            check_stocks()
        print('step end', time.time() - tm, datetime.now())
        time_sleep = 58 - datetime.now().second
        if time_sleep <= 0:
            time_sleep += 60
        time_sleep -= 1
        time_correct = 1000000 - datetime.now().microsecond
        time_sleep += time_correct / 1000000
        time.sleep(time_sleep)
inf_f()


