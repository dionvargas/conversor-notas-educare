# Conversor de Notas: Moodle ➔ Educare (UNOESC)

Utilitário em Python com interface gráfica para converter relatórios de notas exportados do Moodle/UNOESC (`.ods` ou `.xlsx`) em arquivos CSV compatíveis com a importação direta no ambiente virtual Educare.

---
## ⚡ Download Rápido (Sem instalação)

Se você é professor e quer apenas utilizar o programa:

1. Acesse a página de [**Releases**](https://github.com/dionvargas/conversor-notas-educare/releases/latest).
2. Baixe o arquivo **`ConversorNotasUNOESC.exe`**.
3. Dê dois cliques para executar (não precisa ter Python instalado).

> **Aviso do Windows Defender:** Como o executável não possui assinatura digital paga de certificado, o Windows pode exibir uma tela azul avisando sobre arquivo desconhecido. Clique em **"Mais informações" ➔ "Executar assim mesmo"**.

---
## 🖥️ Como Usar a Ferramenta

1. Clique em "Selecionar..." e aponte para a planilha baixada do Moodle/sistema acadêmico (.ods ou .xlsx).
2. No campo "Nome da atividade no Moodle", informe o nome exato da atividade cadastrada no livro de notas (por padrão, vem sugerido notas).
3. Clique em "GERAR ARQUIVO CSV".
4. Escolha onde salvar o arquivo final.
5. Acesse o Moodle/Educare e importe o CSV gerado na aba de importação de notas.
---
## 🎯 Objetivo

Eliminar o trabalho braçal de conferência e digitação manual de notas ao final de etapas e bimestres. O programa extrai os dados, identifica automaticamente colunas de notas e e-mails institucionais, extrai a matrícula do acadêmico e formata o CSV de importação pronto para envio.

---

## ✨ Funcionalidades

* **Suporte a múltiplos formatos:** Lê arquivos `.ods` (via parsing nativo de XML sem dependências pesadas) e `.xlsx` (via `pandas` / `openpyxl`).
* **Identificação inteligente de colunas:** Detecta automaticamente variações como *Real*, *Nota*, *Grade*, *Teams*, *E-mail*, etc.
* **Tratamento de faltas/ausências:** Converte células vazias, hifens (`-`) e valores inválidos para o padrão numérico `0.00`.
* **Interface gráfica limpa:** Desenvolvida em Tkinter, acessível para usuários de qualquer área sem necessidade de interação com terminal.

---

## 🛠️ Guia para Desenvolvedores e Contribuidores

Se você quer modificar as regras de negócio, melhorar a interface ou rodar via código-fonte:

### 1. Estrutura do Projeto (MVC)

```text
conversor-notas-moodle/
│
├── main.py                  # Ponto de entrada (conecta Model, View e Controller)
├── requirements.txt         # Dependências do projeto
├── README.md                # Documentação
│
└── src/
    ├── __init__.py          # Exporta os módulos principais
    ├── model.py             # Lógica de negócio, parsing ODS/XML e formatação
    ├── view.py              # Interface gráfica (Tkinter) e diálogos
    └── controller.py        # Mediação de eventos entre a View e o Model
```

### 2. Pré-requisitos
* Python 3.10 ou superior instalado.
* Git instalado.

### 3. Clonando o repositório
Clone o repositório e instale as dependências:

```bash
git clone [https://github.com/dionvargas/conversor-notas-educare](https://github.com/dionvargas/conversor-notas-educare)
cd conversor-notas-educare
```

### 3. Instalando as dependências

Crie um ambiente virtual (opcional, mas recomendado) e instale os pacotes:

```bash
# Criar ambiente virtual
python -m venv .venv

# Ativar no Windows:
.venv\Scripts\activate
# Ativar no Linux/macOS:
source .venv/bin/activate

# Instalar bibliotecas
pip install -r requirements.txt
```

### 4. Executando o aplicativo
Na raiz do repositório, rode:

```bash
python main.py
```

---
## 🤝 Contribuindo

Pull requests com melhorias na interface, suporte a novos formatos de relatórios institucionais ou tratamento de exceções são bem-vindos!

1. Faça um Fork do projeto.
2. Crie uma branch para sua funcionalidade (git checkout -b feature/nova-funcionalidade).
3. Commit suas alterações (git commit -m 'Adiciona suporte a novo formato').
4. Envie para o branch (git push origin feature/nova-funcionalidade).
5. Abra um Pull Request.

---
## 📄 Licença

Distribuído sob a licença MIT. Consulte [LICENSE](./LICENSE) para mais detalhes.