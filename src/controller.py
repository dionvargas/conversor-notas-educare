import os
import xml.etree.ElementTree as ET

from src.model import GradeConverterModel
from src.view import GradeConverterView

class GradeConverterController:
    """Orquestra as entradas do usuário, invoca o Model e atualiza a View."""

    def __init__(self, model: GradeConverterModel, view: GradeConverterView):
        self.model = model
        self.view = view

        # Conecta as ações da interface aos métodos do Controller
        self.view.set_controller_callbacks(
            on_select_file=self.selecionar_arquivo,
            on_execute_conversion=self.executar_conversao,
        )

    def selecionar_arquivo(self):
        caminho = self.view.abrir_seletor_arquivo()
        if caminho:
            self.view.set_caminho_arquivo(caminho)
            nome_arq = os.path.basename(caminho)
            self.view.set_status(f"Arquivo selecionado: {nome_arq}", cor="#16A34A")

    def executar_conversao(self):
        origem = self.view.get_caminho_arquivo()
        atividade = self.view.get_nome_atividade()

        # Validações de entrada
        if not origem:
            self.view.mostrar_alerta("Atenção", "Por favor, selecione o arquivo de notas primeiro.")
            return

        if not os.path.exists(origem):
            self.view.mostrar_erro("Erro", "O arquivo especificado não foi encontrado.")
            return

        if not atividade:
            self.view.mostrar_alerta("Atenção", "Informe o nome da atividade no Moodle.")
            return

        # Pede destino
        sugestao_nome = f"{atividade.lower().replace(' ', '_')}.csv"
        destino = self.view.abrir_seletor_destino(sugestao_nome)
        if not destino:
            return

        # Executa conversão via Model
        try:
            total_alunos = self.model.converter(origem, destino, atividade)
            nome_destino = os.path.basename(destino)
            self.view.mostrar_sucesso(
                "Sucesso!",
                f"Arquivo gerado com sucesso!\n\n"
                f"• Total de alunos: {total_alunos}\n"
                f"• Salvo em:\n{destino}\n\n"
                f"O arquivo já está pronto para importação no Educare.",
            )
            self.view.set_status(
                f"Sucesso: {total_alunos} alunos exportados para {nome_destino}",
                cor="#15803D",
            )
        except Exception as e:
            self.view.mostrar_erro(
                "Erro no Processamento",
                f"Ocorreu um erro ao converter os dados:\n{str(e)}",
            )