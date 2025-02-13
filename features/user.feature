Feature: Visualização de feed de postagens

  # Cenário 1: Tela de Carregamento
  Scenario: Tela de Carregamento do Feed
    Given O usuário "João" está logado e acessa o Twibbles
    And O feed de "João" está vazio (sem postagens carregadas)
    When A tela de Feed é carregada
    Then Um ícone "T" cinza aparece na tela, com a mensagem "Carregando..." abaixo dele
    And O ícone "T" começa a mudar gradualmente para a cor marrom
    And A mensagem "Carregando..." alterna entre "Carregando..." e "Carregando.."
    When O Feed de notícias é completamente carregado
    Then O ícone "T" fica completamente marrom por 0.5 segundos
    And A mensagem alterna para "Carregado" durante esse tempo

  # Cenário 2: Exibição das postagens do feed
  Scenario: Exibição das postagens no feed
    Given O usuário "João" está na tela de feed e segue os usuários "Maria" e "Pedro"
    And "Maria" e "Pedro" têm postagens publicadas
    When As postagens de "Maria" e "Pedro" são carregadas
    Then O feed exibe os 20 primeiros posts de "Maria" e "Pedro", ordenados por data em ordem decrescente, dispostos em uma coluna
    And Cada postagem exibida no feed contém os seguintes elementos:
      | Elemento                           | Descrição                                                                 |
      |-------------------------------------|---------------------------------------------------------------------------|
      | Nome de usuário                     | Exibe o nome do autor da postagem, com link para o perfil do usuário.     |
      | Avatar do autor                     | Exibe o avatar do autor da postagem, localizado ao lado do nome.          |
      | Data e hora da postagem             | Exibe a data e hora da postagem (por exemplo, "Há 2 horas", "Ontem").     |
      | Conteúdo da postagem                | Exibe o texto da postagem, imagem ou vídeo, conforme o tipo de conteúdo.  |
      | Botão de Curtir                     | Exibe o botão para curtir a postagem, com o número de curtidas atual.     |
      | Botão de Comentar                   | Exibe o botão para comentar na postagem, com o número de comentários.     |


  # Cenário 3: Responsividade do Feed
  Scenario: Responsividade do Feed
    Given O usuário "João" está logado e acessa o Twibbles
    When O feed de notícias é carregado em uma tela de desktop
    Then O feed deve ocupar a largura total da tela
    And As postagens devem ser organizadas em uma única coluna, ocupando a largura disponível
    And O feed deve ser rolável verticalmente com uma barra de rolagem visível
  
    When O usuário "João" acessa o Twibbles em um dispositivo móvel
    Then O feed deve ajustar-se automaticamente para caber na tela do dispositivo móvel
    And As postagens devem ser exibidas em uma única coluna, ocupando a largura do dispositivo
    And Os botões de interação (Curtir, Comentar, Compartilhar) devem ser de fácil acesso, adaptados para o toque
    And O feed deve ser rolável verticalmente com a rolagem adaptada ao toque

  
  # Cenário 4:  Carregar mais postagens antigas com rolagem
  Scenario: Carregar mais postagens antigas com rolagem
    Given O usuário "João" está logado e visualiza os 20 primeiros posts no feed
    And O feed de "João" exibe postagens de "Maria" e "Pedro", as mais recentes
    When O usuário rola o feed até o final das postagens visíveis
    Then Um ícone "T" cinza aparece momentaneamente abaixo da última postagem carregada
    And A mensagem "Carregando..." é exibida abaixo do ícone "T"
    When O feed carrega as próximas 20 postagens antigas de "Maria" e "Pedro"
    Then As 20 novas postagens são adicionadas ao final do feed, mantendo as postagens mais recentes visíveis
    And O ícone "T" cinza desaparece assim que o carregamento é concluído
    And O feed continua rolável, permitindo que o usuário interaja com as postagens carregadas


  # Cenário 5: Carregar mais postagens novas com rolagem para cima
  Scenario: Carregar mais postagens novas com rolagem para cima
    Given O usuário "João" está logado e visualiza as postagens mais antigas no feed
    And O feed de "João" está mostrando postagens de "Maria" e "Pedro" já carregadas
    When O usuário rola o feed para cima para carregar postagens mais novas
    Then O feed exibe as postagens mais novas de "Maria" e "Pedro", sem limite de 20, carregando todas as postagens mais recentes disponíveis
    And As postagens mais novas de "Maria" e "Pedro" são inseridas automaticamente acima das postagens antigas
    And O feed continua rolável, permitindo que o usuário interaja com as postagens recém-carregadas
    And O ícone "T" cinza aparece momentaneamente acima da postagem mais recente, com a mensagem "Carregando..."
    When As postagens mais novas são completamente carregadas
    Then O ícone "T" desaparece


  # Cenário 6: Feed carregado com sucesso
  Scenario: Feed carregado com sucesso
    Given O usuário "João" está logado e segue os usuários "Maria" e "Pedro"
    And "Maria" e "Pedro" ainda não publicaram nenhuma postagem
    When Uma requisição GET é enviada para /feed
    Then Retorna status 200 com uma mensagem “Ainda não há postagens no seu feed”

  # Cenário 7: Nenhuma postagem
  Scenario: Nenhuma postagem
    Given O usuário "João" está logado e segue os usuários "Maria" e "Pedro"
    And "Maria" e "Pedro" ainda não publicaram nenhuma postagem
    When Uma requisição GET é enviada para /feed
    Then Retorna status 200 com uma mensagem “Ainda não há postagens no seu feed”

  # Cenário 8: Usuário não segue ninguém
  Scenario: Usuário não segue ninguém
     Given O usuário "João" está logado e não segue nenhum outro usuário
    When O usuário acessa a tela de feed
    Then O feed não faz nenhuma requisição para /feed
    And A tela exibe a mensagem “Você precisa seguir alguém para ver postagens no seu feed”
    And Não há conteúdo exibido no feed

  # Cenário 9: Nenhuma postagem disponível no feed
  Scenario: Nenhuma postagem disponível no feed
    Given O usuário "João" está logado e segue os usuários "Maria" e "Pedro"
    And "Maria" e "Pedro" não publicaram nenhuma postagem recentemente
    When O feed de notícias é carregado
    Then O feed exibe a mensagem "Ainda não há postagens no seu feed"
    And A mensagem deve ser centralizada na tela, visível para o usuário
    And Não há postagens visíveis no feed
    And Não é exibido o ícone "T" de carregamento, pois não há novas postagens para carregar