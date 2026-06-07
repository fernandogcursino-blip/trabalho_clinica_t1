from datetime import date, time

class Pessoa:
    def __init__(self, nome, celular, cpf):
        self.nome = nome
        self.celular = celular
        self.cpf = cpf


class Paciente(Pessoa):
    def __init__(self, nome, celular, cpf, data_nascimento):
        super().__init__(nome, celular, cpf)
        self.data_nascimento = data_nascimento


class ProfissionalSaude(Pessoa):
    def __init__(self, nome, celular, cpf, especialidade, registro_profissional):
        super().__init__(nome, celular, cpf)
        self.especialidade = especialidade
        self.registro_profissional = registro_profissional


class Pagamento:
    def __init__(self, data, atendimento, paciente, valor_pago):
        self.data = data
        self.atendimento = atendimento
        self.paciente = paciente
        self.valor_pago = valor_pago


class Dinheiro(Pagamento):
    def __init__(self, data, atendimento, paciente, valor_pago):
        super().__init__(data, atendimento, paciente, valor_pago)


class Pix(Pagamento):
    def __init__(self, data, atendimento, paciente, valor_pago, cpf_pagador):
        super().__init__(data, atendimento, paciente, valor_pago)
        self.cpf_pagador = cpf_pagador


class CartaoCredito(Pagamento):
    def __init__(self, data, atendimento, paciente, valor_pago, numero_cartao, bandeira):
        super().__init__(data, atendimento, paciente, valor_pago)
        self.numero_cartao = numero_cartao
        self.bandeira = bandeira


class Clinica:
    def __init__(self, nome, cidade, descricao):
        self.nome = nome
        self.cidade = cidade
        self.descricao = descricao


class Procedimento:
    def __init__(self, descricao, custo, profissional_responsavel):
        self.descricao = descricao
        self.custo = custo
        self.profissional_responsavel = profissional_responsavel  # Associação


class Atendimento:
    def __init__(self, clinica, paciente, profissional, data, horario_inicio, horario_fim, tipo, valor):
        self.clinica = clinica
        self.paciente = paciente
        self.profissional = profissional
        self.data = data
        self.horario_inicio = horario_inicio
        self.horario_fim = horario_fim
        self.tipo = tipo
        self.valor = valor
        
        
        self.procedimentos_realizados = []
        self.pagamentos_realizados = []

#fim parcial 1