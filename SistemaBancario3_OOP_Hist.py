from abc import ABC, abstractmethod
from datetime import datetime

# Classe para registrar o histórico de transações da conta
class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar(self, transacao):
        self.transacoes.append({
            'tipo': transacao.__class__.__name__,
            'valor': transacao.valor,
            'data': datetime.now()
        })

    def mostrar(self):
        if not self.transacoes:
            print("Nenhuma transação realizada.")
            return
        print("\nHistórico de Transações:")
        for t in self.transacoes:
            print(f"{t['data'].strftime('%d/%m/%Y %H:%M:%S')} - {t['tipo']}: R$ {t['valor']:.2f}")

# Classe abstrata para transações
class Transacao(ABC):
    def __init__(self, valor):
        self.valor = valor

    @abstractmethod
    def registrar(self, conta):
        pass

# Transação de saque
class Saque(Transacao):
    def registrar(self, conta):
        if self.valor <= 0:
            print("Valor inválido para saque.")
            return False
        if self.valor > conta.saldo:
            print("Saldo insuficiente para saque.")
            return False
        conta._saldo -= self.valor
        conta.historico.adicionar(self)
        print(f"Saque de R$ {self.valor:.2f} realizado com sucesso.")
        return True

# Transação de depósito
class Deposito(Transacao):
    def registrar(self, conta):
        if self.valor <= 0:
            print("Valor inválido para depósito.")
            return False
        conta._saldo += self.valor
        conta.historico.adicionar(self)
        print(f"Depósito de R$ {self.valor:.2f} realizado com sucesso.")
        return True

# Cliente (pessoa física)
class Cliente:
    def __init__(self, nome, cpf, endereco):
        self.nome = nome
        self.cpf = cpf
        self.endereco = endereco
        self.contas = []

    def vincular_conta(self, conta):
        self.contas.append(conta)

    def executar_transacao(self, conta, transacao):
        return transacao.registrar(conta)

# Conta bancária
class Conta:
    def __init__(self, numero, cliente):
        self._numero = numero
        self._saldo = 0
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

# Exemplo de uso
if __name__ == "__main__":
    cliente1 = Cliente("João Silva", "123.456.789-00", "Rua A, 123")
    conta1 = Conta("1001", cliente1)
    cliente1.vincular_conta(conta1)

    deposito1 = Deposito(500)
    cliente1.executar_transacao(conta1, deposito1)

    saque1 = Saque(200)
    cliente1.executar_transacao(conta1, saque1)

    saque2 = Saque(400)
    cliente1.executar_transacao(conta1, saque2)  # Deve falhar (saldo insuficiente)

    conta1.historico.mostrar()
    print(f"\nSaldo atual: R$ {conta1.saldo:.2f}")
