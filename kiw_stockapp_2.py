import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QTimer, QTime
from pykiwoom.kiwoom import Kiwoom
from pykrx import stock
import datetime

# Qt Designer로 생성한 gui 파일 로드
form_class = uic.loadUiType(r'gui.ui')[0]

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Kiwoom 로그인
        self.kiwoom = Kiwoom()
        self.kiwoom.CommConnect(block=True)

        # 버튼 연결
        self.button_start.clicked.connect(self.start_trading)
        self.button_stop.clicked.connect(self.stop_trading)

        # 타이머 설정
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_market_time)

        self.trade_timer = QTimer(self)
        self.trade_timer.timeout.connect(self.trade_stocks)

    def start_trading(self):
        # ✅ 변경 1: check_market_time 1분마다 호출
        self.timer.start(1000 * 60)  

        # ✅ 변경 2: trade_stocks 17초마다 호출
        self.trade_timer.start(1000 * 17)  

        self.text_board.append("[시스템] 자동매매가 시작되었습니다.")

    def stop_trading(self):
        self.timer.stop()
        self.trade_timer.stop()
        self.text_board.append("[시스템] 자동매매가 중지되었습니다.")

    def check_market_time(self):
        now = QTime.currentTime()
        current_time = now.toString("HHmm")

        # 예: 15시(장마감)에 매도
        if current_time >= "1500":
            self.timer.stop()
            self.trade_timer.stop()
            self.sell_all_stocks()

    # def trade_stocks(self):
    #     codes = self.code_list.text().split(',')
    #     k_value = float(self.k_value.text())

    #     for code in codes:
    #         code = code.strip()
    #         if not code:
    #             continue

    #         # 현재가 및 종목명 조회
    #         result = self.kiwoom.block_request("opt10001",
    #                                            종목코드=code,
    #                                            output="주식기본정보",
    #                                            next=0)
    #         if result is None or '현재가' not in result:
    #             continue

    #         current_price = int(result['현재가'][0].replace(",", ""))
    #         name = result['종목명'][0]

    #         # ✅ 변경 3: 현재가를 text_board에 1초마다 출력
    #         now_str = datetime.datetime.now().strftime("%H:%M:%S")
    #         self.text_board.append(f"[{now_str}] [{code}] [{name}] 현재가: {current_price:,}원")

    #         # 변동성 돌파 전략 계산
    #         today = datetime.datetime.now().strftime('%Y%m%d')
    #         yesterday_data = stock.get_market_ohlcv_by_date(today, today, code)

    #         if not yesterday_data.empty:
    #             high = yesterday_data['고가'][0]
    #             low = yesterday_data['저가'][0]
    #             close = yesterday_data['종가'][0]
    #             target_price = close + (high - low) * k_value

    #             # 매수 조건 체크
    #             if current_price > target_price:
    #                 self.buy_stock(code, current_price, 1)
    def trade_stocks(self):
        # ✅ pykrx 유틸리티로 직전 거래일 구하기
        today_str = datetime.datetime.now().strftime('%Y%m%d')
        yesterday = stock.get_previous_business_day(today_str)
        codes = self.code_list.text().split(',')
        k_value = float(self.k_value.text())

        for code in codes:
            code = code.strip()
            if not code:
                continue

            # 현재가 및 종목명 조회
            result = self.kiwoom.block_request("opt10001",
                                            종목코드=code,
                                            output="주식기본정보",
                                            next=0)
            if result is None or '현재가' not in result:
                continue

            current_price = int(result['현재가'][0].replace(",", ""))
            name = result['종목명'][0]

            # ✅ 현재가를 text_board에 출력
            now_str = datetime.datetime.now().strftime("%H:%M:%S")
            self.text_board.append(f"[{now_str}] [{code}] [{name}] 현재가: {current_price:,}원")

            # ✅ 전일(직전 거래일) OHLC 데이터 불러오기
            df = stock.get_market_ohlcv_by_date(yesterday, yesterday, code)

            if df.empty:
                self.text_board.append(f"[오류] [{code}] 전일({yesterday}) 데이터가 없습니다.")
                continue

            # ✅ 전일 고가/저가/종가 추출
            high = df['고가'][0]
            low = df['저가'][0]
            close = df['종가'][0]

            # ✅ 변동성 돌파 매수가 계산
            target_price = close + (high - low) * k_value

            # ✅ 매수 조건: 현재가가 목표가 초과 시 매수 신호
            if current_price > target_price:
                self.buy_stock(code, current_price, 1)


    def buy_stock(self, code, price, quantity):
        name = self.kiwoom.block_request("opt10001",
                                         종목코드=code,
                                         output="주식기본정보",
                                         next=0)['종목명'][0]
        self.buysell_log.append(f"[매수] [{code}] [{name}] [가격: {price:,}] [수량: {quantity}]")

    def sell_all_stocks(self):
        self.buysell_log.append("[매도] 15시가 되어 모든 주식을 매도합니다.")
        self.text_board.append("[시스템] 15시 매도 완료, 자동매매 종료.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    sys.exit(app.exec_())
