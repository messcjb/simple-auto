import time
import pyupbit
import datetime

access = "aaa"
secret = "bbb"

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")
my_balance = get_balance("KRW")  # 잔고 조회
print(str(format(int(my_balance),",")) + "원")
a = 1
b = 1
c = 1
buy = 1

# 자동매매 시작
while True:
        ticker="KRW-ADA" #종목코드 =========================================> 여기 입력
        now = datetime.datetime.now()
        start_time = get_start_time(ticker)
        end_time = start_time + datetime.timedelta(days=1)

        if start_time < now < end_time - datetime.timedelta(seconds=15):
            target_price = get_target_price(ticker, 0.5) #K값 입력 ===================> K 값 여기 입력!!!!!!!!!
            current_price = get_current_price(ticker)
            avg_price = upbit.get_avg_buy_price(ticker)

            if a < 1.5:
               print("target_price", target_price) # 목표가
               print("current_price", current_price)

            if target_price < current_price:
                # krw = get_balance("KRW")
                krw_input = 1000000  # =======================================> 주문금액 !!!!!!!!!!!!!!!!!
                         
                if buy < 1.5: # ============> 구매후 잔금으로 추가구매하는 것 막는 장치. 수동입력
                   upbit.buy_market_order(ticker, krw_input)
                   buy = buy + 1
 
                else:
                    coin = get_balance("ADA") # ======================================> 여기 입력
                    if coin > 0.0001:
                        if b < 1.5 and c !=0 and current_price > avg_price*1.03: # 1차 익절조건 ===>  여기 % 입력...1차 3% 익절 
                           upbit.sell_market_order(ticker, coin*0.5)  # ======> 코인 50%를 3%에 1차 익절
                           b = b + 1
                        elif b == 2 and c != 0 and current_price > avg_price*1.07: # 2차 익절조건 ===>  여기 % 입력...2차 7% 익절
                             upbit.sell_market_order(ticker, coin*0.5)  # ======> 잔여 코인 50%를 8%에 2차 익절
                             b= b + 1
                        elif b !=0 and c < 1.5 and current_price < avg_price*0.98: # 1차 손절조건 ===> 여기 % 입력...1차 -2% 손절
                             upbit.sell_market_order(ticker, coin*0.5) # ======> 코인 50%를 -2%에 1차 손절
                             c = c + 1
                        elif b != 0 and c == 2 and current_price < avg_price*0.96: # 2차 손절조건 ===> 여기 % 입력...2차 -4% 손절
                             upbit.sell_market_order(ticker, coin*0.5) # ======> 잔여 코인 50%를 -5%에 2차 손절
                             c = c + 1

        else:
            coin = get_balance("ADA") # ======================================> 여기 입력
          
            if coin > 0.0001:
                upbit.sell_market_order(ticker, coin*1.0)
        time.sleep(1)
        a = a + 1
    
        time.sleep(1)