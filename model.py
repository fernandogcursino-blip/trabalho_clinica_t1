from abc import ABC, abstractmethod
from datetime import date, time
from typing import List

class Pessoa(ABC):
    def __init__(self, nome: str, celular: str, cpf: str):
        self.__nome = nome
        self.__celular = celular
        self.__cpf = cpf

    @property
    def nome(self) -> str: return self.__nome
    @nome.setter
    def nome(self, value: str): self.__nome = value

    @property
    def celular(self) -> str: return self.__celular
    @celular.setter
    def celular(self, value: str): self.__celular = value

    @property
    def cpf(self) -> str: return self.__cpf
    @cpf.setter
    def cpf(self, value: str): self.__cpf = value


class Paciente(Pessoa):
    def __init__(self, nome: str, celular: str, cpf: str, data_nascimento: date):
        super().__init__(nome, celular, cpf)
        self.__data_nascimento = data_nascimento

    @property
    def data_nascimento(self) -> date: return self.__data_nascimento
    @data_nascimento.setter
    def data_nascimento(self, value: date): self.__data_nascimento = value

    @property
    def eh_maior_de_idade(self) -> bool:
        hoje = date.today()
        idade = hoje.year - self.__data_nascimento.year - (
            (hoje.month, hoje.day) < (self.__data_nascimento.month, self.__data_nascimento.day)
        )
        return idade >= 18


class ProfissionalSaude(Pessoa):
    def __init__(self, nome: str, celular: str, cpf: str, especialidade: str, registro_profissional: str):
        super().__init__(nome, celular, cpf)
        self.__especialidade = especialidade
        self.__registro_profissional = registro_profissional

    @property
    def especialidade(self) -> str: return self.__especialidade
    @especialidade.setter
    def especialidade(self, value: str): self.__especialidade = value

    @property
    def registro_profissional(self) -> str: return self.__registro_profissional
    @registro_profissional.setter
    def registro_profissional(self, value: str): self.__registro_profissional = value


class Pagamento(ABC):
    def __init__(self, data: date, valor_pago: float):
        self.__data = data
        self.__valor_pago = valor_pago

    @property
    def data(self) -> date: return self.__data
    @data.setter
    def data(self, value: date): self.__data = value

    @property
    def valor_pago(self) -> float: return self.__valor_pago
    @valor_pago.setter
    def valor_pago(self, value: float): self.__valor_pago = value


class Dinheiro(Pagamento):
    def __init__(self, data: date, valor_pago: float):
        super().__init__(data, valor_pago)


class Pix(Pagamento):
    def __init__(self, data: date, valor_pago: float, cpf_pagador: str):
        super().__init__(data, valor_pago)
        self.__cpf_pagador = cpf_pagador

    @property
    def cpf_pagador(self) -> str: return self.__cpf_pagador
    @cpf_pagador.setter
    def cpf_pagador(self, value: str): self.__cpf_pagador = value


class CartaoCredito(Pagamento):
    def __init__(self, data: date, valor_pago: float, numero_cartao: str, bandeira: str):
        super().__init__(data, valor_pago)
        self.__numero_cartao = numero_cartao
        self.__bandeira = bandeira

    @property
    def numero_cartao(self) -> str: return self.__numero_cartao
    @numero_cartao.setter
    def numero_cartao(self, value: str): self.__numero_cartao = value

    @property
    def bandeira(self) -> str: return self.__bandeira
    @bandeira.setter
    def bandeira(self, value: str): self.__bandeira = value


class Clinica:
    def __init__(self, nome: str, localizacao_cidade: str, descricao: str, horario_abertura: time, horario_fechamento: time):
        self.__nome = nome
        self.__localizacao_cidade = localizacao_cidade
        self.__descricao = descricao
        self.__horario_abertura = horario_abertura
        self.__horario_fechamento = horario_fechamento

    @property
    def nome(self) -> str: return self.__nome
    @nome.setter
    def nome(self, value: str): self.__nome = value

    @property
    def localizacao_cidade(self) -> str: return self.__localizacao_cidade
    @localizacao_cidade.setter
    def localizacao_cidade(self, value: str): self.__localizacao_cidade = value

    @property
    def descricao(self) -> str: return self.__descricao
    @descricao.setter
    def descricao(self, value: str): self.__descricao = value

    @property
    def horario_abertura(self) -> time: return self.__horario_abertura
    @horario_abertura.setter
    def horario_abertura(self, value: time): self.__horario_abertura = value

    @property
    def horario_fechamento(self) -> time: return self.__horario_fechamento
    @horario_fechamento.setter
    def horario_fechamento(self, value: time): self.__horario_fechamento = value


class TipoAtendimento:
    def __init__(self, nome: str):
        self.__nome = nome

    @property
    def nome(self) -> str: return self.__nome
    @nome.setter
    def nome(self, nome: str): self.__nome = nome


class Procedimento:
    def __init__(self, descricao: str, custo: float, profissional_responsavel: ProfissionalSaude):
        self.__descricao = descricao
        self.__custo = custo
        self.__profissional_responsavel = profissional_responsavel

    @property
    def descricao(self) -> str: return self.__descricao
    @descricao.setter
    def descricao(self, value: str): self.__descricao = value

    @property
    def custo(self) -> float: return self.__custo
    @custo.setter
    def custo(self, value: float): self.__custo = value

    @property
    def profissional_responsavel(self) -> ProfissionalSaude: return self.__profissional_responsavel
    @profissional_responsavel.setter
    def profissional_responsavel(self, value: ProfissionalSaude): self.__profissional_responsavel = value


class Atendimento:
    def __init__(self, clinica: Clinica, paciente: Paciente, profissional: ProfissionalSaude, 
                 data: date, horario_inicio: time, horario_fim: time, tipo: TipoAtendimento, valor_base: float):
        
        if horario_inicio < clinica.horario_abertura or horario_fim > clinica.horario_fechamento:
            raise ValueError("O horário do atendimento está fora do período de funcionamento da clínica.")

        self.__clinica = clinica
        self.__paciente = paciente
        self.__profissional = profissional
        self.__data = data
        self.__horario_inicio = horario_inicio
        self.__horario_fim = horario_fim
        self.__tipo = tipo
        self.__valor_base = valor_base
        self.__procedimentos: List[Procedimento] = []
        self.__pagamentos: List[Pagamento] = []

    @property
    def clinica(self) -> Clinica: return self.__clinica
    @clinica.setter
    def clinica(self, value: Clinica): self.__clinica = value

    @property
    def paciente(self) -> Paciente: return self.__paciente
    @paciente.setter
    def paciente(self, value: Paciente): self.__paciente = value

    @property
    def profissional(self) -> ProfissionalSaude: return self.__profissional
    @profissional.setter
    def profissional(self, value: ProfissionalSaude): self.__profissional = value

    @property
    def data(self) -> date: return self.__data
    @data.setter
    def data(self, value: date): self.__data = value

    @property
    def horario_inicio(self) -> time: return self.__horario_inicio
    @horario_inicio.setter
    def horario_inicio(self, value: time): self.__horario_inicio = value

    @property
    def horario_fim(self) -> time: return self.__horario_fim
    @horario_fim.setter
    def horario_fim(self, value: time): self.__horario_fim = value

    @property
    def tipo(self) -> TipoAtendimento: return self.__tipo
    @tipo.setter
    def tipo(self, value: TipoAtendimento): self.__tipo = value

    @property
    def valor_base(self) -> float: return self.__valor_base
    @valor_base.setter
    def valor_base(self, value: float): self.__valor_base = value

    @property
    def procedimentos(self) -> List[Procedimento]: return self.__procedimentos

    @property
    def pagamentos(self) -> List[Pagamento]: return self.__pagamentos

    def adicionar_procedimento(self, procedimento: Procedimento):
        self.__procedimentos.append(procedimento)

    def calcular_valor_total(self) -> float:
        return self.__valor_base + sum(p.custo for p in self.__procedimentos)

    def registrar_pagamento(self, pagamento: Pagamento):
        # CORREÇÃO DO PROFESSOR: Tratamento de exceção / Validação de regras
        if pagamento.data > self.__data:
            raise ValueError("O pagamento não pode ser feito após a data do atendimento.")
        if pagamento.valor_pago > self.calcular_valor_restante():
            raise ValueError("Valor pago excede o saldo restante.")
        self.__pagamentos.append(pagamento)

    def calcular_valor_restante(self) -> float:
        return self.calcular_valor_total() - sum(p.valor_pago for p in self.__pagamentos)