import time
import pyupbit
import datetime

access = "access code"
secret = "secret code"

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

def get_ma15(ticker):
    """15일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=15)
    ma15 = df['close'].rolling(15).mean().iloc[-1]
    return ma15

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

# 자동매매 시작
while True:
    try:
        ticker="KRW-SAND" #종목코드 =========================================> 여기 입력
        now = datetime.datetime.now()
        start_time = get_start_time(ticker)
        end_time = start_time + datetime.timedelta(days=1)

        if start_time < now < end_time - datetime.timedelta(seconds=3600*2):
            target_price = get_target_price(ticker, 0.3) #K값 입력 ===================> K 값 여기 입력
            ma15 = get_ma15(ticker)
            current_price = get_current_price(ticker)
            if a < 1.5:
                print("target_price", target_price) # 목표가
                print("current_price", current_price)
            if target_price < current_price and ma15 < current_price:
                krw = get_balance("KRW")

                if krw > 7400000: #최소 주문금액 및 추가 주문 막는 금액 ==========> 여기 입력
                    upbit.buy_market_order(ticker, krw*0.05)
                else:
                    avg_price = upbit.get_avg_buy_price(ticker)
                
                    coin = get_balance("SAND") # ======================================> 여기 입력
                    
                    if coin > 0.1 and current_price > avg_price*1.05: # 매도조건 ===> 여기 입력
                        upbit.sell_market_order(ticker, coin*1.0)
                        break
                    
                    if coin > 0.1 and current_price < avg_price*0.97:
                        upbit.sell_market_order(ticker, coin*1.0)
                        break
                    
        else:
            coin = get_balance("SAND") # ======================================> 여기 입력
          
            if coin > 0.1:
                upbit.sell_market_order(ticker, coin*1.0)
        time.sleep(1)
        a = a + 1
    except Exception as e:
        print(e)
        time.sleep(1)