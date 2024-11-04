import tkinter as tk
from tkinter import messagebox, ttk
import requests
import json

class CryptoTradingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Crypto Trading App")
        self.root.geometry("400x600")
        self.root.configure(bg="#2E2E2E")  # Cor de fundo

        # Estilo do ttk
        style = ttk.Style()
        style.configure("TLabel", background="#2E2E2E", foreground="#FFFFFF", font=("Arial", 12))
        style.configure("TEntry", background="#3E3E3E", foreground="#FFFFFF", font=("Arial", 12))
        style.configure("TButton", background="#4CAF50", foreground="#FFFFFF", font=("Arial", 12))
        style.map("TButton", background=[("active", "#45A049")])  # Cor ao passar o mouse
        style.configure("TText", background="#3E3E3E", foreground="#FFFFFF", font=("Arial", 12))

        # Campos de entrada
        self.create_input_fields()

        # Botão de negociação
        self.trade_button = ttk.Button(self.root, text="Realizar Negociação", command=self.perform_trade)
        self.trade_button.pack(pady=20)

        # Botão para limpar logs
        self.clear_log_button = ttk.Button(self.root, text="Limpar Log", command=self.clear_log)
        self.clear_log_button.pack(pady=5)

        # Botão para obter logs
        self.get_logs_button = ttk.Button(self.root, text="Obter Logs", command=self.get_logs)
        self.get_logs_button.pack(pady=5)

        # Área de texto para logs
        self.log_area = tk.Text(self.root, height=15, width=50)
        self.log_area.pack(pady=10)

        # Adicionando uma barra de rolagem
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.log_area.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.log_area.config(yscrollcommand=self.scrollbar.set)

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
            frame = ttk.Frame(self.root)
            label = ttk.Label(frame, text=field)
            entry = ttk.Entry(frame)
            label.pack(side=tk.LEFT, padx=5)
            entry.pack(side=tk.RIGHT, padx=5)
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
