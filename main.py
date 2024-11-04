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

        # Linha 1: Endereço do Token e DEX
        token_addr_label = QLabel('Token Addr:')
        token_addr_input = QLineEdit()
        token_addr_input.setStyleSheet("background-color: #333; color: #FFF; border: 1px solid #555; padding: 5px;")

        dex_label = QLabel('DEX:')
        dex_selector = QComboBox()
        dex_selector.addItems(["PancakeSwap V2", "Uniswap V2", "SushiSwap", "Arbitrum", "TraderJoe V2"])
        dex_selector.setStyleSheet("background-color: #333; color: #FFF; border: 1px solid #555; padding: 5px;")

        main_layout.addWidget(token_addr_label, 0, 0)
        main_layout.addWidget(token_addr_input, 0, 1, 1, 3)
        main_layout.addWidget(dex_label, 0, 4)
        main_layout.addWidget(dex_selector, 0, 5)

        # Linha 2: Campos de Configurações (Gwei, Slippage, etc.)
        gwei_label = QLabel('GWEI to trade:')
        gwei_input = QSpinBox()
        gwei_input.setRange(0, 1000)
        gwei_input.setValue(25)
        gwei_input.setStyleSheet("background-color: #333; color: #FFF; border: 1px solid #555; padding: 5px;")

        buy_slippage_label = QLabel('Buy slippage %:')
        buy_slippage_input = QSpinBox()
        buy_slippage_input.setRange(0, 100)
        buy_slippage_input.setValue(10)
        buy_slippage_input.setStyleSheet("background-color: #333; color: #FFF; border: 1px solid #555; padding: 5px;")

        main_layout.addWidget(gwei_label, 1, 0)
        main_layout.addWidget(gwei_input, 1, 1)
        main_layout.addWidget(buy_slippage_label, 1, 2)
        main_layout.addWidget(buy_slippage_input, 1, 3)

        # Linha 3: Campos adicionais (taxa de compra, etc.)
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

        main_layout.addWidget(sell_slippage_label, 2, 0)
        main_layout.addWidget(sell_slippage_input, 2, 1)
        main_layout.addWidget(max_buy_tax_label, 2, 2)
        main_layout.addWidget(max_buy_tax_input, 2, 3)

        # Adicionando seções de botões (Start/Stop)
        start_button = QPushButton('START')
        stop_button = QPushButton('STOP')
        start_button.setStyleSheet("background-color: #5cb85c; color: #FFF; border-radius: 5px; padding: 10px;")
        stop_button.setStyleSheet("background-color: #d9534f; color: #FFF; border-radius: 5px; padding: 10px;")

        main_layout.addWidget(start_button, 3, 0)
        main_layout.addWidget(stop_button, 3, 1)

        # Adicionando área de log de transações
        log_area = QTextEdit()
        log_area.setReadOnly(True)
        log_area.setStyleSheet("background-color: #222; color: #FFF; border: 1px solid #555; padding: 5px;")
        main_layout.addWidget(log_area, 4, 0, 1, 6)

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
