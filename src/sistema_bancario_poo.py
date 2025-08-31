from abc import ABC, abstractmethod
from datetime import datetime
from functools import wraps
from pathlib import Path

menu = """
[MENU]
[d] Depositar
[s] Sacar
[e] Extrato
[nc] Nova Conta
[nu] Novo Usuário
[lc] Listar contas
[q] Sair

=> """
class ContaIterador:
    def __init__(self,contas):
        self.contas = contas
        self.contador = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            conta = self.contas[self.contador]
            self.contador += 1
            return conta
        except IndexError:
            raise StopIteration
        
#Interface -_> Qualquer coisa que for uma transação no nosso banco precisa obrigatoriamente saber como registrar em uma conta
class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    # Propriedade de acesso público e somente leitura para um atributo que é considerado protegido da classe
    @property # permite que acesse o método 'valor' como se fosse um atributo normal,sem usar ()
    def valor(self) -> float:
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self) -> float:
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append({"tipo": transacao.__class__.__name__,"valor": transacao.valor,"data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),})

    def gerador_relatorio(self,tipo_transacao=None):
        for transacao in self._transacoes:
            if tipo_transacao is None or transacao['tipo'].lower() == tipo_transacao.lower():
                yield transacao

class Conta:
    def __init__(self, numero: int, cliente: 'Cliente', saldo_inicial: float = 0.0):
        self._saldo = float(saldo_inicial)
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente 
        self._historico = Historico()
        self._numero_saques = 0

    @property
    def saldo(self) -> float:
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

    @classmethod
    def nova_conta(cls, cliente: 'Cliente', numero: int):
        return cls(numero, cliente)

    def sacar(self, valor: float) -> bool:
        """
        Realiza um saque na conta. O valor deve ser um float.
        Retorna True se o saque foi bem-sucedido, False caso contrário.
        """

        excedeu_saldo = valor > self._saldo

        if excedeu_saldo:
            print("\nOperação falhou! Você não tem saldo suficiente.")
        elif valor > 0:
            self._saldo -= valor
            self._numero_saques += 1
            print("\n=== Saque realizado com sucesso! ===")
            return True
        else:
            print("\nOperação falhou! O valor informado é inválido.")

        return False

    def depositar(self, valor: float) -> bool:
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
            return True

        print("\n@@@ Operação falhou! O valor informado é inválido.")
        return False

class ContaCorrente(Conta):
    def __init__(self, numero: int, cliente: 'Cliente', limite: float = 500.0, limite_saque: int = 3, saldo_inicial: float = 0.0):
        super().__init__(numero, cliente, saldo_inicial)
        self._limite = limite
        self._limite_saque = limite_saque

    @classmethod
    def nova_conta(cls, cliente: 'Cliente', numero: int, limite: float, limite_saque: int):
        return cls(numero=numero, cliente=cliente, limite=limite, limite_saque=limite_saque)

    def __repr__(self):
        return f'<{self.__class__.__name__} :( {self.numero}, {self.agencia}, {self.cliente})>'
    def sacar(self,valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao['tipo'] == Saque.__name__])

        excedeu_limite = valor > self._limite
        excedeu_numero_saques = numero_saques >= self._limite_saque

        if excedeu_limite:
            print(f"\nOperação falhou! O valor do saque excede o limite de R${self.limite:.2f}.")
        elif excedeu_numero_saques:
            print("\nOperação falhou! Número máximo de saques excedido. @@@")
        else:
            return super().sacar(valor)

        return False

class Cliente:
    def __init__(self,endereco):
        self._endereco = endereco
        self._contas = [] #inicia como vazio

    @property
    def endereco(self):
        return self._endereco
    
    @property
    def contas(self):
        return self._contas

    # Polimorfismo
    def realizar_transacao(self, conta: Conta, transacao: Transacao):
        transacao.registrar(conta)
    
    def adicionar_conta(self, conta: Conta):
        self._contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome: str, data_nascimento: str, cpf: str, endereco: str):
        super().__init__(endereco)
        self._nome = nome
        self._cpf = cpf
        self._data_nascimento = data_nascimento
    
    @property
    def nome(self):
        return self._nome
    
    @property
    def cpf(self):
        return self._cpf

    @property
    def data_nascimento(self):
        return self._data_nascimento
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}: ({self.cpf})'

def log_transacao(funcao):
    @wraps(funcao)
    def wrapper(*args, **kwargs):
        log_file_path = Path(__file__).parent / "log.txt"
        timestamp = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        resultado = funcao(*args, **kwargs)

        with open(log_file_path, 'a', encoding='utf-8') as log_file:
            log_file.write(f"[{timestamp}] Função '{funcao.__name__} exexutada com argumentos {args} e {kwargs}'\n Retornou: {resultado}")
                           
        return resultado
    return wrapper

# Funções de interação com o usuário (adaptadas para POO)
@log_transacao
def depositar_valor(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado!")
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = selecionar_conta_cliente(cliente)
    if conta:
        cliente.realizar_transacao(conta, transacao)

@log_transacao
def sacar_valor(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado!")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = selecionar_conta_cliente(cliente)
    if conta:
        cliente.realizar_transacao(conta, transacao)

@log_transacao
def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado!")
        return

    conta = selecionar_conta_cliente(cliente)
    if not conta:
        return

    print("\n================ EXTRATO ================")

    tipo_filtro = input("Deseja filtrar o extrato? ([d]eposito, [s]aque, ou [N]ão para todos): ").lower()
    filtro = None
    if tipo_filtro == 's':
        filtro = Saque.__name__
    elif tipo_filtro == 'd':
        filtro = Deposito.__name__

    tem_transacoes = False
    for transacao in conta.historico.gerador_relatorio(tipo_transacao=filtro):
        print(f"\n{transacao['tipo']}:\n\tValor: R$ {transacao['valor']:.2f}\n\tData: {transacao.get('data', 'N/A')}")
        tem_transacoes = True

    if not tem_transacoes:
        print("Não foram realizadas movimentações para a seleção atual.")

    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================")

@log_transacao
def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente número): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\nJá existe cliente com esse CPF!")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    clientes.append(cliente)
    print("\nCliente criado com sucesso!")

@log_transacao
def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado, fluxo de criação de conta encerrado!")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta, limite=500.0, limite_saque=3)
    contas.append(conta)
    cliente.adicionar_conta(conta)
    print("\nConta criada com sucesso!")

def listar_contas(contas):
    #utilizar ContaIterador
    for conta in ContaIterador(contas):
        print("=" * 100)
        print(f"Agência: {conta.agencia}\tC/C: {conta.numero}\tTitular: {conta.cliente.nome}\tSaldo: {conta.saldo}")

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def selecionar_conta_cliente(cliente):
    if not cliente.contas:
        print("\nCliente não possui conta!")
        return None
    
    return cliente.contas[0]

# Lógica Principal
def main():
    clientes = []
    contas = []

    while True:
        opcao = input(menu)

        if opcao == "d":
            depositar_valor(clientes)

        elif opcao == "s":
            sacar_valor(clientes)

        elif opcao == "e":
            exibir_extrato(clientes)

        elif opcao == "nu":
            criar_cliente(clientes)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

main()