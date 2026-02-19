# Teste Técnico (Extração de informações em Faturas de Energia)

Para garantir o eficiente gerenciamento dos créditos de energia provenientes de usinas de energia renovável, é fundamental a extração precisa e automática de dados das notas fiscais de energia elétrica. Além disso, possuir conhecimento sobre faturas de energia elétrica é importante para o sucesso na gestão desses recursos.

Logo, é proposto dois testes como parte da avaliação dos conhecimentos técnicos e teóricos dos candidatos. Essa avaliação tem o objetivo de medir a compreensão do participante no contexto da extração de dados de notas fiscais e no entendimento básico de faturas de energia elétrica.

# Teste 1

Em busca pela eficiência na leitura de faturas, a equipe de desenvolvimento propõe a criação de uma rotina que, a partir de faturas de energia elétrica em formato de PDF, seja capaz de extrair importantes informações.

Nesta atividade, você deve editar o arquivo read.py e desenvolver uma rotina capaz de realizar a leitura da fatura fatura_cpfl.pdf em formato de PDF e retornar as seguintes informações:

- Titular da fatura (Nome e Documento)
- Endereço completo do titular da fatura
- Classificação da Instalação
- Número da instalação
- Valor a Pagar para a distribuidora
- Data de Vencimento
- Mês ao qual a fatura é referente
- Tarifa total com tributos
- Tarifa total Aneel
- Quantidade em kWh do Consumo da fatura
- Saldo em kWh acumulado na Instalação
- Somatório das quantidades das energias compensadas (injetadas)
- Somatório dos Valores Totais das Operações R$
- Contribuição de iluminação Pública
- Alíquotas do ICMS, PIS e COFINS em %
- Linha digitável para pagamento

Organize a saída e visualização das informações extraídas.

## Documentação Teste 1

## 🚀 Tecnologias Utilizadas

* **Python 3.x**: Linguagem base do projeto.
* **pdfplumber**: Biblioteca escolhida para a extração de texto em PDFs estruturados, oferecendo maior fidelidade na leitura de layouts complexos em comparação com leitores tradicionais.
* **re (Expressões Regulares)**: Motor principal de busca para localizar padrões de dados ignorando quebras de linha irregulares e "sujeiras" oriundas da extração de texto.
* **json, os, glob**: Bibliotecas nativas utilizadas para estruturação da saída e automação de processamento em lote (batch processing).

## ⚙️ Como Executar o Projeto

**1. Instale as dependências**
Instale a biblioteca necessária:
```bash
pip install pdfplumber
```

**3. Prepare os arquivos**
Coloque os arquivos PDF das faturas (ex: `fatura_cemig.pdf`, `fatura_cpfl.pdf`) no mesmo diretório do arquivo `read.py`.

**4. Execute o script**
```bash
python read.py
```
O script identificará automaticamente todos os arquivos `.pdf` no diretório e imprimirá um relatório em formato JSON formatado no terminal para cada fatura processada.

## 🧠 Arquitetura e Lógica de Extração

O grande desafio da extração de dados em faturas é a inconsistência do layout extraído (textos que visualmente estão na mesma linha no PDF frequentemente quebram em linhas diferentes no texto bruto). Para contornar isso, a solução adota as seguintes estratégias:

1. **Leitura Resiliente**: O script lê todas as páginas do PDF e concatena o texto, garantindo que nenhuma informação seja perdida caso a fatura tenha múltiplas páginas.
2. **Busca Orientada a Padrões (Regex Avançado)**: Em vez de buscar dados em posições fixas ou linhas exatas, o algoritmo procura por "Palavras-chave" e utiliza o padrão `[\s\S]{0,n}?` (busca não-gulosa). Isso permite que o código pule quebras de linha (`\n`), espaços e caracteres inesperados até encontrar o formato do dado desejado (como uma máscara de moeda ou uma data).
3. **Tratamento Específico por Concessionária**: O código prevê variações de nomenclatura entre distribuidoras (ex: "SALDO ATUAL DE GERAÇÃO" na CEMIG vs. "Saldo em Energia" na CPFL) e unifica a saída.
4. **Limpeza de Dados**: Implementação de tratamentos pós-captura, como a limitação de casas decimais em saldos de geração que vêm superdimensionados do PDF (ex: de `3.606,9002236746` para `3.606,90`).

## 📋 Informações Extraídas (Status)

* [x] Titular da fatura (Nome)
* [x] Documento (CPF/CNPJ)
* [x] Número da instalação
* [x] Valor a Pagar
* [x] Data de Vencimento
* [x] Mês de Referência
* [x] Saldo em kWh acumulado na Instalação
* [x] Contribuição de iluminação Pública
* [x] Consumo em kWh
Escreva aqui a documentação do desenvolvimento do teste 1.

# Teste 2

Contexto: Você recebeu a fatura "fatura_cemig.pdf" e deve desenvolver um script para extrair seus dados. Antes de iniciar a programação, é essencial compreender e interpretar as informações presentes nesta fatura.

Atividade: Analise a fatura e redija um documento respondendo os pontos abaixo. As respostas podem ser inseridas neste 'README'.

 - Identifique as principais diferenças entre a fatura "fatura_cemig.pdf" e uma fatura convencional de energia elétrica "fatura_cemig_convencional.pdf".
 - Descreva e explique os termos e valores apresentados na seção "Valores Faturados" da fatura "fatura_cemig.pdf".
 - Considerando que a instalação da "fatura_cemig.pdf" participa do Sistema de Compensação de Energia Elétrica, identifique e explique qual informação na seção "Informações Gerais" da fatura é considerada a mais importante.
 - Identifique o consumo da instalação referente ao mês de julho de 2023.

# Resposta para o Teste 2

**1. Identifique as principais diferenças entre a fatura "fatura_cemig.pdf" e uma fatura convencional de energia elétrica "fatura_cemig_convencional.pdf".**

A diferença fundamental entre as duas faturas é que a instalação da `fatura_cemig.pdf` possui um sistema de geração distribuída e participa do Sistema de Compensação de Energia Elétrica (SCEE). Isso fica evidente pelos seguintes pontos:
* [cite_start]**Composição de Tarifas:** A fatura convencional cobra o consumo total sob a rubrica "Energia Elétrica"[cite: 107]. [cite_start]Já a fatura com geração distribuída discrimina o que foi consumido da rede, o que foi injetado, possuindo itens como "Energia compensada GD II" [cite: 39] [cite_start]e "Energia comp. adicional"[cite: 45].
* [cite_start]**Saldo de Geração:** A fatura com geração apresenta no campo de Informações Gerais o "SALDO ATUAL DE GERAÇÃO" [cite: 66][cite_start], indicando créditos de energia para meses futuros, informação inexistente na fatura convencional[cite: 113, 114, 115, 116, 117].
* [cite_start]**Custo de Disponibilidade:** Na `fatura_cemig.pdf`, o cliente é cobrado por 50 kWh na rubrica "Energia Elétrica"[cite: 27, 29], que representa o custo de disponibilidade (taxa mínima) da rede.

**2. Descreva e explique os termos e valores apresentados na seção "Valores Faturados" da fatura "fatura_cemig.pdf".**

[cite_start]Na fatura com geração distribuída[cite: 19], o faturamento ocorre de forma detalhada:
* [cite_start]**Energia Elétrica (50 kWh / R$ 47,96):** Refere-se ao custo de disponibilidade para o uso da rede[cite: 27, 29, 31]. 
* [cite_start]**Energia SCEE s/ ICMS (149 kWh / R$ 76,26):** É a energia que o cliente consumiu da rede da concessionária e que será abatida pelos créditos de energia[cite: 33, 35, 37]. 
* [cite_start]**Energia compensada GD II (149 kWh / -R$ 67,24) e Energia comp. adicional (7 kWh / -R$ 5,24):** Representam os créditos de energia da Geração Distribuída sendo aplicados para abater o valor do consumo, por isso os valores são negativos[cite: 39, 41, 43, 45, 47, 49].
* [cite_start]**Bônus Itaipu art 21 Lei 10438 (-R$ 9,79):** Crédito tarifário repassado aos consumidores[cite: 51, 52].
* [cite_start]**Ass Combt Câncer (R$ 10,00):** Doação voluntária ou serviço de terceiros autorizado pelo titular[cite: 53, 54].
* [cite_start]**Contrib Ilum Publica Municipal (R$ 24,71):** A CIP/COSIP é a taxa para custeio da iluminação pública, cobrada de todos os consumidores[cite: 55, 56].

**3. Considerando que a instalação da "fatura_cemig.pdf" participa do Sistema de Compensação de Energia Elétrica, identifique e explique qual informação na seção "Informações Gerais" da fatura é considerada a mais importante.**

[cite_start]A informação mais importante na seção de Informações Gerais [cite: 65] [cite_start]é: **"SALDO ATUAL DE GERAÇÃO: 234,63 kWh"**[cite: 66]. 
* [cite_start]**Explicação:** Esta linha informa o banco de créditos do consumidor[cite: 66]. [cite_start]Significa que o sistema produziu um excedente de 234,63 kWh que fica armazenado na concessionária e será utilizado automaticamente para abater a conta em meses futuros[cite: 66, 68].

**4. Identifique o consumo da instalação referente ao mês de julho de 2023.**

[cite_start]O consumo da instalação no mês de JUL/23 foi de **199 kWh**[cite: 60]. 
* [cite_start]**Explicação:** Esse valor é a diferença entre a leitura atual do medidor (421) e a leitura anterior (222)[cite: 63], representando a energia total consumida no período.

# Requisitos dos Desafios:

1. Utilize a linguagem Python para desenvolver a solução.
2. No mesmo README, inclua uma seção detalhada que explique claramente os passos necessários para executar o código. Certifique-se de que as instruções sejam precisas, organizadas e fáceis de entender, pois os avaliadores seguirão essa documentação.
3. Faça um fork do repositório, para iniciar o desenvolvimento.
4. A entrega deve ser realizada por meio de um pull request para o repositório original. Caso não consiga, os arquivos podem ser enviados para o email falecom@dg.energy, porém com penalidade de pontos.
5. Abra o pull request também faltando 5 minutos para o prazo final da entrega do teste. Se o pull request for realizado antes dos 5 minutos restantes haverá eliminação do candidato.
6. A entrega deve ser realizada até às 12:30h.
