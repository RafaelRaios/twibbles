Feature: postagem

    # Cenário 1
    Scenario: Publicação bem sucedida
        Given O usuário "João Silva" está logado na plataforma Twibbles
        And João Silva está na tela de usuário, na aba de postagens
        And João Silva tem 150 caracteres disponíveis para escrever, e o texto "Hoje o dia está lindo!" está dentro do limite de 280 caracteres
        When João Silva escreve o texto "Hoje o dia está lindo!" e envia uma requisição POST para /postagens
        Then O sistema retorna status 201 com a mensagem “Postagem publicada com sucesso”
        And A postagem "Hoje o dia está lindo!" aparece no feed de João Silva

    # Cenário 2
    Scenario: Texto inválido
        Given O usuário "Maria Oliveira" está logado na plataforma Twibbles
        And Maria Oliveira está na tela de usuário, na aba de postagens
        And Maria Oliveira tenta publicar uma postagem com o texto " " (texto vazio)
        When Maria Oliveira tenta enviar a postagem e o sistema valida o texto
        Then O botão de enviar fica desabilitado, impedindo a publicação
        And O sistema exibe uma mensagem de erro: “O texto deve conter entre 1 e 280 caracteres”

    # Cenário 3
    Scenario: Usuário não autenticado
        Given O usuário "Carlos Souza" está na tela de usuário
        And Carlos Souza está na aba de postagens, mas não está autenticado no sistema
        And Carlos Souza tenta publicar a postagem com o texto "Olha só essa novidade!"
        When Carlos Souza envia a requisição POST para /postagens
        Then O sistema redireciona Carlos Souza para a aba de login
        And O sistema retorna status 401 com a mensagem “Você precisa estar autenticado para enviar mensagens”

    # Cenário 4
	Scenario: Postagem ultrapassa o limite de caracteres
		Given O usuário "Ana Pereira" está logado na plataforma Twibbles
		And Ana Pereira está na tela de usuário, na aba de postagens
		And Ana Pereira tenta publicar uma postagem com um texto que contém 300 caracteres
		When Ana Pereira tenta enviar a postagem e o sistema valida o texto
		Then O botão de enviar fica desabilitado, impedindo a publicação
		And O sistema exibe uma mensagem de erro: “O texto deve conter entre 1 e 280 caracteres”

	# Cenário 5
	Scenario: Edição de postagem bem-sucedida
		Given O usuário "Fernando Lima" está logado na plataforma Twibbles
		And Fernando Lima está na tela de usuário, na aba de postagens
		And Fernando Lima tem uma postagem existente com o texto "Bom dia, pessoal!"
		When Fernando Lima edita a postagem para "Bom dia, galera!" e envia a requisição PUT para /postagens/{id}
		Then O sistema retorna status 200 com a mensagem “Postagem atualizada com sucesso”
		And A postagem atualizada "Bom dia, galera!" aparece no feed de Fernando Lima

	# Cenário 6
	Scenario: Exclusão de postagem bem-sucedida
		Given O usuário "Mariana Costa" está logado na plataforma Twibbles
		And Mariana Costa está na tela de usuário, na aba de postagens
		And Mariana Costa tem uma postagem existente com o texto "Adoro café!"
		When Mariana Costa solicita a exclusão da postagem e envia a requisição DELETE para /postagens/{id}
		Then O sistema retorna status 200 com a mensagem “Postagem excluída com sucesso”
		And A postagem "Adoro café!" não aparece mais no feed de Mariana Costa

	# Cenário 7
	Scenario: Falha ao editar postagem de outro usuário
		Given O usuário "Ricardo Nunes" está logado na plataforma Twibbles
		And Ricardo Nunes está na tela de usuário, na aba de postagens
		And Ricardo Nunes tenta editar uma postagem de outro usuário
		When Ricardo Nunes envia a requisição PUT para /postagens/{id} com o novo texto "Alteração não autorizada"
		Then O sistema retorna status 403 com a mensagem “Você não tem permissão para editar esta postagem”

	# Cenário 8
	Scenario: Falha ao publicar devido a erro no servidor
		Given O usuário "Gustavo Alves" está logado na plataforma Twibbles
		And Gustavo Alves está na tela de usuário, na aba de postagens
		And Gustavo Alves tenta publicar uma postagem com o texto "Testando erro do servidor"
		When Gustavo Alves envia a requisição POST para /postagens e ocorre um erro interno no servidor
		Then O sistema retorna status 500 com a mensagem “Erro interno do servidor. Tente novamente mais tarde”

	# Cenário 9
	Scenario: Tentativa de postagem com mídia não suportada
		Given O usuário "Lucas Fernandes" está logado na plataforma Twibbles
		And Lucas Fernandes está na tela de usuário, na aba de postagens
		And Lucas Fernandes tenta publicar uma postagem anexando um arquivo de formato não suportado (ex: .exe)
		When Lucas Fernandes tenta enviar a postagem
		Then O sistema exibe uma mensagem de erro: “Formato de arquivo não suportado”
		And O botão de enviar permanece desabilitado
