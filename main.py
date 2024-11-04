import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget,
                             QHBoxLayout, QComboBox, QTextEdit, QCheckBox, QSpinBox, QGridLayout)
from PyQt5.QtCore import Qt

class TradingBotApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Sniper Trading Bot')
        self.setGeometry(100, 100, 1200, 800)

        # Layout principal
        main_layout = QGridLayout()

        # Linha 1: Token Address e DEX
        token_addr_label = QLabel('Token Addr:')
        token_addr_input = QLineEdit()
        token_addr_input.setStyleSheet("background-color: #333; color: #FFF; border: 1px solid #555; padding: 5px;")

        dex_label = QLabel('DEX:')
        dex_selector = QComboBox()
        dex_selector.addItems(["PancakeSwap V2", "UniSwap V2", "PancakeSwap V3", "Arbitrum SushiSwap", "TraderJoe V2"])
        dex_selector.setStyleSheet("background-color: #333; color: #FFF; border: 1px solid #555; padding: 5px;")

        main_layout.addWidget(token_addr_label, 0, 0)
        main_layout.addWidget(token_addr_input, 0, 1, 1, 3)
        main_layout.addWidget(dex_label, 0, 4)
        main_layout.addWidget(dex_selector, 0, 5)

        # Linha 2: Campos de configuração de negociação
        pay_coin_label = QLabel('Pay Coin to trade:')
        pay_coin_input = QLineEdit()
        pay_coin_input.setStyleSheet("background-color: #333; color: #FFF; border: 1px solid #555; padding: 5px;")

        gwei_label = QLabel('GWEI to trade:')
        gwei_input = QSpinBox()
        gwei_input.setRange(0, 1000)
        gwei_input.setValue(25)
        gwei_input.setStyleSheet("background-color: #333; color: #FFF; border: 1px solid #555; padding: 5px;")

        main_layout.addWidget(pay_coin_label, 1, 0)
        main_layout.addWidget(pay_coin_input, 1, 1)
        main_layout.addWidget(gwei_label, 1, 2)
        main_layout.addWidget(gwei_input, 1, 3)

        # Linha 3: Opções de Gwei e slippage
        tip_gwei_label = QLabel('Tip (GWEI):')
        tip_gwei_input = QSpinBox()
        tip_gwei_input.setRange(0, 1000)
        tip_gwei_input.setValue(10)
        tip_gwei_input.setStyleSheet("background-color: #333; color: #FFF; border: 1px solid #555; padding: 5px;")

        auto_gwei_checkbox = QCheckBox('Auto Gwei')
        auto_gwei_checkbox.setStyleSheet("color: #FFF;")

        buy_slippage_label = QLabel('Buy slippage %:')
        buy_slippage_input = QSpinBox()
        buy_slippage_input.setRange(0, 100)
        buy_slippage_input.setValue(10)
        buy_slippage_input.setStyleSheet("background-color: #333; color: #FFF; border: 1px solid #555; padding: 5px;")

        main_layout.addWidget(tip_gwei_label, 2, 0)
        main_layout.addWidget(tip_gwei_input, 2, 1)
        main_layout.addWidget(auto_gwei_checkbox, 2, 2)
        main_layout.addWidget(buy_slippage_label, 2, 3)
        main_layout.addWidget(buy_slippage_input, 2, 4)

        # Linha 4: Outras configurações
        sell_slippage_label = QLabel('Sell slippage %:')
        sell_slippage_input = QSpinBox()
        sell_slippage_input.setRange(0, 100)
        sell_slippage_input.setValue(10)
        sell_slippage_input.setStyleSheet("background-color: #333; color: #FFF; border: 1px solid #555; padding: 5px;")

        max_buy_tax_label = QLabel('Max buy tax %:')
        max_buy_tax_input = QSpinBox()
        max_buy_tax_input.setRange(0, 100)
        max_buy_tax_input.setValue(10)
        max_buy_tax_input.setStyleSheet("background-color: #333; color: #FFF; border: 1px solid #555; padding: 5px;")

        max_sell_tax_label = QLabel('Max sell tax %:')
        max_sell_tax_input = QSpinBox()
        max_sell_tax_input.setRange(0, 100)
        max_sell_tax_input.setValue(10)
        max_sell_tax_input.setStyleSheet("background-color: #333; color: #FFF; border: 1px solid #555; padding: 5px;")

        main_layout.addWidget(sell_slippage_label, 3, 0)
        main_layout.addWidget(sell_slippage_input, 3, 1)
        main_layout.addWidget(max_buy_tax_label, 3, 2)
        main_layout.addWidget(max_buy_tax_input, 3, 3)
        main_layout.addWidget(max_sell_tax_label, 3, 4)
        main_layout.addWidget(max_sell_tax_input, 3, 5)

        # Linha 5: Aprovação de GWEI e opções de Pinksale
        gwei_approve_label = QLabel('GWEI to approve:')
        gwei_approve_input = QSpinBox()
        gwei_approve_input.setRange(0, 1000)
        gwei_approve_input.setValue(5)
        gwei_approve_input.setStyleSheet("background-color: #333; color: #FFF; border: 1px solid #555; padding: 5px;")

        force_approve_button = QPushButton('Force Approve')
        force_approve_button.setStyleSheet("background-color: #5cb85c; color: #FFF; border-radius: 5px; padding: 10px;")

        pinksale_checkbox = QCheckBox('Pinksale options')
        pinksale_checkbox.setStyleSheet("color: #FFF;")

        main_layout.addWidget(gwei_approve_label, 4, 0)
        main_layout.addWidget(gwei_approve_input, 4, 1)
        main_layout.addWidget(force_approve_button, 4, 2)
        main_layout.addWidget(pinksale_checkbox, 4, 3)

        # Seção de botões e log
        start_button = QPushButton('START')
        stop_button = QPushButton('STOP')
        start_button.setStyleSheet("background-color: #5cb85c; color: #FFF; border-radius: 5px; padding: 10px;")
        stop_button.setStyleSheet("background-color: #d9534f; color: #FFF; border-radius: 5px; padding: 10px;")

        log_area = QTextEdit()
        log_area.setReadOnly(True)
        log_area.setStyleSheet("background-color: #222; color: #FFF; border: 1px solid #555; padding: 5px;")

        main_layout.addWidget(start_button, 5, 0)
        main_layout.addWidget(stop_button, 5, 1)
        main_layout.addWidget(log_area, 6, 0, 1, 6)

        # Configuração do container
        container = QWidget()
        container.setLayout(main_layout)
        container.setStyleSheet("background-color: #1a1a1a;")
        self.setCentralWidget(container)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = TradingBotApp()
    mainWin.show()
    sys.exit(app.exec_())
