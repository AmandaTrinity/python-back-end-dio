# 🐍 Sistema Bancário com Python — Santander Open Academy

Este repositório contém a evolução de um sistema bancário desenvolvido durante o curso **Back-End com Python**, promovido pelo **Santander** em parceria com a **DIO**. O projeto partiu de uma estrutura funcional simples até uma arquitetura robusta baseada em Programação Orientada a Objetos (POO).

## 🎯 Objetivo

Praticar e consolidar fundamentos avançados de Python, aplicando conceitos que tornam o código mais escalável, organizado e profissional.

## 🛠️ Tecnologias e Conceitos Aplicados

- **Python**: Linguagem principal.
- **Programação Orientada a Objetos (POO)**: Implementação de classes, herança, polimorfismo e interfaces (classes abstratas).
- **Arquitetura e Design Patterns**:
  - **Decoradores**: Utilizados para criar logs automáticos de transações.
  - **Iteradores**: Implementação de um iterador customizado para listar contas.
  - **Geradores**: Uso de `yield` para otimizar o relatório de extrato.
- **Manipulação de Ficheiros**: Sistema de logging persistente em ficheiro `.txt`.

## 🏗️ Estrutura do Projeto

O projeto está dividido em duas etapas principais:

1. **Versão Funcional (`sistema_bancario.py`)**: Focada em funções, dicionários e listas para gerir utilizadores e contas.
2. **Versão POO (`sistema_bancario_poo.py`)**: Refatoração completa utilizando classes como `PessoaFisica`, `ContaCorrente`, `Historico` e `Transacao`.

## 🚀 Funcionalidades Finalizadas

- [x] **Gestão de Utilizadores**: Cadastro de clientes (Pessoa Física) com validação de CPF.
- [x] **Gestão de Contas**: Criação de múltiplas contas correntes vinculadas a um cliente.
- [x] **Operações Bancárias**:
  - **Depósito e Saque**: Com validações de saldo, limite de valor e limite de transações diárias.
  - **Extrato Detalhado**: Histórico de transações com data e hora, incluindo filtros por tipo de operação.
- [x] **Sistema de Logs**: Registo automático de cada função executada num ficheiro externo para auditoria.

## 🔧 Como Executar

1. **Clona o repositório**:
```bash
git clone https://github.com/teu-utilizador/python-back-end-dio.git
```
2. **Navega até a pasta do código**:
```bash
cd src
```
3. **Executa a versão mais recente (POO)**:
```bash
python sistema_bancario_poo.py
```
