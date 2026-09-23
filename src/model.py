import csv
import os
import re
import xml.etree.ElementTree as ET
import zipfile
import pandas as pd

class GradeConverterModel:
    """Gerencia a extração, transformação e exportação das notas."""

    @staticmethod
    def processar_ods(caminho_ods: str) -> pd.DataFrame:
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

        if not rows:
            raise ValueError("O arquivo ODS não contém dados legíveis.")

        header = rows[0]
        return pd.DataFrame(rows[1:], columns=header[: len(rows[1])])

    def carregar_dados(self, caminho_origem: str) -> pd.DataFrame:
        """Carrega dados dependendo da extensão do arquivo."""
        ext = os.path.splitext(caminho_origem)[1].lower()
        if ext == ".ods":
            return self.processar_ods(caminho_origem)
        elif ext in [".xlsx", ".xls"]:
            return pd.read_excel(caminho_origem)
        else:
            raise ValueError(f"Extensão de arquivo não suportada: {ext}")

    def converter(self, caminho_origem: str, caminho_destino: str, nome_atividade: str) -> int:
        """Processa a planilha e gera o CSV formatado para o Educare."""
        df = self.carregar_dados(caminho_origem)

        # Identificar colunas de Nota e Email dinamicamente
        cols_nota = [
            c for c in df.columns if any(k in str(c).lower() for k in ["real", "nota", "grade"])
        ]
        cols_email = [
            c for c in df.columns if any(k in str(c).lower() for k in ["teams", "email", "correio", "endereço"])
        ]

        if not cols_nota:
            raise KeyError("Coluna de nota não identificada na planilha de origem.")
        if not cols_email:
            raise KeyError("Coluna de e-mail institucional não identificada na planilha de origem.")

        col_nota = cols_nota[0]
        col_email = cols_email[0]

        with open(caminho_destino, "w", encoding="utf-8", newline="") as f:
            # Cabeçalho exigido pelo Educare
            f.write(
                f'Nome,Sobrenome,"Número de identificação","Conta Microsoft Teams","{nome_atividade} (Real)"\n'
            )
            writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)

            for _, row in df.iterrows():
                nome = str(row.get("Nome", "")).strip()
                sobrenome = str(row.get("Sobrenome", "")).strip()
                email = str(row.get(col_email, "")).strip()

                # Extração da matrícula do e-mail institucional
                mat_match = re.findall(r"\d+", email)
                matricula = mat_match[0] if mat_match else ""

                # Tratamento da nota com preenchimento de 0.00 para ausências
                nota_raw = str(row.get(col_nota, "")).strip()
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