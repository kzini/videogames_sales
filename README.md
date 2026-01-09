# Análise de vendas da 7ª geração de videogames

## Objetivo

Este projeto analisa comparativamente as vendas de jogos da sétima geração de consoles (Xbox 360, PlayStation 3 e Nintendo Wii), com foco nos mercados norte-americano e japonês.

A análise investiga como diferenças culturais regionais e estratégias corporativas influenciaram o desempenho comercial das plataformas ao longo da geração.

---

## Preparação e tratamento dos dados

### Títulos duplicados e registros redundantes

O dataset original continha tanto duplicatas completas quanto entradas redundantes resultantes da fragmentação de vendas regionais.

Esses casos foram tratados por meio da padronização dos títulos e posterior agregação por `title` e `platform`, somando as vendas regionais e consolidando os metadados associados. O processo completo de identificação e consolidação está documentado no notebook.

### Valores nulos e classificação etária
A API da IGDB (Internet Game Database) foi utilizada para auxiliar na obtenção e validação de informações ausentes nas colunas `year_of_release` e `rating`.

Boa parte das ausências restantes na coluna `rating` refletem diferenças entre os sistemas de classificação etária ocidentais (ESRB) e japoneses (CERO), comuns em títulos voltados prioritariamente ao mercado japonês. Esses registros foram mantidos na análise e tratados como uma categoria própria.

---

## Estrutura da análise

A análise foi organizada em dois eixos principais:

### 1. Estrutura competitiva da 7ª geração
- Evolução do mercado ao longo das gerações (5ª, 6ª e 7ª)
- Estratégias de lançamento inicial por plataforma
- Exclusividade temporária e dinâmica dos títulos multiplataforma

### 2. Diferenças regionais de consumo
- Contraste entre os mercados norte-americano e japonês
- Comparação de desempenho entre plataformas
- Preferências por gêneros e publishers
- Impacto dos exclusivos no desempenho regional
- Distribuição por classificação etária

---

## Breve contexto histórico

A 7ª geração representou uma ruptura no domínio histórico da Sony observado nas duas gerações anteriores.  

Enquanto o PlayStation manteve forte presença no Japão, o Xbox 360 conquistou o mercado norte-americano.  

A Nintendo, por sua vez, redefiniu o mercado ao priorizar acessibilidade e experiências first-party, e manteve forte presença em ambos os mercados.

---

## Destaque analítico: exclusividade temporária no Xbox 360

O Xbox 360 obteve de forma sistemática a **exclusividade temporária**, sendo muitas vezes a primeira plataforma a receber títulos multiplataforma relevantes.

A análise dos dados mostra que jogos lançados inicialmente no Xbox 360 — e apenas posteriormente no PS3 — tendem a apresentar **vendas globais superiores na plataforma da Microsoft**, mesmo após a chegada das versões concorrentes.

Casos emblemáticos incluem:
- *The Elder Scrolls IV: Oblivion*
- *BioShock*
- *Mass Effect 2*
- *Minecraft*

---

## Principais resultados da análise de mercado  
*Com ênfase nos mercados norte-americano e japonês*

### Mercado norte-americano
- Predomínio de gêneros como shooters, esportes e ação
- Forte presença de publishers ocidentais
- Liderança consistente do Xbox 360

### Mercado japonês
- Alta concentração de JRPGs e títulos de publishers japonesas
- Melhor desempenho relativo do PlayStation 3 e do Wii
- Baixa penetração do Xbox 360, mesmo em títulos multiplataforma

### Performance por plataforma
- **Xbox 360:** hegemonia no mercado norte-americano, foco em público hardcore, relevância marginal no Japão  
- **PlayStation 3:** desempenho mais equilibrado, com vantagem no Japão sustentada por títulos first-party e JRPGs  
- **Nintendo Wii:** sucesso global impulsionado por exclusivos first-party e apelo casual/familiar

### Diferenças intragênero
Mesmo em gêneros populares em ambas as regiões, observam-se diferenças significativas de desempenho, indicando que preferências culturais influenciam não apenas o gênero consumido, mas também o tipo de experiência valorizada.

## Estrutura do projeto

```
videogames_sales/
├── data/
│ └── Video_Games.csv
├── src/
│ ├── utils.py
│ ├── visualization.py
│ └── constants.py
├── notebooks/
│ └── videogames_sales.ipynb
└── README.md
```

---

## Lições aprendidas

- A importância de tratar ausência de dados como informação contextual, e não necessariamente como erro
  (ex.: distinção entre sistemas ESRB e CERO em mercados distintos).

- Definição operacional de “exclusividade temporária” a partir de dados de lançamento, em vez de rótulos de marketing.

- Construção de comparações regionais evitando agregações globais que mascaram diferenças culturais relevantes.

---

## Como reproduzir

### 1. Clone o repositório:
```bash
git clone https://github.com/kzini/videogames_sales.git
cd videogames_sales
```

### 2. Instale as dependências:
```bash
pip install -r requirements.txt
```

### 3. Execute videogames_sales.ipynb na pasta `notebook/` para reproduzir os experimentos.


## Contato
> Desenvolvido por Bruno Casini  
> LinkedIn: https://www.linkedin.com/in/kzini
