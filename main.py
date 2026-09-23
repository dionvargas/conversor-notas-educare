import csv
import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import xml.etree.ElementTree as ET
import zipfile
import pandas as pd


def processar_ods(caminho_ods):
    """Extrai os dados diretamente do XML do ODS sem dependências extras."""
    with zipfile.ZipFile(caminho_ods, "r") as z:
        content = z.read("content.xml")

    root = ET.fromstring(content)
    ns = {
        "table": "urn:oasis:names:tc:opendocument:xmlns:table:1.0",
        "text": "urn:oasis:names:tc:opendocument:xmlns:text:1.0",
    }

    rows = []
    for table in root.findall(".//table:table", ns):
        for tr in table.findall(".//table:table-row", ns):
            row_data = []
            for tc in tr.findall(".//table:table-cell", ns):
                repeat = int(
                    tc.attrib.get(f"{{{ns['table']}}}number-columns-repeated", 1)
                )
                texts = [p.text for p in tc.findall(".//text:p", ns) if p.text]
                cell_text = " ".join(texts) if texts else ""
                if repeat > 50:
                    continue
                for _ in range(repeat):
                    row_data.append(cell_text)
            if any(row_data):
                rows.append(row_data)

    header = rows[0]
    return pd.DataFrame(rows[1:], columns=header[: len(rows[1])])


def converter_arquivo(caminho_origem, caminho_destino, nome_atividade):
    """Lê a planilha de origem (.ods ou .xlsx) e gera o CSV formatado."""
    ext = os.path.splitext(caminho_origem)[1].lower()

    if ext == ".ods":
        df = processar_ods(caminho_origem)
    else:
        df = pd.read_excel(caminho_origem)

    # Identificar colunas de Nota e Email dinamicamente
    col_nota = [
        c for c in df.columns if any(k in c.lower() for k in ["real", "nota", "grade"])
    ][0]
    col_email = [
        c
        for c in df.columns
        if any(k in c.lower() for k in ["teams", "email", "correio", "endereço"])
    ][0]

    with open(caminho_destino, "w", encoding="utf-8", newline="") as f:
        # Cabeçalho exigido pelo Moodle
        f.write(
            f'Nome,Sobrenome,"Número de identificação","Conta Microsoft Teams","{nome_atividade} (Real)"\n'
        )
        writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)

        for _, row in df.iterrows():
            nome = str(row["Nome"]).strip()
            sobrenome = str(row["Sobrenome"]).strip()
            email = str(row[col_email]).strip()

            # Extração da matrícula do e-mail institucional
            mat_match = re.findall(r"\d+", email)
            matricula = mat_match[0] if mat_match else ""

            # Tratamento da nota com preenchimento de 0.00 para ausências
            nota_raw = str(row[col_nota]).strip()
            if nota_raw == "-" or not nota_raw or nota_raw.lower() == "nan":
                nota_val = 0.0
            else:
                try:
                    nota_val = float(nota_raw.replace(",", "."))
                except ValueError:
                    nota_val = 0.0

            nota_fmt = f"{nota_val:.2f}"
            writer.writerow([nome, sobrenome, matricula, email, nota_fmt])

    return len(df)


class AppConversor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Conversor de Notas - UNOESC / Moodle")
        self.geometry("580x360")
        self.resizable(False, False)

        # Configuração de estilo visual
        self.configure(bg="#F4F6F9")
        style = ttk.Style(self)
        style.theme_use("clam")

        # Cabeçalho
        header_frame = tk.Frame(self, bg="#0A3A60", height=60)
        header_frame.pack(fill="x")
        header_lbl = tk.Label(
            header_frame,
            text="Exportador de Notas para Importação no Moodle",
            font=("Segoe UI", 13, "bold"),
            fg="white",
            bg="#0A3A60",
        )
        header_lbl.pack(pady=15)

        # Corpo principal
        body_frame = tk.Frame(self, bg="#F4F6F9", padx=25, pady=20)
        body_frame.pack(fill="both", expand=True)

        # 1. Seleção de Arquivo
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
            command=self.selecionar_arquivo,
        )
        btn_procurar.grid(row=1, column=1)

        # 2. Nome da Atividade de Destino
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

        # 3. Barra de Status / Informações
        self.lbl_status = tk.Label(
            body_frame,
            text="Selecione o arquivo de notas para começar.",
            font=("Segoe UI", 8, "italic"),
            bg="#F4F6F9",
            fg="#666",
        )
        self.lbl_status.grid(
            row=4, column=0, columnspan=2, sticky="w", pady=(15, 0)
        )

        # Botão Principal de Conversão
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
            command=self.executar_conversao,
        )
        btn_converter.pack(fill="x", padx=25, pady=(0, 20), ipady=6)

    def selecionar_arquivo(self):
        caminho = filedialog.askopenfilename(
            title="Selecione a planilha de notas",
            filetypes=[
                ("Planilhas Moodle", "*.ods *.xlsx *.xls"),
                ("OpenDocument (.ods)", "*.ods"),
                ("Excel (.xlsx)", "*.xlsx"),
            ],
        )
        if caminho:
            self.entry_arquivo.delete(0, tk.END)
            self.entry_arquivo.insert(0, caminho)
            self.lbl_status.config(
                text=f"Arquivo selecionado: {os.path.basename(caminho)}",
                fg="#16A34A",
            )

    def executar_conversao(self):
        origem = self.entry_arquivo.get().strip()
        atividade = self.entry_atividade.get().strip()

        if not origem:
            messagebox.showwarning(
                "Atenção", "Por favor, selecione o arquivo de notas primeiro."
            )
            return

        if not os.path.exists(origem):
            messagebox.showerror(
                "Erro", "O arquivo especificado não foi encontrado."
            )
            return

        if not atividade:
            messagebox.showwarning(
                "Atenção", "Informe o nome da atividade no Moodle."
            )
            return

        # Pede onde salvar o CSV
        sugestao_nome = f"{atividade.lower().replace(' ', '_')}.csv"
        destino = filedialog.asksaveasfilename(
            title="Salvar CSV de Importação",
            initialfile=sugestao_nome,
            defaultextension=".csv",
            filetypes=[("Arquivo CSV (UTF-8)", "*.csv")],
        )

        if not destino:
            return

        try:
            total = converter_arquivo(origem, destino, atividade)
            messagebox.showinfo(
                "Sucesso!",
                f"Arquivo gerado com sucesso!\n\n"
                f"• Total de alunos: {total}\n"
                f"• Salvo em:\n{destino}\n\n"
                f"O arquivo já está pronto para importação no Moodle.",
            )
            self.lbl_status.config(
                text=f"Sucesso: {total} alunos exportados para {os.path.basename(destino)}",
                fg="#15803D",
            )
        except Exception as e:
            messagebox.showerror(
                "Erro no Processamento",
                f"Ocorreu um erro ao converter os dados:\n{str(e)}",
            )


if __name__ == "__main__":
    app = AppConversor()
    app.mainloop()