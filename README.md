# Loans For Good

Aplicação para criação e manutenção de propostas de empréstimos

## Sumário

- [Visão Geral](#visão-geral)
- [Requisitos](#requisitos)
- [Configuração](#configuração)
- [Uso](#uso)
- [Contribuição](#contribuição)
- [Licença](#licença)

## Visão Geral

Aplicação para criação e manutenção de propostas de empréstimos, permite a criação de propostas via pagina web e atualização e visualização das mesmas via django admin.

## Requisitos

* [docker](https://docs.docker.com/engine/install/)
* [docker-compose](https://docs.docker.com/compose/install/)

## Configuração

1. Clone o repositório: `git clone https://github.com/seu-usuario/loansforgood.git`
2. Acesse o diretório do projeto: `cd loansforgood`

## Uso

1. Para subir o projeto localmente utilize `make dc-project-up` e aguarde até que todas as configurações sejam realizadas.
2. Acesse [este link](http://localhost:3000/) para acessar a pagina de criação de propostas.
3. Acesse [este link](http://localhost:8000/admin) para acessar as paginas de backoffice, nela clique logue com o usuário já criado com as seguintes informações: Username: `myuser`, Password: `mypassword`.
4. Para criar novos campos para as propostas clique no botao `+ Add` ao lado de `Proposal fields` ou acesse `Proposal fields` e clique em `ADD PROPOSAL FIELD` ou  `+ Add`, adicione o nome do campo, o tipo e se é obrigatório e por fim clique em `SAVE`.
4. Para atualizar as propostas acesse `Proposals`, escolha a proposal a atualizar e clique no seu identificador, você será redirecionado a pagina da proposal, e caso esteja com status de `PENDING_HUMAN_APPROVAL` será permitido alterar seu status, por fim clique em `SAVE`.

## Tests

Caso queira ter acesso ao resultado dos testes utilize `make dc-project-test`
