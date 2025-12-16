# Análise de vendas da 7ª geração de videogames

## Objetivo
Analisar comparativamente,  as vendas de jogos da sétima geração de consoles (Xbox 360, PlayStation 3 e Nintendo Wii), com foco nos mercados norte-americano e japonês. Explorando como preferências culturais e estratégias corporativas se refletem nos dados de vendas.

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

## Principais resultados

### Domínio da Sony nas duas gerações anteriores
Por duas gerações (5ª e 6ª), a Sony dominou o mercado sem que nenhum concorrente chegasse perto.

### 7ª geração - A ascenção da Microsoft
O panorama mudou na 7ª geração. Embora a Sony tenha mantido sua hegemonia nos mercados japonês e europeu, a Microsoft com seu segundo colsole - Xbox 360 — conseguiu desbancar o domínio de vendas de títulos do Playstation no mercado norte-americano, que acabou também sendo ultrapassado pela Nintendo neste mercado e amargou a lanterna das vendas.

## Características da geração

- Exclusividade temporária de títulos do Xbox 360
- Perda de títulos multiplataformas no Wii.

## Tendências
### Jogos de ritmo
As séries Guitar Hero e Rock Band tiveram vendas impressionantes (mais de 60 milhões de cópias vendidas no mercado global), com 23 títulos lançados.

### Franquia Call of Duty
Com destaque para as séries Modern Warfare e Black Ops. No total, a franquia vendeu mais de 183,69 milhões de cópias no mercado de consoles domésticos desta geração.

### Jogos de mundo aberto
Títulos como Fallout 3 (2008), Assassin's Creed 2 (2009), Red Dead Redemption e Fallout: New Vegas em 2010, Batman: Arkham City e The Elder Scrolls V: Skyrim em 2011, e Far Cry 3 (2012) alcançaram sucesso crítico e comercial.

## Análise de Mercado da 7ª geração

### Mercado norte-americano
- Predomínio de ação, esportes e shooters  
- Publishers ocidentais dominaram  
- Xbox 360 liderou as vendas  

### Mercado japonês
- Forte apelo de RPGs japoneses  
- Publishers japonesas dominaram  
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

> Desenvolvido por Bruno Casini  
> Contato: kzini1701@gmail.com  
> LinkedIn: www.linkedin.com/in/kzini
