# Análise de vendas da 7ª geração de videogames

## Objetivo
Analisar comparativamente as vendas de jogos da sétima geração de consoles (Xbox 360, PlayStation 3 e Nintendo Wii), com foco 
nos mercados norte-americano e japonês, explorando como preferências culturais e estratégias corporativas se refletem nos dados de vendas.

## Estrutura da Análise

### Parte 1 – Contexto histórico e panorama geral
- Comparação de vendas entre gerações (5ª, 6ª e 7ª)
- Introdução e tendência da 7ª geração

### Parte 2 – Análise comparativa entre mercados
- Diferenças entre as regiões da América do Norte e Japão
- Comparação de vendas entre plataformas
- Preferências por gêneros, publishers
- Impacto de exclusivos por plataforma
- Distribuição por classificação etária

## Tecnologias utilizadas
- **Linguagem:** Python 3.12  
- **Bibliotecas principais:** pandas, matplotlib, seaborn

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
│ └── videogame_sales.ipynb
└── README.md
```

## Principais Resultados

### Mercado Norte-Americano
- Predomínio de ação, esportes e shooters  
- Publishers ocidentais (EA, Activision, Ubisoft) dominam  
- Xbox 360 liderou as vendas  

### Mercado japonês
- Forte apelo de RPGs japoneses  
- Publishers japonesas (Nintendo, Square Enix, Capcom) dominaram  
- PS3 e Wii tiveram melhor desempenho  

### Performance por plataforma
- **Xbox 360:** hegemonia no NA, foco em público hardcore, quase irrelevante no JP  
- **PlayStation 3:** equilíbrio, com destaque no Japão graças aos JRPGs  
- **Nintendo Wii:** sucesso global, dominando o público casual e familiar

### Diferenças intrigênero  
- Preferências distintas de cada mercado mesmo em gêneros populares em ambas regiões.

## Lições aprendidas

- Prática extensiva das bibliotecas Pandas e Matplot
- Estruturação de análise de dados e prática de storytelling

## Como reproduzir

1. Clone o repositório:
```bash
git clone https://github.com/kzini/videogames_sales.git
cd videogames_sales
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute videogame_sales.ipynb na pasta `notebooks/` para reproduzir os experimentos.

> Desenvolvido por Bruno Casini  
> Contato: kzini1701@gmail.com
> LinkedIn:Em construção
