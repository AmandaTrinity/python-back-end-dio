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

# Operações bancárias
def sacar(*, conta, valor_saque,limite_valor_saque, limite_numero_saques):
    """"Atualização de Estado. Key only"""
    saldo = conta['saldo']
    numero_saques = conta['numero_saques']

    excedeu_saldo = valor_saque > saldo
    excedeu_limite_valor = valor_saque > limite_valor_saque
    excedeu_numero_saques = numero_saques >= limite_numero_saques

    if excedeu_saldo:
        print('Não será possível sacar, por falta de saldo')
    elif excedeu_numero_saques:
        print('Diaramente, você só pode realizar três saques.') 
    elif excedeu_limite_valor:
        print('Você passou do seu limite máximo por saque.')
    elif valor_saque < 0:
        print('Por favor, digite um valor válido.')
    else:
        conta['saldo'] = saldo - valor_saque
        conta['numero_saques'] = numero_saques + 1
        conta['extrato'] += f'Saque: R${valor_saque:.2f}\n'
        return True
    
    return False

def depositar(conta, valor_deposito, /):
    if valor_deposito > 0:
        saldo = conta['saldo']
        conta['saldo'] = saldo + valor_deposito
        conta['extrato'] += f'Depósito: R${valor_deposito:.2f}\n'
        return True
    
    print('Por favor, digite um valor válido.')
    return False

def exibir_extrato(conta,/):
    extrato = conta['extrato']
    saldo = conta['saldo']
    print('\n=========== EXTRATO ===========')
    print('Não foi realizado nenhum depósito ou saque.\n' if not extrato else extrato)
    print(f'Saldo: R${saldo:.2f}')
    print('================================')

# Gerenciamento de Contas
def criar_conta(agencia, conta_corrente, usuario_cpf):
    '''Cria uma nova conta e a associa a um usuário existente.'''
    numero_conta = len(conta_corrente) + 1
    nova_conta = {'agencia': agencia, 'numero_conta': numero_conta, 'usuario_cpf': usuario_cpf,'saldo':0, 'extrato': "", 'numero_saques': 0}

    conta_corrente.append(nova_conta)
    print("\nConta criada com sucesso!")
    print(f"Agência: {agencia}\nC/C:     {numero_conta}")

def listar_contas(contas, usuarios_cadastrados):
    '''Lista todas as contas cadastradas.'''
    for conta in contas:
        cpf_titular = conta['usuario_cpf']
        nome_titular = usuarios_cadastrados[cpf_titular]['nome']
        linha = f"Agência: {conta['agencia']} | C/C: {conta['numero_conta']} | Titular: {nome_titular}"
        print("=" * (len(linha) + 2))
        print(f" {linha} ")
        print("=" * (len(linha) + 2))

# Gerenciamento de Usuários
def cadastro_usuario(*,cpf, nome, data_nascimento, endereco, usuarios_cadastrados):
    """ Cadastro no  banco de dados"""
    usuarios_cadastrados[cpf] = {'nome': nome, 'data_nascimento': data_nascimento, 'endereco': endereco}
    print("\nUsuário criado com sucesso!")

def filtrar_usuario(cpf, usuarios):
    """"Buscar esse cpf no banco de dados para ver se já existe"""
    return usuarios.get(cpf)

# Fluxo de Interação com o Usuário
def fluxo_criacao_usuario(usuarios_cadastrados):
    """Coordena a criação de um novo usuário."""
    cpf = input('Digite o número do seu cpf (somente números): ')
    
    if filtrar_usuario(cpf, usuarios_cadastrados):
        print('\nJá existe usuário com esse CPF!')
        return
    nome = input('Digite o seu nome: ')
    data_nascimento = input('Digite a sua data de nascimento: ')
    endereco = input('Digite o seu endereço: ')

    cadastro_usuario(cpf=cpf, nome=nome, data_nascimento=data_nascimento, endereco=endereco, usuarios_cadastrados=usuarios_cadastrados)

def fluxo_criacao_conta_corrente(agencia,contas, usuarios_cadastrados):
    '''Coordena a criação de uma nova conta corrente'''
    cpf = input('Digite o número do seu cpf (somente números): ')

    if not filtrar_usuario(cpf, usuarios_cadastrados):
        print('Usuario não encontrado, fluxo de criação de conta encerrado')
        return
    criar_conta(agencia, contas, cpf)

def selecionar_conta(usuarios_cadastrados, contas):
    """Permite ao usuário selecionar uma de suas contas."""
    cpf = input("Informe o CPF do titular da conta: ")
    usuario = filtrar_usuario(cpf, usuarios_cadastrados)

    if not usuario:
        print("\nUsuário não encontrado!")
        return None

    contas_usuario = [conta for conta in contas if conta['usuario_cpf'] == cpf]
    if not contas_usuario:
        print("\nNenhuma conta encontrada para este usuário.")
        return None

    print("\nContas encontradas:")
    for i, conta in enumerate(contas_usuario):
        print(f"[{i+1}] Agência: {conta['agencia']}, C/C: {conta['numero_conta']}")

    escolha = int(input("Selecione o número da conta: ")) - 1
    if 0 <= escolha < len(contas_usuario):
        return contas_usuario[escolha]
    
    print("\nOpção inválida.")
    return None

# Lógica Principal
def main():
    usuarios_cadastrados = {}
    contas = [] # Isso permite armazenar várias contas
    
    AGENCIA = '0001'
    LIMITE_VALOR_SAQUE = 500
    LIMITE_NÚMEROS_SAQUES = 3
    
    while True:

        opcao = input(menu)

        if opcao == "d":
            conta_selecionada = selecionar_conta(usuarios_cadastrados, contas)
            if conta_selecionada:
                valor_deposito = float(input('Digite o valor a ser depositado: '))
                resultado = depositar(conta_selecionada, valor_deposito)
                
                if resultado:
                    print('Depósito realizado com sucesso!')

        elif opcao == 'lc': 
            listar_contas(contas, usuarios_cadastrados)

        elif opcao == "s":
            conta_selecionada = selecionar_conta(usuarios_cadastrados, contas)
            if conta_selecionada:
                valor_saque = float(input('Digite o valor a ser sacado: '))
                resultado = sacar(conta=conta_selecionada,valor_saque=valor_saque,limite_valor_saque=LIMITE_VALOR_SAQUE,limite_numero_saques=LIMITE_NÚMEROS_SAQUES)
                
                if resultado:
                    print('Saque concluído com sucesso.')

        elif opcao == "e":
            conta_selecionada = selecionar_conta(usuarios_cadastrados, contas)
            if conta_selecionada:
                exibir_extrato(conta_selecionada)
        
        elif opcao == "q":
            print('\nSaindo do sistema... Obrigado por usar nosso serviço!')
            break
        elif opcao == 'nu': # Novo Usuário
            fluxo_criacao_usuario(usuarios_cadastrados)
        elif opcao == 'nc': # Nova Conta
            fluxo_criacao_conta_corrente(AGENCIA, contas, usuarios_cadastrados)
        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")
main()