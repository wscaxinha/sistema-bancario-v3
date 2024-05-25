from abc import ABC, abstractmethod
import textwrap

class Usuario:
    def __init__(self, nome, data_nascimento, cpf, endereco):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        self.endereco = endereco

    def __str__(self):
        return f"Usuário: {self.nome}, CPF: {self.cpf}"

class ContaBase(ABC):
    def __init__(self, usuario, numero_conta, agencia="0001"):
        self.usuario = usuario
        self.numero_conta = numero_conta
        self.agencia = agencia
        self._saldo = 0.0
        self._extrato = []
        self._numero_saques = 0
        self._limite = 500.0

    @property
    def saldo(self):
        return self._saldo

    @property
    def extrato(self):
        return self._extrato

    @property
    def numero_saques(self):
        return self._numero_saques

    @property
    def limite(self):
        return self._limite

    @abstractmethod
    def depositar(self, valor):
        pass

    @abstractmethod
    def sacar(self, valor):
        pass

    def exibir_extrato(self):
        extrato_str = "\n================ EXTRATO ================\n"
        if not self._extrato:
            extrato_str += "Não foram realizadas movimentações."
        else:
            for transacao in self._extrato:
                extrato_str += f"{transacao}\n"
        extrato_str += f"\nSaldo: R$ {self._saldo:.2f}\n"
        extrato_str += "=========================================="
        return extrato_str

    def __str__(self):
        return f"Conta Nº {self.numero_conta}, Agência: {self.agencia}, Usuário: {self.usuario}"

class Conta(ContaBase):
    LIMITE_SAQUES = 3

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            self._extrato.append(f"{self.usuario.nome}: Depósito: + R$ {valor:.2f}")
            return "\n===== Depósito realizado com sucesso! ====="
        else:
            return """
===== Valor de depósito inválido. Informe um valor válido ===== 
=====    O valor deve ser positivo e maior que zero     =====
"""

    def sacar(self, valor):
        if valor <= 0:
            return """
===== Valor de saque inválido. Informe um valor válido ===== 
=====    O valor deve ser positivo e maior que zero     =====
"""
        if self._numero_saques >= Conta.LIMITE_SAQUES:
            return "\n===== Limite de saques excedido ====="
        if self._saldo >= valor and valor <= self._limite:
            self._saldo -= valor
            self._extrato.append(f"{self.usuario.nome}: Saque:    - R$ {valor:.2f}")
            self._numero_saques += 1
            return f"""
===== Saque realizado com sucesso! =====
===== Saldo em conta: R$ {self._saldo:.2f}    =====
===== Saques restantes: {Conta.LIMITE_SAQUES - self._numero_saques} =====
"""
        elif self._saldo < valor:
            return "\n===== Saldo insuficiente ====="
        else:
            return "\n===== Valor de saque excedeu o limite ====="

class Banco:
    def __init__(self):
        self.usuarios = []
        self.contas = []
        self.numero_conta = 1

    def criar_usuario(self, nome, data_nascimento, cpf, endereco):
        if any(usuario.cpf == cpf for usuario in self.usuarios):
            return "\n===== Usuário já cadastrado com esse CPF ====="
        novo_usuario = Usuario(nome, data_nascimento, cpf, endereco)
        self.usuarios.append(novo_usuario)
        return "\n===== Usuário criado com sucesso! ====="

    def criar_conta(self, cpf):
        usuario = self.buscar_usuario(cpf)
        if usuario:
            nova_conta = Conta(usuario, self.numero_conta)
            self.contas.append(nova_conta)
            self.numero_conta += 1
            return f"\n===== Conta criada com sucesso! =====\n{nova_conta}"
        return "\n===== Usuário não encontrado com o CPF informado ====="

    def buscar_usuario(self, cpf):
        return next((usuario for usuario in self.usuarios if usuario.cpf == cpf), None)

    def buscar_conta(self, numero_conta):
        return next((conta for conta in self.contas if conta.numero_conta == numero_conta), None)

    def listar_contas(self):
        if not self.contas:
            return "\nNão há contas cadastradas."
        for conta in self.contas:
            print("=" * 80)
            print(textwrap.dedent(str(conta)))
        return "=" * 80

def main():
    banco = Banco()
    while True:
        opcao = input(textwrap.dedent("""
        \n=============== MENU ================
        [d] Depositar
        [s] Sacar
        [e] Extrato
        [nc] Nova Conta
        [nu] Novo Usuário
        [lc] Listar Contas
        [q] Sair
        => """))

        if opcao == "d":
            numero_conta = int(input("Informe o número da conta: "))
            conta = banco.buscar_conta(numero_conta)
            if conta:
                valor = float(input("Informe o valor do depósito: R$ "))
                print(conta.depositar(valor))
            else:
                print("\n===== Conta não encontrada =====")

        elif opcao == "s":
            numero_conta = int(input("Informe o número da conta: "))
            conta = banco.buscar_conta(numero_conta)
            if conta:
                valor = float(input("Informe o valor do saque: R$ "))
                print(conta.sacar(valor))
            else:
                print("\n===== Conta não encontrada =====")

        elif opcao == "e":
            numero_conta = int(input("Informe o número da conta: "))
            conta = banco.buscar_conta(numero_conta)
            if conta:
                print(conta.exibir_extrato())
            else:
                print("\n===== Conta não encontrada =====")

        elif opcao == "nc":
            cpf = input("Informe o CPF do usuário para associar à nova conta: ")
            print(banco.criar_conta(cpf))

        elif opcao == "nu":
            nome = input("Informe o nome do usuário: ")
            data_nascimento = input("Data de nascimento (DD/MM/AAAA): ")
            cpf = input("Informe o CPF do usuário (somente o número): ")
            endereco = input("Informe o endereço (Conjunto - Nº, Bairro, Cidade-UF): ")
            print(banco.criar_usuario(nome, data_nascimento, cpf, endereco))

        elif opcao == "lc":
            print(banco.listar_contas())

        elif opcao == "q":
            print("\n===== Obrigado por utilizar nosso banco =====")
            break

        else:
            print("\n===== Operação inválida, por favor selecione novamente a operação desejada =====")

if __name__ == "__main__":
    main()
