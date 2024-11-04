import tkinter as tk
from tkinter import messagebox
import requests

class CryptoTradingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cripto e Afins Trading App")
        self.root.geometry("800x600")

        # Campos de entrada
        self.create_input_fields()

        # Botão de negociação
        self.trade_button = tk.Button(self.root, text="Realizar Negociação", command=self.perform_trade)
        self.trade_button.pack(pady=20)

        # Botão para limpar logs
        self.clear_log_button = tk.Button(self.root, text="Limpar Log", command=self.clear_log)
        self.clear_log_button.pack(pady=5)

        # Botão para obter logs
        self.get_logs_button = tk.Button(self.root, text="Obter Logs", command=self.get_logs)
        self.get_logs_button.pack(pady=5)

        # Área de texto para logs
        self.log_area = tk.Text(self.root, height=15, width=50)
        self.log_area.pack(pady=10)

    def create_input_fields(self):
        self.inputs = {}
        fields = [
            "Token Address", "Pay Coin", "GWEI to Trade", "Tip (GWEI)",
            "Buy Slippage (%)", "Sell Slippage (%)", "Max Buy Tax (%)",
            "Max Sell Tax (%)", "GWEI to Approve", "Token Amount to Buy",
            "Limit Buy Order", "Limit Sell Order", "Take Profit (%)",
            "Stop Loss (%)", "Wait (s)", "Min Pool Amount",
            "RPC", "Max GAS", "DEX", "Pool", "Pay"
        ]
        
        for field in fields:
            frame = tk.Frame(self.root)
            label = tk.Label(frame, text=field)
            entry = tk.Entry(frame)
            label.pack(side=tk.LEFT)
            entry.pack(side=tk.RIGHT)
            frame.pack(pady=5)
            self.inputs[field] = entry

    def perform_trade(self):
        data = {field: entry.get() for field, entry in self.inputs.items()}
        
        try:
            response = requests.post('http://127.0.0.1:5000/trade', json=data)
            if response.status_code == 200:
                messagebox.showinfo("Sucesso", response.json().get('message', 'Transação realizada com sucesso!'))
            else:
                messagebox.showerror("Erro", response.json().get('error', 'Erro desconhecido.'))
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def clear_log(self):
        try:
            response = requests.post('http://127.0.0.1:5000/clear_log')
            if response.status_code == 200:
                messagebox.showinfo("Sucesso", "Log limpo com sucesso!")
            else:
                messagebox.showerror("Erro", response.json().get('error', 'Erro ao limpar o log.'))
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def get_logs(self):
        try:
            response = requests.get('http://127.0.0.1:5000/get_logs')
            if response.status_code == 200:
                logs = response.json()
                self.log_area.delete(1.0, tk.END)  # Limpa a área de texto
                for log in logs:
                    self.log_area.insert(tk.END, json.dumps(log) + "\n")
            else:
                messagebox.showerror("Erro", response.json().get('error', 'Erro ao obter logs.'))
        except Exception as e:
            messagebox.showerror("Erro", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = CryptoTradingApp(root)
    root.mainloop()
