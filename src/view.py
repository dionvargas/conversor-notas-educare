import tkinter as tk
from tkinter import filedialog, messagebox, ttk

class GradeConverterView(tk.Tk):
    """Gerencia apenas os componentes visuais e a interação de tela."""

    def __init__(self):
        super().__init__()
        self.title("Conversor de Notas - UNOESC / Educare")
        self.geometry("580x360")
        self.resizable(False, False)
        self.configure(bg="#F4F6F9")

        # Handlers/Callbacks definidos pelo Controller
        self._on_select_file = None
        self._on_execute_conversion = None

        self._configurar_estilo()
        self._criar_widgets()

    def set_controller_callbacks(self, on_select_file, on_execute_conversion):
        """Associa os comandos de botões às ações do Controller."""
        self._on_select_file = on_select_file
        self._on_execute_conversion = on_execute_conversion

    def _configurar_estilo(self):
        style = ttk.Style(self)
        style.theme_use("clam")

    def _criar_widgets(self):
        # 1. Cabeçalho
        header_frame = tk.Frame(self, bg="#0A3A60", height=60)
        header_frame.pack(fill="x")
        header_lbl = tk.Label(
            header_frame,
            text="Exportador de Notas para Importação do Educare",
            font=("Segoe UI", 13, "bold"),
            fg="white",
            bg="#0A3A60",
        )
        header_lbl.pack(pady=15)

        # 2. Corpo principal
        body_frame = tk.Frame(self, bg="#F4F6F9", padx=25, pady=20)
        body_frame.pack(fill="both", expand=True)

        lbl_arquivo = tk.Label(
            body_frame,
            text="Planilha baixada do Moodle (.ods ou .xlsx):",
            font=("Segoe UI", 9, "bold"),
            bg="#F4F6F9",
            fg="#333",
        )
        lbl_arquivo.grid(row=0, column=0, sticky="w", pady=(0, 4))

        self.entry_arquivo = tk.Entry(
            body_frame, font=("Segoe UI", 9), width=46, relief="solid", bd=1
        )
        self.entry_arquivo.grid(row=1, column=0, padx=(0, 8), ipady=3)

        btn_procurar = tk.Button(
            body_frame,
            text="Selecionar...",
            font=("Segoe UI", 9),
            bg="#E2E8F0",
            relief="groove",
            command=lambda: self._on_select_file() if self._on_select_file else None,
        )
        btn_procurar.grid(row=1, column=1)

        lbl_atividade = tk.Label(
            body_frame,
            text="Nome da atividade no Moodle:",
            font=("Segoe UI", 9, "bold"),
            bg="#F4F6F9",
            fg="#333",
        )
        lbl_atividade.grid(row=2, column=0, sticky="w", pady=(15, 4))

        self.entry_atividade = tk.Entry(
            body_frame, font=("Segoe UI", 9), width=46, relief="solid", bd=1
        )
        self.entry_atividade.insert(0, "notas")
        self.entry_atividade.grid(row=3, column=0, sticky="w", ipady=3)

        self.lbl_status = tk.Label(
            body_frame,
            text="Selecione o arquivo de notas para começar.",
            font=("Segoe UI", 8, "italic"),
            bg="#F4F6F9",
            fg="#666",
        )
        self.lbl_status.grid(row=4, column=0, columnspan=2, sticky="w", pady=(15, 0))

        # 3. Botão de Conversão
        btn_converter = tk.Button(
            self,
            text="GERAR ARQUIVO CSV",
            font=("Segoe UI", 10, "bold"),
            bg="#16A34A",
            fg="white",
            activebackground="#15803D",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=lambda: self._on_execute_conversion() if self._on_execute_conversion else None,
        )
        btn_converter.pack(fill="x", padx=25, pady=(0, 20), ipady=6)

    # Getters e Setters de tela
    def get_caminho_arquivo(self) -> str:
        return self.entry_arquivo.get().strip()

    def set_caminho_arquivo(self, caminho: str):
        self.entry_arquivo.delete(0, tk.END)
        self.entry_arquivo.insert(0, caminho)

    def get_nome_atividade(self) -> str:
        return self.entry_atividade.get().strip()

    def set_status(self, mensagem: str, cor: str = "#666"):
        self.lbl_status.config(text=mensagem, fg=cor)

    # Diálogos de sistema operacional
    def abrir_seletor_arquivo(self) -> str:
        return filedialog.askopenfilename(
            title="Selecione a planilha de notas",
            filetypes=[
                ("Planilhas Moodle", "*.ods *.xlsx *.xls"),
                ("OpenDocument (.ods)", "*.ods"),
                ("Excel (.xlsx)", "*.xlsx"),
            ],
        )

    def abrir_seletor_destino(self, sugestao_nome: str) -> str:
        return filedialog.asksaveasfilename(
            title="Salvar CSV de Importação",
            initialfile=sugestao_nome,
            defaultextension=".csv",
            filetypes=[("Arquivo CSV (UTF-8)", "*.csv")],
        )

    def mostrar_alerta(self, titulo: str, mensagem: str):
        messagebox.showwarning(titulo, mensagem)

    def mostrar_erro(self, titulo: str, mensagem: str):
        messagebox.showerror(titulo, mensagem)

    def mostrar_sucesso(self, titulo: str, mensagem: str):
        messagebox.showinfo(titulo, mensagem)