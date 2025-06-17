# Um sistema bancario que permite criar conta e usuário
# Fazer deposito, realizar saques e visualizar extrato
# Desafio DIO - Back-end Python Santander 2025
# autor: Fábio Gonçalves
# Data 17-06-2025 versão: 2.0

# Biblioteca de texto para indentacao
import textwrap
# Biblioteca time para usar metodo sleep
from time import sleep

def exibir_menu():
    opcoes_menu = '''\n
    ================ MENU ================
    [1]\tDepositar
    [2]\tSacar
    [3]\tExtrato
    [4]\tNova conta
    [5]\tListar contas
    [6]\tNovo usuário
    [0]\tSair
    Selecione umas da opções acima:
    '''
    return int(input(textwrap.dedent(opcoes_menu)))

def depositar(saldo_conta, valor_deposito, extrato, /):
    if (valor_deposito > 0):
        saldo_conta += valor_deposito
        extrato += f"\nDeposito: R${saldo_conta:.2f}"
        print(f"Deposito realizado com sucesso!")
    else:
        print("O valor informado é inválido!")
    
    return saldo_conta, extrato

def sacar(*, saldo_conta, valor_saque, extrato, limite_saque, limite_valor, numero_saques):
    excedeu_saldo = valor_saque > saldo_conta
    excedeu_limite = valor_saque > limite_valor
    excedeu_saques = numero_saques >= limite_saque

    if excedeu_saldo:
        print("Saldo insuficiente!")
    elif excedeu_limite:
        print("O valor do saque é maior que seu limite disponivel!")
    elif excedeu_saques:
        print("Limite de saques excedido!")
    else:
        numero_saques += 1
        saldo_conta -= valor_saque
        extrato += f"\nSaque: R${saldo_conta:.2f}"
        print("Saque realizado com sucesso!")
    
    print(f"Voce tem {(3-numero_saques)} tentativas restantes!")
    return saldo_conta, extrato

def extrato_conta(saldo_conta, extrato):
    print("-"*10, "EXTRATO", "-"*10)
    print("Não foram realizadas movimentações!" if not extrato else extrato)
    print(f"{extrato}\nSaldo atual: R${saldo_conta:.2f}")

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Digite seu cpf")
    usuario = filtrar_usuario(cpf, usuarios)

    if (usuario):
        print("Conta criada com sucesso!")
        return {"agencia": agencia, "numero conta": numero_conta, "usuario": usuarios}

    return print("Cpf não encontrado!")

def listar_contas(contas):
    if (not contas):
        return "Não foram encontrados dados na conta!"

    for conta in contas():
        exibir_contas = f'''\n
        Agencia: {conta['agencia']}
        Conta: {conta['numero conta']}
        Usuario: {conta['usuario']}
        '''
    
    return exibir_contas


def criar_usuario(usuarios):
    cpf = input("Digite seu cpf: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if (usuario):
        return print("Já existe um usuario com o cpf informado!")

    nome = input("Digite seu nome completo")
    data_nascimento = input("Digite sua data de nascimento: (dd-mm-aa)")
    endereco = input("Digite seu endereco: (Rua, Bairro, Cidade)")

    usuarios.append({"cpf": cpf, "nome": nome, "data nascimento": data_nascimento, "endereco": endereco})
    # Quebrar a string para exibir apenas o primeiro nome
    primeiro_nome = nome.split(" ")
    print(f"Bem-vindo, {primeiro_nome[0]}. Seu usuario foi criado com sucesso!")

# Validar se o cpf do usuario está no dicionario usuario
def filtrar_usuario(cpf, usuarios):
    usuario_filtrado = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuario_filtrado[0] if usuario_filtrado else None

# Função principal que chama outras funcoes
def main():
    LIMITE_SAQUES = 3
    LIMITE_VALOR_SAQUES = 500
    AGENCIA = "0001"

    saldo_conta = float(0)
    extrato = ""
    exibir_contas = ""
    numero_saques = 0
    usuarios = []
    contas = []

    # Loop principal para manter o sistema em execução
    while True:
        try:
            opcao = exibir_menu()
        except ValueError:
            print("Opção inválida. Tente novamente!")
            sleep(1)
            continue
        
        if opcao == 1:
            valor_deposito = float(input("Digite o valor do deposito"))

            saldo_conta, extrato = depositar(saldo_conta, valor_deposito, extrato)
            sleep(1)
        elif opcao == 2:
            valor_saque = float(input("Digite o valor do saque: "))

            saldo_conta, extrato = sacar(saldo_conta=saldo_conta,
                                         valor_saque=valor_saque,
                                         extrato=extrato,
                                         limite_saque=LIMITE_SAQUES,
                                         limite_valor=LIMITE_VALOR_SAQUES,
                                         numero_saques=numero_saques
                                         )
            sleep(1)
        elif opcao == 3:
            extrato_conta(saldo_conta, extrato=extrato)
            sleep(3)
        elif opcao == 4:
            numero_conta = len(contas) + 1
            conta_usuario = criar_conta(AGENCIA, numero_conta, usuarios)
            
            if (conta_usuario):
                contas.append(conta_usuario)
            
            sleep(1)
        elif opcao == 5:
            print(listar_contas(contas))
            sleep(1)
        elif opcao == 6:
            criar_usuario(usuarios)
            sleep(1)
        elif opcao == 0:
            print("Encerrando...")
            sleep(2)
            break
        else:
            print("Algo deu errado!")

# Iniciar função principal
if __name__ == "__main__":
    main()