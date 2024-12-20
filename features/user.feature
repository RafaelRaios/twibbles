Feature: Visualização de feed de postagens

  # Cenário 1: Feed carregado com sucesso
  Scenario: Feed carregado com sucesso
    Given O usuário na tela de usuário
    And O usuário segue outros usuários que possuem postagens
    When Uma requisição GET é enviada para /feed
    Then Retorna status 200 com uma lista de postagens ordenada por hora de publicação

  # Cenário 2: Nenhuma postagem
  Scenario: Nenhuma postagem
    Given O usuário na tela de usuário
    And O usuário segue outros usuários que ainda não publicaram nenhuma postagem
    When Uma requisição GET é enviada para /feed
    Then Retorna status 200 com uma mensagem “Ainda não há postagens no seu feed”
