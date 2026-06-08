from datetime import date, time
from model import Clinica, Paciente, ProfissionalSaude, TipoAtendimento, Atendimento, Procedimento, Dinheiro, Pix, CartaoCredito
from view import ViewPrincipal, ViewCadastro, ViewRegistro, ViewRelatorio

class ControladorPrincipal:
    def __init__(self):
        self.__view_principal = ViewPrincipal()
        self.__view_cadastro = ViewCadastro()
        self.__view_registro = ViewRegistro()
        self.__view_relatorio = ViewRelatorio()
        
        # Horário funcionamento clínica - 8 às 20h
        self.__clinicas = [Clinica("Clínica Central Sul", "Florianópolis", "Atendimento Geral", time(8, 0), time(20, 0))]
        self.__pacientes = []
        self.__profissionais = []
        self.__tipos_atendimento = [TipoAtendimento("Consulta"), TipoAtendimento("Exame")]
        self.__atendimentos = []

    def iniciar_sistema(self):
        while True:
            opcao = self.__view_principal.exibir_menu_principal()
            if opcao == 1:
                self.__loop_cadastro()
            elif opcao == 2:
                self.__loop_registro()
            elif opcao == 3:
                self.__loop_relatorio()
            elif opcao == 0:
                break

    def __loop_cadastro(self):
        while True:
            op = self.__view_cadastro.exibir_menu()
            if op == 1:  # Inclusão Paciente
                d = self.__view_cadastro.obter_dados_paciente()
                if any(p.cpf == d["cpf"] for p in self.__pacientes):
                    self.__view_principal.exibir_erro("CPF de paciente já cadastrado.")
                    continue
                self.__pacientes.append(Paciente(d["nome"], d["celular"], d["cpf"], d["data_nascimento"]))
                self.__view_principal.exibir_mensagem("Paciente incluído com sucesso!")
            elif op == 2:  # Listagem Pacientes
                print("\n=== LISTA DE PACIENTES ===")
                for p in self.__pacientes:
                    m = "Sim" if p.eh_maior_de_idade else "Não"
                    print(f"Nome: {p.nome} | CPF: {p.cpf} | Maior de Idade: {m}")
                input("\nPressione Enter...")
            elif op == 3:  # Alteração Paciente
                cpf = input("Digite o CPF do paciente a alterar: ").strip()
                pac = next((p for p in self.__pacientes if p.cpf == cpf), None)
                if not pac:
                    self.__view_principal.exibir_erro("Paciente não encontrado.")
                    continue
                d = self.__view_cadastro.obter_dados_paciente()
                pac.nome, pac.celular, pac.data_nascimento = d["nome"], d["celular"], d["data_nascimento"]
                self.__view_principal.exibir_mensagem("Cadastro alterado com sucesso!")
            elif op == 4:  # Exclusão Paciente
                cpf = input("Digite o CPF para exclusão: ").strip()
                pac = next((p for p in self.__pacientes if p.cpf == cpf), None)
                if pac:
                    self.__pacientes.remove(pac)
                    self.__view_principal.exibir_mensagem("Paciente removido!")
                else:
                    self.__view_principal.exibir_erro("Paciente não encontrado.")
            elif op == 5:  # Inclusão Profissional
                d = self.__view_cadastro.obter_dados_profissional()
                if any(pr.cpf == d["cpf"] for pr in self.__profissionais):
                    self.__view_principal.exibir_erro("CPF de profissional já cadastrado.")
                    continue
                self.__profissionais.append(ProfissionalSaude(d["nome"], d["celular"], d["cpf"], d["especialidade"], d["registro_profissional"]))
                self.__view_principal.exibir_mensagem("Profissional cadastrado com sucesso!")
            elif op == 6:  # Listagem Profissionais
                print("\n=== LISTA DE PROFISSIONAIS ===")
                for pr in self.__profissionais:
                    print(f"Dr(a). {pr.nome} | Especialidade: {pr.especialidade} | Registro: {pr.registro_profissional}")
                input("\nPressione Enter...")
            elif op == 7:  # Inclusão Tipo Atendimento
                nome = input("Nome do novo tipo de atendimento: ").strip()
                self.__tipos_atendimento.append(TipoAtendimento(nome))
                self.__view_principal.exibir_mensagem("Tipo incluído com sucesso!")
            elif op == 8:  # Listagem Tipos
                print("\n=== TIPOS DE ATENDIMENTO CRIADOS ===")
                for t in self.__tipos_atendimento: 
                    print(f"- {t.nome}")
                input("\nPressione Enter...")
            elif op == 9:  # Alterar dados da Clínica
                print("\n=== ALTERAR DADOS DA CLÍNICA ===")
                c = self.__clinicas[0]
                c.nome = input(f"Novo nome ({c.nome}): ").strip() or c.nome
                c.localizacao_cidade = input(f"Nova cidade ({c.localizacao_cidade}): ").strip() or c.localizacao_cidade
                self.__view_principal.exibir_mensagem("Dados da clínica atualizados!")
            elif op == 0:
                break

    def __loop_registro(self):
        while True:
            op = self.__view_registro.exibir_menu()
            if op == 1:  # Agendar Atendimento
                d = self.__view_registro.obter_dados_atendimento()
                if not d: continue
                pac = next((p for p in self.__pacientes if p.cpf == d["cpf_paciente"]), None)
                profissional = next((p for p in self.__profissionais if p.cpf == d["cpf_profissional"]), None)
                tipo = next((t for t in self.__tipos_atendimento if t.nome.lower() == d["tipo"].lower()), None)
                
                if not pac or not profissional or not tipo:
                    self.__view_principal.exibir_erro("Paciente, Profissional ou Tipo não localizado.")
                    continue
                
                if not pac.eh_maior_de_idade:
                    self.__view_principal.exibir_erro("Paciente menor de idade não pode agendar atendimento de forma independente.")
                    continue
                
                try:
                    novo_at = Atendimento(self.__clinicas[0], pac, profissional, d["data"], d["inicio"], d["fim"], tipo, d["valor_base"])
                    self.__atendimentos.append(novo_at)
                    self.__view_principal.exibir_mensagem("Atendimento agendado com sucesso!")
                except ValueError as e:
                    self.__view_principal.exibir_erro(str(e))
                    
            elif op == 2:  # Listar Atendimentos
                print("\n=== ATENDIMENTOS AGENDADOS ===")
                if not self.__atendimentos:
                    print("Nenhum atendimento registrado.")
                for i, a in enumerate(self.__atendimentos):
                    print(f"[{i}] Data: {a.data} | Paciente: {a.paciente.nome} | Médico: {a.profissional.nome} | Total: R${a.calcular_valor_total()} | Restante: R${a.calcular_valor_restante()}")
                input("\nPressione Enter...")
                
            elif op == 3:  # Inserir Procedimento
                if not self.__atendimentos: 
                    self.__view_principal.exibir_erro("Não há atendimentos registrados.")
                    continue
                try:
                    idx = int(input("Digite o índice do Atendimento: "))
                    if idx < 0 or idx >= len(self.__atendimentos): 
                        self.__view_principal.exibir_erro("Índice inválido.")
                        continue
                except ValueError:
                    self.__view_principal.exibir_erro("Digite um número válido.")
                    continue

                d = self.__view_registro.obter_dados_procedimento()
                profissional = next((p for p in self.__profissionais if p.cpf == d["cpf_responsavel"]), None)
                if not profissional: 
                    self.__view_principal.exibir_erro("Profissional Responsável não localizado.")
                    continue
                
                self.__atendimentos[idx].adicionar_procedimento(Procedimento(d["descricao"], d["custo"], prof))
                self.__view_principal.exibir_mensagem("Procedimento adicionado com sucesso!")
                
            elif op == 4:  # Registrar Pagamento
                if not self.__atendimentos: 
                    self.__view_principal.exibir_erro("Não há atendimentos registrados.")
                    continue
                try:
                    idx = int(input("Digite o índice do Atendimento: "))
                    if idx < 0 or idx >= len(self.__atendimentos): 
                        self.__view_principal.exibir_erro("Índice inválido.")
                        continue
                except ValueError:
                    self.__view_principal.exibir_erro("Digite um número válido.")
                    continue

                d = self.__view_registro.obter_dados_pagamento()
                
                try:
                    if d["modalidade"] == 1:
                        pag = Dinheiro(d["data"], d["valor"])
                    elif d["modalidade"] == 2:
                        pag = Pix(d["data"], d["valor"], d["cpf_pagador"])
                    else:
                        pag = CartaoCredito(d["data"], d["valor"], d["numero_cartao"], d["bandeira"])
                    
                    self.__atendimentos[idx].registrar_pagamento(pag)
                    self.__view_principal.exibir_mensagem("Pagamento computado com sucesso!")
                except ValueError as e:
                    self.__view_principal.exibir_erro(str(e))

            elif op == 5:  # Alterar Detalhes
                self.__view_principal.exibir_mensagem("Funcionalidade em desenvolvimento de refatoração.")

            elif op == 6:  # Cancelar/Excluir
                try:
                    idx = int(input("Índice do atendimento para remoção: "))
                    if 0 <= idx < len(self.__atendimentos):
                        self.__atendimentos.pop(idx)
                        self.__view_principal.exibir_mensagem("Atendimento cancelado com sucesso!")
                    else:
                        self.__view_principal.exibir_erro("Índice não localizado.")
                except ValueError:
                    self.__view_principal.exibir_erro("Entrada inválida.")
            elif op == 0:
                break

    def __loop_relatorio(self):
        while True:
            op = self.__view_relatorio.exibir_menu()
            if op == 1:
                print(f"\n--- RELATÓRIO: MOVIMENTAÇÃO POR CLÍNICA ---")
                for c in self.__clinicas:
                    qtd = sum(1 for a in self.__atendimentos if a.clinica == c)
                    print(f"Clínica: {c.nome} | Total Atendimentos: {qtd}")
                input("\nPressione Enter...")
            elif op == 2:
                if not self.__atendimentos: 
                    print("Nenhum atendimento registrado."); input(); continue
                ordenados = sorted(self.__atendimentos, key=lambda x: x.calcular_valor_total())
                print(f"\nATENDIMENTO MAIS BARATO: Paciente {ordenados[0].paciente.nome} - R$ {ordenados[0].calcular_valor_total():.2f}")
                print(f"ATENDIMENTO MAIS CARO: Paciente {ordenados[-1].paciente.nome} - R$ {ordenados[-1].calcular_valor_total():.2f}")
                input("\nPressione Enter...")
            elif op == 3:
                procedimentos_gerais = []
                for a in self.__atendimentos: 
                    procedimentos_gerais.extend(a.procedimentos)
                if not procedimentos_gerais: 
                    print("Nenhum procedimento executado."); input(); continue
                contagem = {}
                for p in procedimentos_gerais: 
                    contagem[p.descricao] = contagem.get(p.descricao, 0) + 1
                mais_pop = max(contagem, key=contagem.get)
                print(f"\nProcedimento mais realizado (Popular): {mais_pop} ({contagem[mais_pop]} vezes)")
                input("\nPressione Enter...")
            elif op == 4:
                procedimentos_gerais = []
                for a in self.__atendimentos: 
                    procedimentos_gerais.extend(a.procedimentos)
                if not procedimentos_gerais: 
                    print("Nenhum procedimento executado."); input(); continue
                ordenados_p = sorted(procedimentos_gerais, key=lambda x: x.custo)
                print(f"\nPROCEDIMENTO MAIS BARATO: {ordenados_p[0].descricao} - R$ {ordenados_p[0].custo:.2f}")
                print(f"PROCEDIMENTO MAIS CARO: {ordenados_p[-1].descricao} - R$ {ordenados_p[-1].custo:.2f}")
                input("\nPressione Enter...")
            elif op == 0:
                break