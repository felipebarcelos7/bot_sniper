import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QComboBox, QTextEdit, QCheckBox, QSpinBox
from PyQt5.QtCore import Qt
from web3 import Web3

class TradingBotApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.w3 = Web3(Web3.HTTPProvider("https://bsc-dataseed.binance.org/"))

        if self.w3.is_connected():
            self.log_area.append("Conectado à blockchain!")
        else:
            self.log_area.append("Falha ao conectar à blockchain.")

    def initUI(self):
        self.setWindowTitle('Sniper Trading Bot')
        self.setGeometry(100, 100, 1000, 700)

        # Aplicando estilo QSS para toda a janela
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                color: #c0c0c0;
                font-family: Arial;
            }
            QLabel {
                font-size: 14px;
            }
            QLineEdit, QComboBox, QSpinBox {
                background-color: #333;
                border: 1px solid #555;
                border-radius: 5px;
                padding: 5px;
                color: #c0c0c0;
            }
            QPushButton {
                background-color: #3a3a3a;
                border: 1px solid #555;
                border-radius: 5px;
                padding: 5px;
                color: #c0c0c0;
            }
            QPushButton:hover {
                background-color: #505050;
            }
            QTextEdit {
                background-color: #282828;
                border: 1px solid #555;
                color: #c0c0c0;
            }
        """)

        # Layout principal
        main_layout = QVBoxLayout()

        # Linha superior com token e DEX
        top_layout = QHBoxLayout()
        self.token_addr_label = QLabel('Token Addr:')
        self.token_addr_input = QLineEdit(self)
        self.dex_selector = QComboBox(self)
        self.dex_selector.addItems(["PancakeSwap V2", "Uniswap V2", "SushiSwap", "Arbitrum", "TraderJoe V2"])

        top_layout.addWidget(self.token_addr_label)
        top_layout.addWidget(self.token_addr_input)
        top_layout.addWidget(self.dex_selector)

        main_layout.addLayout(top_layout)

        # Configurações de slippage e Gwei
        config_layout = QHBoxLayout()
        self.slippage_label = QLabel('Slippage %:')
        self.slippage_input = QSpinBox(self)
        self.slippage_input.setRange(0, 100)
        self.slippage_input.setValue(5)

        self.gwei_label = QLabel('Gwei:')
        self.gwei_input = QSpinBox(self)
        self.gwei_input.setRange(0, 500)
        self.gwei_input.setValue(5)

        config_layout.addWidget(self.slippage_label)
        config_layout.addWidget(self.slippage_input)
        config_layout.addWidget(self.gwei_label)
        config_layout.addWidget(self.gwei_input)

        main_layout.addLayout(config_layout)

        # Botões de ação
        button_layout = QHBoxLayout()
        self.buy_button = QPushButton('Buy Token')
        self.sell_button = QPushButton('Sell Token')

        button_layout.addWidget(self.buy_button)
        button_layout.addWidget(self.sell_button)

        main_layout.addLayout(button_layout)

        # Área de log de transações
        self.log_area = QTextEdit(self)
        self.log_area.setReadOnly(True)
        main_layout.addWidget(QLabel('Transaction Log:'))
        main_layout.addWidget(self.log_area)

        # Configuração do container
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Conectar os botões às funções
        self.buy_button.clicked.connect(self.buy_token)
        self.sell_button.clicked.connect(self.sell_token)

    def buy_token(self):
        token_address = self.token_addr_input.text()
        slippage = self.slippage_input.value()
        gwei = self.gwei_input.value()

        if not token_address:
            self.log_area.append('Erro: Por favor, insira o endereço do token.')
            return

        # Exemplo de log de transação
        self.log_area.append(f'Iniciando a compra do token: {token_address}')
        self.log_area.append(f'Slippage definido: {slippage}%')
        self.log_area.append(f'Gas Price definido: {gwei} Gwei')

        # Lógica para enviar a transação (adicionar lógica real aqui)
        try:
            # Transação simulada para fins de demonstração
            tx_hash = '0x123abc...'  # Substituir pela chamada real de `web3.eth.sendTransaction()`
            self.log_area.append(f'Transação enviada. Hash: {tx_hash}')
        except Exception as e:
            self.log_area.append(f'Erro ao enviar a transação: {e}')

    def sell_token(self):
        token_address = self.token_addr_input.text()
        slippage = self.slippage_input.value()
        gwei = self.gwei_input.value()

        if not token_address:
            self.log_area.append('Erro: Por favor, insira o endereço do token.')
            return

        # Exemplo de log de transação
        self.log_area.append(f'Iniciando a venda do token: {token_address}')
        self.log_area.append(f'Slippage definido: {slippage}%')
        self.log_area.append(f'Gas Price definido: {gwei} Gwei')

        # Lógica para enviar a transação (adicionar lógica real aqui)
        try:
            # Transação simulada para fins de demonstração
            tx_hash = '0x456def...'  # Substituir pela chamada real de `web3.eth.sendTransaction()`
            self.log_area.append(f'Transação enviada. Hash: {tx_hash}')
        except Exception as e:
            self.log_area.append(f'Erro ao enviar a transação: {e}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = TradingBotApp()
    mainWin.show()
    sys.exit(app.exec_())
