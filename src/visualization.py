import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.ticker as mticker

from src.constants import (
    font, region_info, gen7, gen6, gen5, region_prepositions, score_labes,
    region_info
    )

from src.utils import (
    get_sales_by_platform_region, calculate_percentage_sales, 
    calculate_percentage_sales, count_titles_by_platform,
    get_top_games_by_region, get_top_games_by_platform,
    shorten_title, get_top_rated_score,
    get_genres_count_by_publishers, get_top_publishers_by_region,
    get_sales_and_exclusives, get_region_only_sales,
    group_and_sum_sales_by_rating

    )

def plot_global_market_share_pie_chart(df):
    regions = [region for region in region_info.keys() if region != 'global_sales']
    total_sales = sum(df[region].sum() for region in regions)
    
    labels = [region_info[region]['region_name'] for region in regions]
    colors = [region_info[region]['color'] for region in regions]
    pct_sizes = [
        calculate_percentage_sales(df[region].sum(), total_sales)
        for region in regions
    ]

    fig, ax = plt.subplots(figsize=(6, 6))
    wedges, texts, autotexts = ax.pie(
        pct_sizes,
        labels=labels,
        colors=colors,
        autopct='%1.2f%%',
        startangle=140,
        wedgeprops={'edgecolor': 'black', 'linewidth': 1}
    )
    for text in texts:
        text.set_fontsize(13)
        text.set_fontweight('normal')
    
    for autotext in autotexts:
        autotext.set_fontsize(13)
        autotext.set_fontweight('bold')

    ax.set_title('Participação de mercado por região', fontdict=font, fontsize=16)
    ax.axis('equal')
    plt.tight_layout()
    plt.show()

def plot_sales_by_platform_region(df, region_info, gen_dict):
    sales_data = {
        region: [get_sales_by_platform_region(df, platform, region) 
                 for platform in gen_dict.keys()]
        for region in region_info.keys()
    }

    platform_keys = list(gen_dict.keys())
    console_names = [gen_dict[key]['console_name'] for key in platform_keys]

    width = 0.2 
    group_gap = 0.3
    x = np.arange(len(gen_dict)) * (1 + group_gap)

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = []

    for i, (region, data) in enumerate(region_info.items()):
        color = data['color']
        bar = ax.bar(
            [pos + width * i for pos in x],
            sales_data[region],
            width,
            label=data['region_name'],
            color=color
        )
        bars.append(bar)

    for bar_group in bars:
        for bar in bar_group:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                height,
                f'{height:.2f}',
                ha='center',
                va='bottom'
            )

    ax.set_ylabel('Vendas Totais', fontsize=12)
    ax.set_title(
        "Vendas de jogos por plataforma e região",
        fontdict=font,
        fontsize=16
    )
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    ax.legend(title='Regiões')

    ax.set_xticks([pos + width * (len(region_info) - 1) / 2 for pos in x])
    ax.set_xticklabels(console_names, rotation=0, ha='center')

    plt.tight_layout()
    plt.show()

def plot_region_market_share_pie_charts(df, gen, regions):
    fig = plt.figure(figsize=(14, 10))
    gs = gridspec.GridSpec(2, 2, height_ratios=[1, 1])
    
    axs = [fig.add_subplot(gs[0, 0]), fig.add_subplot(gs[0, 1])]

    fig.suptitle(
        "Participação de mercado em vendas de jogos por plataforma e região",
        fontdict=font,
        fontsize=16,
        y=1.00
    )

    for idx, region in enumerate(regions):
        total_region_sales = df[region].sum()
        total_sales_dict = {}
        percentage_sales_dict = {}

        for platform in gen.keys():
            total_sales = get_sales_by_platform_region(df, platform, region)
            total_sales_dict[platform] = total_sales
            percentage_sales = calculate_percentage_sales(total_sales, total_region_sales)
            percentage_sales_dict[platform] = percentage_sales

        labels = [gen[platform]['console_name'] for platform in total_sales_dict.keys()]
        pct_sizes = list(percentage_sales_dict.values())
        colors = [gen[platform]['color'] for platform in total_sales_dict.keys()]

        wedges, texts, autotexts = axs[idx].pie(
            pct_sizes,
            labels=labels,
            colors=colors,
            autopct='%1.2f%%',
            startangle=140,
            wedgeprops={'edgecolor': 'black', 'linewidth': 1}
        )

        axs[idx].set_title(
            region_info[region]["region_name"],
            fontsize=15, fontweight='bold', pad=20
        )
        axs[idx].axis('equal')
        plt.setp(texts, size=13)
        plt.setp(autotexts, size=13, weight="bold")

    plt.tight_layout()
    plt.show()

def plot_total_titles_by_platform(df, gen):
    titles_count = df['platform'].value_counts()
    console_name = [gen[platform]['console_name'] for platform in titles_count.keys()]
    colors = [gen[platform]['color'] for platform in titles_count.keys()]
    
    plt.figure(figsize=(8,6))
    bars = plt.bar(console_name, titles_count.values, color = colors, edgecolor = 'black')
    
    for bar, count in zip(bars, titles_count.values):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), str(count),
                 va='bottom', ha='center', fontsize=12)
        
    plt.title(f"Total de títulos lançados por plataforma", fontdict=font, fontsize=16)
    plt.ylabel('Número de Títulos', fontsize=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.tight_layout()
    plt.show()

def plot_games_per_platform_year(df, gen):
    games_per_platform_year = df.groupby(['year_of_release', 'platform']).size().unstack()

    plt.figure(figsize=(10, 6))

    for platform in games_per_platform_year.columns:
        console_name = gen[platform]['console_name']
        color = gen[platform]['color']
        plt.plot(games_per_platform_year.index, games_per_platform_year[platform], 
                 label=console_name, color=color)

    plt.title('Número de Jogos Lançados por Ano e Plataforma', 
              fontdict=font, fontsize=16)
    plt.ylabel('Número de Jogos', fontsize=14)
    plt.legend(title='Plataforma')
    plt.xticks(games_per_platform_year.index, fontsize=12)
    plt.yticks(fontsize=12)
    plt.tight_layout()
    plt.show()

def plot_regional_games(df, gen, platforms_years):
    regions = ['all', 'na_sales', 'jp_sales']
    data = {}

    for platform, year in platforms_years.items():
        all_count = len(df[(df['platform'] == platform) & (df['year_of_release'] == year)])
        na_count = len(df[(df['platform'] == platform) & (df['year_of_release'] == year) & (df['na_sales'] > 0)])
        jp_count = len(df[(df['platform'] == platform) & (df['year_of_release'] == year) & (df['jp_sales'] > 0)])
        data[platform] = {'all': all_count, 'na_sales': na_count, 'jp_sales': jp_count}

    fig, ax = plt.subplots(figsize=(12, 6))
    bar_width = 0.25
    positions = range(len(data))

    for i, region in enumerate(regions):
        counts = [data[platform][region] for platform in platforms_years.keys()]
        if region == 'all':
            label = 'Total'
            color = '#bc987e'
        else:
            label = region_info[region]['region_name']
            color = region_info[region]['color']

        ax.bar(
            [p + i * bar_width for p in positions],
            counts,
            width=bar_width,
            label=label,
            color=color
        )
        for j, count in enumerate(counts):
            ax.text(j + i * bar_width, count + 0.2, str(count), ha='center', va='bottom', fontsize=12)

    ax.set_title('Total de jogos lançados por região no primeiro ano de cada plataforma', fontdict=font, fontsize=16)
    ax.set_xticks([p + bar_width for p in positions])
    ax.set_xticklabels(
    [f"{gen[platform]['console_name']} ({year})" for platform, year in platforms_years.items()],
    fontsize=12
    )
    ax.set_ylabel('Quantidade de Jogos', fontsize=13)
    ax.tick_params(labelsize=14)
    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()

def plot_total_sales_by_platform(df, gen, region_sales, games_type):
    sales = df.groupby('platform')[region_sales].sum().sort_values(ascending=False)
    console_name = [gen[platform]['console_name'] for platform in sales.index]
    colors = [gen[platform]['color'] for platform in sales.index]
    
    plt.figure(figsize=(8,6))
    bars = plt.bar(console_name, sales.values, color = colors, edgecolor = 'black')
    
    for bar, count in zip(bars, sales.values):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), str(count),
                 va='bottom', ha='center', fontsize=12)
        
    plt.title(f"Vendas de {games_type} ({region_sales})", fontdict=font, fontsize=16)
    plt.ylabel('Número de Títulos', fontsize=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.tight_layout()
    plt.show()

def plot_top_games_by_region(df, region_key):
    region_name = region_info[region_key]['region_name']
    color = region_info[region_key]['color']
    top_games = get_top_games_by_region(df, region_key)
    preposition = region_prepositions.get(region_name, 'em')
    
    plt.figure(figsize=(14, 6))
    bars = plt.barh(top_games.index, top_games.values, color=color)
    
    for bar in bars:
        width = bar.get_width()
        plt.text(width + width*0.01, bar.get_y() + bar.get_height()/2, f'{width:.2f}', 
                 va='center', fontsize=12)
    
    plt.xlabel('Vendas (milhões de unidades)', fontsize=13)
    plt.title(f"Top 10 jogos mais vendidos {preposition} {region_name}", fontdict=font, fontsize=16)
    plt.gca().invert_yaxis()
    plt.xticks(fontsize=13)
    plt.yticks(fontsize=13)
    plt.tight_layout()
    plt.show()

def plot_top_games(top_games, console_name, region_name, color):
    plt.barh(top_games.index, top_games.values, color=color)
    plt.xlabel('Cópias vendidas')
    plt.title(region_name, fontsize=14)
    plt.gca().invert_yaxis()
    plt.xticks(fontsize=11)
    plt.yticks(fontsize=11)

    for i, value in enumerate(top_games.values):
        offset = value * 0.02
        plt.text(value + offset, i, f'{value:.2f}', va='center', fontsize=10)

def plot_top_games_by_console_and_region(df, platforms, regions, gen, region_info):
    for platform in gen.keys():
        console_name = gen[platform]['console_name'] 

        plt.figure(figsize=(14, 3))
        plt.suptitle(f"Top 10 jogos mais vendidos para {console_name}", fontdict=font, fontsize=16, y=1.05)

        for idx, region_sales in enumerate(regions, start=1):
            top_games_data = get_top_games_by_platform(df, platform, region_sales)
            region_name = region_info[region_sales]['region_name']
            color = region_info[region_sales]['color'] 

            plt.subplot(1, len(regions), idx)
            plot_top_games(top_games_data, console_name, region_name, color)

            ax = plt.gca()
            ax.set_xlim(0, top_games_data.max() * 1.1)

        plt.tight_layout()
        plt.subplots_adjust(top=0.85) 
        plt.show()

def plot_titles_by_genre(df, gen):
    titles_by_genre = df.groupby(['platform', 'genre']).size().sort_values(ascending=False)
    results = {console: titles_by_genre.loc[console].to_dict() for console in gen}
    
    fig, ax = plt.subplots(figsize=(10, 6))

    consoles = list(results.keys())
    generos = list(results[consoles[0]].keys())
    num_consoles = len(consoles)
    bar_width = 4.0 
    bar_padding = 1.2
    genre_padding = 3.0

    for i, console_code in enumerate(consoles):
        console_info = gen[console_code]
        bar_positions = [j * (len(consoles) * (bar_width + bar_padding) + 
                              genre_padding) + i * (bar_width + bar_padding) for j in range(len(generos))]
        counts = [results[console_code].get(genre, 0) for genre in generos]
        color = console_info['color']
        ax.barh(bar_positions, counts, height=bar_width, color=color, edgecolor='black', label=console_code)

        for j, count in enumerate(counts):
            offset = max(counts) * 0.008
            ax.text(count + offset, bar_positions[j], str(count), ha='left', va='center', color='black')

    plt.xticks(fontsize=11)
    plt.yticks(fontsize=11)

    ax.set_yticks([j * (len(consoles) * (bar_width + bar_padding) + genre_padding) + 
                   (len(consoles) - 1) * (bar_width + bar_padding) / 2 for j in range(len(generos))])
    ax.set_yticklabels(generos)
    ax.set_xlabel('Número de Títulos')
    ax.set_ylabel('Gênero', fontsize=11)
    ax.set_title('Número de títulos por gênero', 
                 fontdict = font, fontsize=16)
    ax.legend()

    plt.tight_layout()
    plt.gca().invert_yaxis()
    plt.show()

def plot_top_genres_by_region(df, regions, country_colors):
    plt.figure(figsize=(9, 5))
    plt.suptitle("Top 5 gêneros mais vendidos por região", fontdict=font, fontsize=16, y=0.99)
    
    for idx, region_sales in enumerate(regions, start=1):
        top_genres = df.groupby('genre')[region_sales].sum().sort_values(ascending=False).head()
        region_name = country_colors[region_sales]['region_name']
        color = country_colors[region_sales]['color']
        
        plt.subplot(len(regions), 1, idx)
        plt.barh(top_genres.index, top_genres.values, color=color)
        plt.xlabel('Vendas (milhões de cópias)', fontsize=12)
        plt.title(region_name)
        plt.gca().invert_yaxis()
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        
        offset = 0.2 if region_sales == 'jp_sales' else 1.0
        for i, (genre, value) in enumerate(top_genres.items()):
            plt.text(value + offset, i, f'{value:.2f}', va='center', fontsize=10)
        
        ax = plt.gca()
        ax.set_xlim(0, top_genres.max() * 1.1)
    
    plt.tight_layout()
    plt.subplots_adjust(top=0.88)
    plt.show()

def plot_market_share_by_genre(df, regions, region_info):
    n_regions = len(regions)
    fig, axes = plt.subplots(n_regions, 1, figsize=(10, 6 * n_regions))

    for ax, region_sales in zip(axes, regions):
        region_name = region_info[region_sales]['region_name']
        preposition = region_prepositions.get(region_name, 'em')
        
        total_sales_region = df[region_sales].sum()
        genre_sales = df.groupby('genre')[region_sales].sum()
        market_share = (genre_sales / total_sales_region * 100).sort_values(ascending=True)
        
        genres = market_share.index
        shares = market_share.values
        
        colors = plt.cm.tab20.colors[:len(genres)]
        bars = ax.barh(genres, shares, color=colors, edgecolor='black')

        for bar, share in zip(bars, shares):
            ax.text(bar.get_width() + 0.2, bar.get_y() + bar.get_height()/2, f'{share:.1f}%', va='center', fontsize=10)
        
        ax.set_xlabel('Participação de mercado', fontsize=12)
        ax.set_ylabel('Gênero', fontsize=12)
        ax.set_title(f'Participação de mercado por gênero {preposition} {region_name}',
                     fontdict=font, fontsize=16, pad=15)
        ax.set_xlim(0, max(shares) + 2)
    
    plt.tight_layout()
    plt.show()

def plot_top_titles_by_region(df, genre, country_colors, regions):
    plt.figure(figsize=(11, 8))
    plt.suptitle(f"Top 10 títulos de {genre} por região", fontdict=font, fontsize=16, y=0.99)

    for idx, region_sales in enumerate(regions, start=1):
        region_name = country_colors[region_sales]['region_name']
        color = country_colors[region_sales]['color']

        genre_data = df[df['genre'] == genre]
        region_sales_data = genre_data.groupby('title')[region_sales].sum().reset_index()
        top_titles = region_sales_data.sort_values(by=region_sales, ascending=False).head(10)
        short_titles = top_titles['title'].apply(shorten_title)

        plt.subplot(len(regions), 1, idx)
        bars = plt.barh(short_titles, top_titles[region_sales], color=color)
        plt.xlabel('Cópias vendidas', fontsize=12)
        plt.title(region_name, fontsize=14)
        plt.gca().invert_yaxis()
        plt.xticks(fontsize=11)
        plt.yticks(fontsize=11)

        for bar in bars:
            width = bar.get_width()
            offset = width * 0.02
            plt.text(width + offset, bar.get_y() + bar.get_height()/2, f'{width:.2f}', va='center', fontsize=11)

        ax = plt.gca()
        ax.set_xlim(0, top_titles[region_sales].max() * 1.1)
    
    plt.tight_layout()
    plt.subplots_adjust(left=0.3)
    plt.show()

def plot_top_genres_by_console_and_region(df, gen, regions):
    for platform in gen.keys():
        console_name = gen[platform]['console_name']
        plt.figure(figsize=(14, 3))
        plt.suptitle(f"Top 5 gêneros mais vendidos para {console_name}", fontdict=font, fontsize=16, y=1.05)

        for idx, region_sales in enumerate(regions, start=1):
            top_genres = (
                df[df['platform'] == platform]
                .groupby('genre')[region_sales]
                .sum()
                .sort_values(ascending=False)
                .head()
            )

            region_name = region_info[region_sales]['region_name']
            color = region_info[region_sales]['color']

            plt.subplot(1, len(regions), idx)
            plt.barh(top_genres.index, top_genres.values, color=color)
            plt.xlabel('Vendas (milhões de cópias)', fontsize=12)
            plt.title(region_name, fontsize=14)
            plt.gca().invert_yaxis()
            plt.xticks(fontsize=12)
            plt.yticks(fontsize=12)

            for i, value in enumerate(top_genres.values):
                plt.text(value + value * 0.02, i, f'{value:.2f}', va='center', fontsize=11)

            ax = plt.gca()
            ax.set_xlim(0, top_genres.max() * 1.1)

        plt.tight_layout()
        plt.subplots_adjust(top=0.85)
        plt.show()

def plot_top_rated_score(df, gen, score_type, count_type):
    top_rated_plot = get_top_rated_score(df, gen, score_type, count_type)
   
    plt.figure(figsize=(10, 6))
    bars = plt.barh(
        top_rated_plot['title'],
        top_rated_plot['mean_score'],
        color='#987654',
        edgecolor='black'
    )

    for bar, score in zip(bars, top_rated_plot['mean_score']):
            plt.text(
                bar.get_width() + 0.05,
                bar.get_y() + bar.get_height() / 2,
                f"{score:.2f}",
                va='center',
                ha='left',
                fontsize=12
            )

    plt.xlabel(score_type, fontsize=12)
    plt.title(f"Top 10 jogos da geração ({score_labes[score_type]})", fontdict=font, fontsize=16)
    plt.xlim(0, 10)
    plt.yticks(fontsize=12)
    plt.gca().invert_yaxis()
    ax = plt.gca()
    ax.set_xlim(0, top_rated_plot['mean_score'].max() * 1.1)
    plt.tight_layout()
    plt.show()

def plot_genres_count_by_publishers_global(df):
    top_publishers_na = get_top_publishers_by_region(df, 'na_sales')
    top_publishers_jp = get_top_publishers_by_region(df, 'jp_sales')
    top_publishers = pd.concat([top_publishers_na, top_publishers_jp]).drop_duplicates()
    top_publishers_list = top_publishers.index.tolist()   

    genres_data = get_genres_count_by_publishers(df, top_publishers_list)
    genres_data = genres_data.sort_index(ascending=False)
    genres_data.plot(kind='barh', stacked=True, figsize=(12, 8), colormap='tab20')

    plt.title(f"Distribuição de genêros publicados pelas top 10 publishers", fontdict = font, fontsize=16)
    plt.xlabel('Número de Jogos', fontsize=12)
    plt.ylabel('Publisher', fontsize=12)
    plt.xticks(fontsize=11)
    plt.yticks(fontsize=11)

def plot_top_exclusives_console_by_region(df, platform, gen, regions):
    for platform in gen.keys():
        console_name = gen[platform]['console_name']       
        exclusives = df[(df['platform'] == platform) &
                        ~(df['title'].isin(df[df['platform'] != platform]['title']))]
    
        plt.figure(figsize=(14, 4))
        plt.suptitle(f"{console_name} - Top 10 exclusivos por região", 
                     fontdict=font, fontsize=16, y=0.95)
        
        for idx, region_sales in enumerate(regions, start=1):
            top_exclusives = exclusives[['title', region_sales]] \
                              .sort_values(by=region_sales, ascending=False) \
                              .head(10)
            top_exclusives.index = range(1, len(top_exclusives)+1)
            region_name = region_info[region_sales]['region_name']
            color = region_info[region_sales]['color']
            
            plt.subplot(1, len(regions), idx)
            plt.barh(top_exclusives['title'], top_exclusives[region_sales], color=color)
            plt.gca().invert_yaxis()
            plt.title(region_name, fontsize=14)
            plt.xlabel("Cópias vendidas (milhões)", fontsize=12)
            plt.xticks(fontsize=12)
            plt.yticks(fontsize=12)

            for i, value in enumerate(top_exclusives[region_sales]):
                plt.text(value + (value * 0.02), i, f'{value:.2f}', va='center', fontsize=11)
            
            ax = plt.gca()
            ax.set_xlim(0, top_exclusives[region_sales].max() * 1.1)
        
        plt.tight_layout()
        plt.subplots_adjust(top=0.8)
        plt.show()

def plot_sales_histograms(df, region_sales):
    sales_data = {key: df.loc[df[key] > 0, key] for key in region_sales}
    fig, axs = plt.subplots(1, len(region_sales), figsize=(15,6))
    
    if len(region_sales) == 1:
        axs = [axs]
    
    for ax, key in zip(axs, region_sales):
        region = region_info[key]
        region_name = region['region_name']
        preposition = region_prepositions.get(region_name, 'em')
        
        ax.hist(sales_data[key], bins=30, color=region['color'], edgecolor='black')
        ax.set_title(f'Distribuição de vendas {preposition} {region_name}', fontdict=font, fontsize=16)
        ax.set_xlabel('Cópias vendidas', fontsize=14)
        ax.set_ylabel('Frequência', fontsize=14)
        ax.set_yscale('log')
        ax.yaxis.set_major_formatter(mticker.ScalarFormatter())
        step = 0.5 if 'jp_' in key else 5
        ax.set_xticks(np.arange(0, sales_data[key].max() + step, step))
        ax.tick_params(axis='both', which='major', labelsize=12)
    
    if len(axs) > 1:
        ylim = axs[0].get_ylim()
        for ax in axs[1:]:
            ax.set_ylim(ylim)
    
    plt.tight_layout()
    plt.show()

def plot_platform_sales_histograms(df, gen, region_sales):
    platforms = gen.keys() 
    n_platforms = len(platforms)
    n_regions = len(region_sales)
    
    fig, axs = plt.subplots(n_platforms, n_regions, figsize=(15, 10))
    
    if n_platforms == 1 and n_regions == 1:
        axs = [[axs]]
    elif n_platforms == 1:
        axs = [axs]
    elif n_regions == 1:
        axs = [[ax] for ax in axs]
    
    for i, platform in enumerate(platforms):
        for j, key in enumerate(region_sales):
            ax = axs[i][j] if n_platforms > 1 and n_regions > 1 else axs[i] if n_regions > 1 else axs[j]
            platform_data = df[(df['platform'] == platform) & (df[key] > 0)][key]
            region = region_info[key]
            region_name = region['region_name']
            preposition = region_prepositions.get(region_name, 'em')
            platform_color = gen7[platform]['color'] if platform in gen7 else '#1f77b4'
            ax.hist(platform_data, bins=30, color=platform_color, edgecolor='black', alpha=0.7)
            ax.set_title(f'Vendas do {gen7[platform]["console_name"]} {preposition} {region_name}', 
                         fontdict=font, fontsize=16)
            ax.set_xlabel('Cópias vendidas', fontsize=12)
            ax.set_ylabel('Frequência', fontsize=12)
            ax.set_yscale('log')
            ax.yaxis.set_major_formatter(mticker.ScalarFormatter())
            step = 0.5 if 'jp_' in key else 5
            max_val = platform_data.max() if len(platform_data) > 0 else 1
            ax.set_xticks(np.arange(0, max_val + step, step))
            ax.tick_params(axis='both', which='major', labelsize=9)
            
    plt.tight_layout()
    plt.show()

def plot_top_publishers_by_region(df, region_sales):
    for region_sales in region_sales:
        top_publishers = get_top_publishers_by_region(df, region_sales)
        top_publishers = top_publishers[::-1]
        region_name = region_info[region_sales]['region_name']
        preposition = region_prepositions.get(region_name, 'em')

        plt.figure(figsize=(10, 6))
        bars = plt.barh(
        top_publishers.index,
        top_publishers.values,
        color=region_info[region_sales]['color']
    )
        plt.title(f"Top 10 publishers {preposition} {region_name} (por vendas)", fontdict = font, fontsize=16)
        plt.xlabel('Cópias vendidas', fontsize=12)
        plt.ylabel('Publisher', fontsize=12)
        plt.yticks(fontsize=11)
    
        offset = 0.2 if region_sales == 'jp_sales' else 1.0
        for bar in bars:
            width = bar.get_width()
            plt.text(width + offset, bar.get_y() + bar.get_height() / 2, f'{width:.1f}', va='center', fontsize=11)
    
        ax = plt.gca()
        ax.set_xlim(0, top_publishers.max() * 1.1)
        plt.tight_layout()
        plt.show()

def plot_rating_distribution(df, dropna):
    df['rating'] = df['rating'].replace({'EC': 'E'})
    rating_counts = df['rating'].value_counts(dropna=dropna)
    
    plt.figure(figsize=(7, 7))
    wedges, texts, autotexts = plt.pie(
        rating_counts, 
        labels=rating_counts.index, 
        autopct='%1.2f%%', 
        startangle=140, 
        textprops={'fontsize': 12},  
        colors=plt.cm.tab20.colors,  
        wedgeprops={'edgecolor': 'black'} 
    )
    plt.setp(autotexts, size=12, weight="bold") 
    plt.title('Distribuição de títulos lançados por classificação etária',
              fontdict=font, fontsize = 16)
    
    legend_labels = {
        'E': 'Everyone',
        'T': 'Teen',
        'M': 'Mature',
        'E10+': 'Everyone 10 and older',
        None: 'Unknown'
    }
    plt.legend(wedges, 
               [f"{label}: {legend_labels.get(label, 'Unknown')}" for label in rating_counts.index],
               title="Classificações", loc="center left", bbox_to_anchor=(1, 0.84))
    plt.show()

def plot_rating_distribution_by_platform(df, gen, dropna):
    df['rating'] = df['rating'].replace({'EC': 'E'})

    for platform, platform_info in gen.items():
        platform_df = df[df['platform'] == platform]
        rating_counts = platform_df['rating'].value_counts(dropna=dropna)
        
        plt.figure(figsize=(7, 7))
        plt.subplots_adjust(top=5.82)
        wedges, texts, autotexts = plt.pie(
            rating_counts, 
            labels=rating_counts.index, 
            autopct='%1.2f%%',
            startangle=140, 
            textprops={'fontsize': 12}, 
            colors=plt.cm.tab20.colors,
            wedgeprops={'edgecolor': 'black'},
        )
        
        plt.setp(autotexts, size=12, weight="bold") 
        
        plt.title(f'Distribuição de títulos lançados por classificação etária e plataforma', 
                  fontdict=font, fontsize=16)
        
        plt.text(0.5, 0.96, platform_info["console_name"], 
                 horizontalalignment='center', verticalalignment='center', 
                 transform=plt.gca().transAxes, fontsize=16)
        
        legend_labels = {
            'E': 'Everyone',
            'T': 'Teen',
            'M': 'Mature',
            'E10+': 'Everyone 10 and older',
            None: 'Unknown'
        }
        plt.legend(wedges, 
                   [f"{label}: {legend_labels.get(label, 'Unknown')}" for label in rating_counts.index],
                   title="Classificações", loc="center left", bbox_to_anchor=(1, 0.84))
        plt.show()

def plot_sales_by_rating_per_region(df, regions):
    for region in regions:
        plt.figure(figsize=(10, 6))
        
        region_name = region_info[region]['region_name']
        preposition = region_prepositions.get(region_name, 'em')
        sales_results = df.groupby('rating')[region].sum().reset_index().sort_values(by=region, ascending=False)

        plt.title(f'Vendas por classificação etária {preposition} {region_name}', fontdict=font, fontsize=16)
        bars = plt.bar(sales_results['rating'], sales_results[region], color = region_info[region]['color'])
        
        for bar, value in zip(bars, sales_results[region]):
            plt.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + (sales_results[region].max() * 0.01),
                str(round(value, 2)),
                va='bottom', ha='center', fontsize=12
            )

        plt.ylabel("Cópias vendidas", fontsize=14)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        plt.ylim(0, sales_results[region].max() * 1.2)

        plt.show()

def plot_sales_by_rating_per_platform(df, gen, regions):
    for region in regions:
        sales_by_rating = (
            df.groupby(['platform', 'rating'])[region]
              .sum()
              .unstack(fill_value=0)
        )

        platforms = gen.keys()
        plt.figure(figsize=(10, 4 * len(platforms)))

        region_name = region_info[region]['region_name']
        preposition = region_prepositions.get(region_name, 'em')

        plt.suptitle(
            f"Vendas por classificação etária {preposition} {region_name}",
            fontdict=font, fontsize=16, y=0.99
        )

        for i, platform in enumerate(platforms, start=1):
            plt.subplot(len(platforms), 1, i)
            

            sales = sales_by_rating.loc[platform].sort_values(ascending=False)
            
            bars = plt.bar(
                sales.index, sales.values,
                color=gen[platform].get('color', '#999999'), width=0.5
            )

            for bar, value in zip(bars, sales.values):
                plt.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + (sales.values.max() * 0.01),
                    str(round(value, 2)),
                    va='bottom', ha='center', fontsize=12
                )

            plt.title(f'{gen[platform]['console_name']}', fontsize=14)
            plt.ylim(0, sales.max() * 1.2)
            plt.xticks(fontsize=12)
            plt.yticks(fontsize=12)

        plt.tight_layout()
        plt.show()

