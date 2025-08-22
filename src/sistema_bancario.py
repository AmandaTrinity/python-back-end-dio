menu = """
[MENU]
[a] Nova Conta
[c] Novo Usuário
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """


usuarios_cadastrados = {}
conta_corrente = {}

saldo = 0
LIMITE_VALOR_SAQUE = 500
extrato = ""
numero_saques = 0
LIMITE_NÚMEROS_SAQUES = 3

# Objetivo geral: Separar funções existentes de saque,deposito e extrato em funções. Criar duas novas funções: cadastrar usuário e conta corrente

#1. Validação de regras de negócio
def possibilidade_sacar(*, valor_saque, saldo, numero_saques, limite_saque, limite_num_saques):
    excedeu_saldo = valor_saque > saldo
    excedeu_limite_valor = valor_saque > limite_saque
    excedeu_numero_saques = numero_saques >= limite_num_saques

    if excedeu_saldo:
        print('Não será possível sacar, por falta de saldo')

    elif excedeu_numero_saques:
        print('Diaramente, você só pode realizar três saques.') 

    elif excedeu_limite_valor:
        print('Você passou do seu limite máximo por saque.')
    elif valor_saque < 0:
        print('Por favor, digite um valor válido.')
    else:
        return True
    
    return False

#2. Atualização de Estado. Key only
def sacar(*, saldo, valor_saque, extrato, numero_saques):
    saldo -= valor_saque
    numero_saques += 1
    extrato += f'Valor sacado: R${valor_saque:.2f}\n'
    print('Saque concluído.')    
    return saldo, extrato, numero_saques

#positional only
def depositar(saldo, valor_deposito, extrato, /):
    if valor_deposito > 0:
        saldo += valor_deposito
        extrato += f'Valor depositado: R${valor_deposito:.2f}\n'
        print('Depósito realizado')
    else:
        print('Por favor, digite um valor válido.')
    return saldo, extrato

#positional and keyword
def exibir_extrato(saldo, /, *, extrato):
    print('\n=========== EXTRATO ===========')
    print('Não foi realizado nenhum depósito ou saque.\n' if not extrato else extrato)
    print(f'Saldo: R${saldo:.2f}')
    print('================================')

# Cadastro no  banco de dados
def cadastro_usuario(*,cpf, nome, data_nascimento, endereco, usuarios_cadastrados):
    usuarios_cadastrados[cpf] = {'nome': nome, 'data_nascimento': data_nascimento, 'endereco': endereco}
    print("\nUsuário criado com sucesso!")

#Buscar esse cpf no banco de dados para ver se já existe
def filtrar_usuario(cpf, usuarios):
    return usuarios.get(cpf)

# Lógica de negócio criação de usuário
def fluxo_criacao_usuario(usuarios_cadastrados):
    cpf = input('Digite o número do seu cpf (somente números): ')
    
    if filtrar_usuario(cpf, usuarios_cadastrados):
        print('\nJá existe usuário com esse CPF!')
        return
    nome = input('Digite o seu nome: ')
    data_nascimento = input('Digite a sua data de nascimento: ')
    endereco = input('Digite o seu endereço: ')

    cadastro_usuario(cpf=cpf, nome=nome, data_nascimento=data_nascimento, endereco=endereco, usuarios_cadastrados=usuarios_cadastrados)

def criar_conta_corrente(agencia, numero_conta, conta_corrente, usuario, cpf):
    conta_corrente[cpf] = {'agencia': agencia, 'numero_conta': numero_conta, 'usuario': usuario }
    print("\nConta criada com sucesso!")
    print(f"Agência: {agencia}\nC/C:     {numero_conta}")

def fluxo_criacao_conta_corrente(conta_corrente, usuarios_cadastrados):
    cpf = input('Digite o número do seu cpf (somente números): ')
    usuario = filtrar_usuario(cpf, usuarios_cadastrados)
    if not usuario:
        print('Usuario não encontrado, fluxo de criação de conta encerrado')
        return
    numero_conta = len(conta_corrente) + 1
    agencia = '0001'

    criar_conta_corrente(agencia, numero_conta, conta_corrente, usuario, cpf)

while True:

    opcao = input(menu)

    if opcao == "d":
        valor_deposito = float(input('Digite o valor a ser depositado: '))
        saldo, extrato = depositar(saldo, valor_deposito, extrato)
        
    elif opcao == "s":
        valor_saque = float(input('Digite o valor a ser sacado: '))

        pode_sacar = possibilidade_sacar(
            valor_saque=valor_saque, saldo=saldo, numero_saques=numero_saques, 
            limite_saque=LIMITE_VALOR_SAQUE, limite_num_saques=LIMITE_NÚMEROS_SAQUES)

        if pode_sacar:
            saldo, extrato, numero_saques = sacar(saldo=saldo, valor_saque=valor_saque, extrato=extrato, numero_saques=numero_saques)

    elif opcao == "e":
        exibir_extrato(saldo, extrato=extrato)
    
    elif opcao == "q":
        print('\nSaindo do sistema... Obrigado por usar o nosso serviço!')
        break
    elif opcao == 'c':
        fluxo_criacao_usuario(usuarios_cadastrados)
    elif opcao == 'a':
        fluxo_criacao_conta_corrente(conta_corrente, usuarios_cadastrados)
    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
