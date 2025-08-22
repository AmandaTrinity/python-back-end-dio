menu = """
[MENU]
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

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
    excedeu_limite_valor = valor_saque > limite_saque
    excedeu_saldo = valor_saque > saldo

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

#2. Atualização de Estado
def sacar(*, saldo, valor_saque, extrato, numero_saques):
    saldo -= valor_saque
    numero_saques += 1
    extrato += f'Valor sacado: R${valor_saque:.2f}\n'
    print('Saque concluído.')    
    return saldo, extrato, numero_saques

while True:

    opcao = input(menu)

    if opcao == "d":
        valor_deposito = float(input('Digite o valor a ser depositado: '))

        if valor_deposito > 0:
            saldo += valor_deposito
            extrato += f'Valor depositado: R${ valor_deposito:.2f}\n'
            print('Depósito realizado')
        else:
            print('Por favor, digite um valor válido.')

    elif opcao == "s":
        valor_saque = float(input('Digite o valor a ser sacado: '))

        pode_sacar = possibilidade_sacar(
            valor_saque=valor_saque, saldo=saldo, numero_saques=numero_saques, 
            limite_saque=LIMITE_VALOR_SAQUE, limite_num_saques=LIMITE_NÚMEROS_SAQUES)

        if pode_sacar:
            saldo, extrato, numero_saques = sacar(saldo=saldo, valor_saque=valor_saque, extrato=extrato, numero_saques=numero_saques)

    elif opcao == "e":
        print('\n=========== EXTRATO ===========')
        print('Não foi realizado nenhum depósito ou saque.\n' if not extrato else extrato)
        print(f'Saldo: R${saldo:.2f}')
    
    elif opcao == "q":
        print('\nSaindo do sistema... Obrigado por usar o nosso serviço!')
        print('Saindo do sistema... Obrigado por usar o nosso serviço')

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
