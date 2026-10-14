
# MESAFARTAI — Relatório da Fase 1, Etapa 2

## 1. Quantas árvores foram utilizadas no Random Forest?

Foram utilizadas 80 árvores de decisão, configuradas pelo parâmetro `n_estimators=80`.

## 2. Qual foi o threshold utilizado?

O threshold definido foi de 0.60 (60%).

Quando a confiança do modelo é inferior a 60%, ou quando a intenção identificada é `fora_de_escopo`, o sistema retorna `fallback`, solicitando que o usuário reformule sua mensagem.

## 3. Quais foram os resultados da primeira execução?

O arquivo `src/nlu.py` foi executado com sucesso utilizando Python 3.12.10.

| Entrada | Intenção retornada | Confiança |
|---|---|---|
| Tenho 30 kg de banana para doar | cadastrar_doacao | 92,5% |
| Nossa instituição precisa de mantimentos | fallback | 41% |
| Qual é a receita de bolo de cenoura? | fallback | 49% |
| coisa comida doar la | fallback | 42% |

O primeiro teste identificou corretamente a intenção de cadastrar uma doação. Nos outros três testes, a trava de segurança foi acionada.

A frase sobre a instituição precisar de mantimentos pertence ao contexto de solicitação de alimentos, mas não atingiu a confiança mínima exigida pelo modelo.

## 4. Como podemos melhorar a confiança do modelo?

Podemos aumentar e diversificar a quantidade de frases de treinamento, incluindo diferentes maneiras de solicitar alimentos, cadastrar doações e consultar o status.

Também podemos realizar novos testes, analisar os erros de classificação e ajustar os parâmetros do modelo.

## 5. Por que utilizar Random Forest?

O Random Forest combina várias árvores de decisão para realizar classificações.

Ele foi escolhido para o projeto por permitir a classificação das intenções a partir dos textos transformados em valores numéricos pelo TF-IDF.

Além disso, o modelo permite calcular probabilidades de classificação, utilizadas na aplicação do threshold de segurança.

Para confirmar se é o melhor algoritmo para o projeto, seria necessário compará-lo com outros modelos utilizando métricas de avaliação.

## Conclusão

O motor NLU do MESAFARTAI foi implementado e executado com sucesso, utilizando TF-IDF, Random Forest com 80 árvores e threshold de 60%.

Os testes demonstraram o funcionamento da classificação de intenções e do mecanismo de fallback. Como melhoria futura, será necessário ampliar a base de treinamento para reconhecer mais variações das mensagens dos usuários.
