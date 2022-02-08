from tradingview_ta import TA_Handler, Interval, Exchange
from datetime import datetime
import time
import tinvest
TOKEN = "t.WVpg6thNk00O9Vd8P4vrne6om7zDgWaGIsKH6TqdRKgT2giER_3Lqp7w9DI7NYdjPWF4AXkj6MRNP5G51zp2lQ"
S_TOKEN = "t.gJWIDbsjDOGnbAl2y-pm5kzEIxljV-kWYb1To6Skr4STriOvfDp4q4xwvFzuLzaXxWZt2UzRXysejROedAS1TQ"
client = tinvest.SyncClient(TOKEN)

spis = {'IRAO', 'VTBR', 'SBER', 'GAZP', 'RUAL', 'DSKY', 'MTSS', 'FIVE', 'MVID', 'TATN', 'CHMF', 'ALRS', 'SGZH'}
lasts = {'T-RM' : -1, 'F-RM' : -1, 'M-RM' : -1, 'SWN-RM' : -1, 'IRAO' : -1, 'VTBR' : -1, 'SBER' : -1, 'GAZP' : -1, 'RUAL' : -1, 'DSKY' : -1, 'MTSS' : -1, 'FIVE' : -1, 'MVID' : -1, 'TATN' : -1, 'CHMF' : -1, 'ALRS' : -1, 'SGZH' : -1}
lastm = {'T-RM' : -1, 'F-RM' : -1, 'M-RM' : -1, 'SWN-RM' : -1, 'IRAO' : -1, 'VTBR' : -1, 'SBER' : -1, 'GAZP' : -1, 'RUAL' : -1, 'DSKY' : -1, 'MTSS' : -1, 'FIVE' : -1, 'MVID' : -1, 'TATN' : -1, 'CHMF' : -1, 'ALRS' : -1, 'SGZH' : -1}
order = {'T-RM' : 'sell', 'F-RM' : 'sell', 'M-RM' : 'sell', 'SWN-RM' : 'sell', 'IRAO' : 'sell', 'VTBR' : 'sell', 'SBER' : 'sell', 'GAZP' : 'sell', 'RUAL' : 'sell', 'DSKY' : 'sell', 'MTSS' : 'sell', 'FIVE' : 'sell', 'MVID' : 'sell', 'MVID' : 'sell', 'TATN' : 'sell', 'CHMF' : 'sell', 'ALRS' : 'sell', 'SGZH' : 'sell'}
buy = {'T-RM' : 0, 'F-RM' : 0, 'M-RM' : 0, 'SWN-RM' : 0, 'IRAO' : 0, 'VTBR' : 0, 'SBER' : 0, 'GAZP' : 0, 'RUAL' : 0, 'DSKY' : 0, 'MTSS' : 0, 'FIVE' : 0, 'MVID' : 0, 'TATN' : 0, 'CHMF' : 0, 'ALRS' : 0, 'SGZH' : 0}
ans = {'T-RM' : 0, 'F-RM' : 0, 'M-RM' : 0, 'SWN-RM' : 0, 'IRAO' : 0, 'VTBR' : 0, 'SBER' : 0, 'GAZP' : 0, 'RUAL' : 0, 'DSKY' : 0, 'MTSS' : 0, 'FIVE' : 0, 'MVID' : 0, 'TATN' : 0, 'CHMF' : 0, 'ALRS' : 0, 'SGZH' : 0}
ind = {'T-RM' : 0, 'F-RM' : 1, 'M-RM' : 2, 'SWN-RM' : 3, 'IRAO' : 4, 'VTBR' : 5, 'SBER' : 6, 'GAZP' : 7, 'RUAL' : 8, 'DSKY' : 9, 'MTSS' : 10, 'FIVE' : 11, 'MVID' : 12, 'TATN' : 13, 'CHMF' : 14, 'ALRS' : 15, 'SGZH' : 16}

'''with open('d.txt', 'r') as f:
    for i in f:
        s = i.split()
        lasts[s[0]] = float(s[1])
        lastm[s[0]] = float(s[2])
        order[s[0]] = s[3]
        buy[s[0]] = float(s[4])
        ans[s[0]] = float(s[5])
'''

def fun():
    time.sleep(53)
    for el in spis:
        ticker = TA_Handler(
            symbol=el,
            screener="russia",
            exchange="MOEX",
                interval=Interval.INTERVAL_15_MINUTES
        )
        
        analysis = ticker.get_analysis()
        mm = analysis.indicators["MACD.macd"]
        ms = analysis.indicators["MACD.signal"]
        sk = analysis.indicators["Stoch.K"]
        sd = analysis.indicators["Stoch.D"]
        close = analysis.indicators["close"]
        
        s = sk - sd
        m = mm - ms
        if (s > 0 and lasts[el] < 0) and (m > 0) and order[el] == 'buy':
            order[el] = 'sell'
            buy[el] = close
            print(el, 'buy', close)
            
            #request to buy
            try:
                comm(el, 1, 'Buy', close)
            except:
                random_el = 1
            
        if (m > 0 and lastm[el] < 0) and (s > 0) and order[el] == 'buy':
            order[el] = 'sell'
            buy[el] = close
            print(el, 'buy', close)
            
            #request to buy
            try:
                comm(el, 1, 'Buy', close)
            except:
                random_el = 1
            
        if (s <= 0) and order[el] == 'sell':
            order[el] = 'buy'
            if buy[el] != 0:
                ans[el] += (close - buy[el]) / buy[el] * 100
                print(el, 'sell', close)
                
            #request to sell
            try:
                comm(el, 1, 'Sell', close)
            except:
                random_el = 1
        
        lasts[el] = sk - sd
        lastm[el] = mm - ms
    with open('d.txt', 'w') as f:
        for i in spis:
            f.write(i + ' ' + str(lasts[i]) + ' ' + str(lastm[i]) + '  ' + order[i] + '  ' + str(buy[i]) + '  ' + str(ans[i]) + '  ' + '\n')
    print(ans)
   
def comm(el, lots, operation, pr):
    instr = client.get_market_search_by_ticker(el)
    fg = instr.payload.instruments[0].figi
    request = tinvest.LimitOrderRequest(lots=lots, operation=operation, price=pr)
    try:
        resp = client.post_orders_limit_order(fg, request)
    except:
        random_el = 1
    



    
while True:
    n = datetime.now().minute
    if n == 14:
        fun()
    if n == 29:
        fun()
    if n ==44:
        fun()
    if n == 59:
        fun()
    time.sleep(1)
