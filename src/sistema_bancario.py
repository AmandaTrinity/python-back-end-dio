menu = """

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
        valor_saque = int(input('Digite o valor a ser sacado: '))

        excedeu_numero_saques = numero_saques >= LIMITE_NÚMEROS_SAQUES
        excedeu_limite_valor = valor_saque > LIMITE_VALOR_SAQUE
        excedeu_saldo = valor_saque > saldo

        if excedeu_saldo:
            print('Não será possível sacar, por falta de saldo')

        elif excedeu_numero_saques:
            print('Diaramente, você só pode realizar três saques.') 

        elif excedeu_limite_valor:
            print('Você passou do seu limite máximo por saque.')
        
        elif valor_saque > 0:
                saldo -= valor_saque
                numero_saques += 1
                extrato += f'Valor sacado: R${valor_saque:.2f}\n'
                print('Saque concluído.')

        else:
            print('Por favor, digite um valor válido.')

    elif opcao == "e":
        print('\n=========== EXTRATO ===========')
        print('Não foi realizado nenhum depósito ou saque.\n' if not extrato else extrato)
        print(f'Saldo: R${saldo:.2f}')
    
    elif opcao == "q":
        print('Saindo do sistema... Obrigado por usar o nosso serviço')
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
