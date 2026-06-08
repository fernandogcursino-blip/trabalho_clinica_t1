import os
import subprocess
from datetime import date, time

class ViewPrincipal:
    def exibir_menu_principal(self) -> int:
        self.limpar_tela()
        print("=" * 60)
        print("         SISTEMA DE GESTÃO CLÍNICA - REAVALIAÇÃO MVC        ")
        print("=" * 60)
        print("1. GERENCIAR CADASTROS (Clínicas, Pacientes, Profissionais, Tipos)")
        print("2. GERENCIAR REGISTROS (Atendimentos, Procedimentos, Pagamentos)")
        print("3. EMISSÃO DE RELATÓRIOS GERENCIAIS")
        print("0. SAIR DO SISTEMA")
        print("=" * 60)
        return self.ler_opcao("Escolha uma opção geral: ", [0, 1, 2, 3])
    
    def exibir_mensagem(self, texto: str):
        print(f"\n[INFO] {texto}")
        input("\nPressione [Enter] para continuar...")

    def exibir_erro(self, texto: str):
        print(f"\n[ERRO] {texto}")
        input("\nPressione [Enter] para continuar...")

    def ler_opcao(self, mensagem: str, opcoes_validas: list) -> int:
        while True:
            try:
                opcao = int(input(mensagem))
                if opcao in opcoes_validas:
                    return opcao
                print(f"Opção inválida! Escolha entre {opcoes_validas}.")
            except ValueError:
                print("Por favor, digite um número inteiro válido.")

    def limpar_tela(self):
        comando = "cls" if os.name == "nt" else "clear"
        subprocess.run(comando, shell=True, check=False)


class ViewCadastro:
    def exibir_menu(self) -> int:
        print("\n" + "-" * 45)
        print("          SUBMENU: SUB-SISTEMA DE CADASTROS         ")
        print("-" * 45)
        print("1. Inclusão de Paciente")
        print("2. Listagem de Pacientes")
        print("3. Alteração de Paciente")
        print("4. Exclusão de Paciente")
        print("5. Inclusão de Profissional de Saúde")
        print("6. Listagem de Profissionais")
        print("7. Alteração de Profissional de Saúde")
        print("8. Exclusão de Profissional de Saúde")
        print("9. Alterar Dados da Clínica")
        print("0. Voltar ao Menu Principal")
        print("-" * 45)
        return ViewPrincipal().ler_opcao("Escolha uma opção de cadastro: ", list(range(10)))

    def obter_dados_paciente(self) -> dict:
        print("\n--- CADASTRO / ALTERAÇÃO DE PACIENTE ---")
        nome = input("Nome completo: ").strip()
        celular = input("Celular: ").strip()
        cpf = input("CPF (apenas números): ").strip()
        while True:
            try:
                print("Data de Nascimento:")
                dia = int(input("  Dia (DD): "))
                mes = int(input("  Mês (MM): "))
                ano = int(input("  Ano (AAAA): "))
                return {"nome": nome, "celular": celular, "cpf": cpf, "data_nascimento": date(ano, mes, dia)}
            except ValueError:
                print("Data inválida! Tente novamente.")

    def obter_dados_profissional(self) -> dict:
        print("\n--- CADASTRO DE PROFISSIONAL DE SAÚDE ---")
        nome = input("Nome do Profissional: ").strip()
        celular = input("Celular: ").strip()
        cpf = input("CPF: ").strip()
        especialidade = input("Especialidade Médica: ").strip()
        registro = input("Registro Profissional (Ex: CRM/COREN): ").strip()
        return {"nome": nome, "celular": celular, "cpf": cpf, "especialidade": especialidade, "registro_profissional": registro}


class ViewRegistro:
    def exibir_menu(self) -> int:
        print("\n" + "#" * 45)
        print("          SUBMENU: SUB-SISTEMA DE REGISTROS         ")
        print("#" * 45)
        print("1. Agendar Novo Atendimento (Consulta/Exame)")
        print("2. Listar Atendimentos Agendados")
        print("3. Registrar Procedimento em Atendimento")
        print("4. Registrar Pagamento de Atendimento")
        print("5. Alterar Detalhes de Atendimento")
        print("6. Cancelar/Excluir Atendimento")
        print("0. Voltar ao Menu Principal")
        print("#" * 45)
        return ViewPrincipal().ler_opcao("Escolha uma opção de registro: ", list(range(7)))

    def obter_dados_atendimento(self) -> dict:
        print("\n--- AGENDAMENTO DE ATENDIMENTO ---")
        cpf_paciente = input("CPF do Paciente: ").strip()
        cpf_prof = input("CPF do Profissional de Saúde: ").strip()
        nome_tipo = input("Nome do Tipo de Atendimento (Ex: Consulta, Exame): ").strip()
        try:
            print("Data do Atendimento:")
            dia = int(input("  Dia (DD): "))
            mes = int(input("  Mês (MM): "))
            ano = int(input("  Ano (AAAA): "))
            
            print("Horário de Início:")
            h_in = int(input("  Hora (HH): "))
            m_in = int(input("  Minuto (MM): "))
            
            print("Horário de Término:")
            h_fim = int(input("  Hora (HH): "))
            m_fim = int(input("  Minuto (MM): "))
            
            valor_base = float(input("Valor Base do Atendimento (R$): "))
            
            return {
                "cpf_paciente": cpf_paciente, "cpf_profissional": cpf_prof, "tipo": nome_tipo,
                "data": date(ano, mes, dia), "inicio": time(h_in, m_in), "fim": time(h_fim, m_fim), "valor_base": valor_base
            }
        except ValueError:
            return {}

    def obter_dados_procedimento(self) -> dict:
        print("\n--- REGISTRO DE PROCEDIMENTO ---")
        descricao = input("Descrição do Serviço realizado: ").strip()
        custo = float(input("Custo Adicional do Procedimento (R$): "))
        cpf_resp = input("CPF do Profissional Responsável: ").strip()
        return {"descricao": descricao, "custo": custo, "cpf_responsavel": cpf_resp}

    def obter_dados_pagamento(self) -> dict:
        print("\n--- REGISTRO DE PAGAMENTO ---")
        print("Escolha a Modalidade:")
        print("  1. Dinheiro\n  2. PIX\n  3. Cartão de Crédito")
        mod = ViewPrincipal().ler_opcao("Opção: ", [1, 2, 3])
        valor = float(input("Valor Pago (R$): "))
        
        while True:
            try:
                print("Data do Pagamento:")
                d = int(input("  Dia: "))
                m = int(input("  Mês: "))
                a = int(input("  Ano: "))
                dt_pag = date(a, m, d)
                break
            except ValueError:
                print("Data Inválida!")

        dados = {"modalidade": mod, "valor": valor, "data": dt_pag}
        if mod == 2:
            dados["cpf_pagador"] = input("CPF do Pagador do PIX: ").strip()
        elif mod == 3:
            dados["numero_cartao"] = input("Número do Cartão de Crédito: ").strip()
            dados["bandeira"] = input("Bandeira do Cartão: ").strip()
        return dados


class ViewRelatorio:
    def exibir_menu(self) -> int:
        print("\n" + "=" * 45)
        print("          PAINEL DE RELATÓRIOS GERENCIAIS         ")
        print("=" * 45)
        print("1. Relatório: Clínicas com Maior Número de Atendimentos")
        print("2. Relatório: Atendimentos Mais Caros e Mais Baratos")
        print("3. Relatório: Procedimentos Mais Realizados (Populares)")
        print("4. Relatório: Procedimentos Mais Caros e Mais Baratos")
        print("0. Voltar ao Menu Principal")
        print("=" * 45)
        return ViewPrincipal().ler_opcao("Escolha o relatório para emissão: ", [0, 1, 2, 3, 4])  