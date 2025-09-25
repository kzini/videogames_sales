import pandas as pd
from src.constants import year_mapping_gen7, region_prepositions, region_info, color

def remove_duplicates_per_platform(df, gen):
    df_clean = []
    
    for platform in gen:
        platform_data = df[df['platform'] == platform]
        duplicates_before = platform_data['title'].duplicated().sum()
        console_name = gen[platform]['console_name']

        print("Número de títulos duplicados na plataforma", console_name,
              "antes da remoção:", duplicates_before)

        platform_data = platform_data.drop_duplicates(subset=['title'], keep='first')
        duplicates_after = platform_data['title'].duplicated().sum()

        print("Número de títulos duplicados na plataforma",
              console_name, "após a remoção:", duplicates_after)
        print("")

        df_clean.append(platform_data)

        # Linha de separação (menos na última plataforma)
        if platform != list(gen.keys())[-1]:
            print()
    
    return pd.concat(df_clean, ignore_index=True)

def display_null(df):
    print("Valores nulos em: df_7th_gen\n")
    for col in df.columns.tolist():
        print(col, df[col].isnull().sum())
    print('\n')

def update_year_of_release(df, year_mapping):
    for title, year in year_mapping.items():
        idx = df[df['title'] == title].index
        df.loc[idx, 'year_of_release'] = year

    print(f"Valores nulos restantes: {df['year_of_release'].isnull().sum()}")

def update_publisher(df, title, publisher):
    idx = df[df['title'] == title].index
    df.loc[idx, 'publisher'] = publisher

def get_sales_by_platform_region(df, platform, region):
    sales_by_platform = df.groupby('platform')[[region]].sum()
    total_sales = sales_by_platform.loc[platform, region]
    return round(total_sales, 2)

def calculate_percentage_sales(total_sales, total_global_sales):
    return (total_sales / total_global_sales) * 100

def count_titles_by_platform(df):
    return df['platform'].value_counts()

def get_console_exclusives_by_year(df, platform, year):
    title_counts = df['title'].value_counts()
    exclusives = df[
        (df['platform'] == platform) & 
        (df['year_of_release'] == year) &
        (df['title'].map(title_counts) == 1)
    ][['title', 'genre', 'year_of_release', 'global_sales', 'na_sales', 'jp_sales', 'critic_score', 'user_score']]
    
    exclusives = exclusives.sort_values('global_sales', ascending=False)
    exclusives = exclusives.reset_index(drop=True)
    exclusives.index = exclusives.index + 1
    
    return exclusives

def get_console_releases_by_year(df, platform, year):
    title_counts = df['title'].value_counts()
    releases = df[
        (df['platform'] == platform) & 
        (df['year_of_release'] == year)
    ][['title', 'genre', 'year_of_release', 'global_sales']]
    
    releases = releases.sort_values('global_sales', ascending=False)
    releases = releases.reset_index(drop=True)
    releases.index = releases.index + 1
    
    return releases

def get_top_games_by_region(df, region_sales):
    top_games_by_region = df.groupby('title')[region_sales].sum().sort_values(ascending=False).head(10)
    return top_games_by_region

def get_top_games_by_platform(df, platform, region_sales):
    console = df[df['platform'] == platform]
    top_games = console.groupby('title')[region_sales].sum().sort_values(ascending=False).head(10)
    return top_games

def display_top_games_by_platform_and_region(df, gen7, regions):
    for platform, platform_info in gen7.items():
        console_name = platform_info['console_name']
        
        for region in regions:
            region_name = region_info[region]['region_name']
            top_games = get_top_games_platform(df, platform, region)
            
            titles_info = df[['title', 'publisher', 'developer', 'year_of_release', 'genre', 'rating', 
                              'critic_score', 'user_score']].drop_duplicates('title')
            top_games = top_games.reset_index().merge(titles_info, on='title', how='left')
            
            top_games.index = range(1, len(top_games) + 1)
            preposition = region_prepositions.get(region_name, 'em')

            print(f"Top 10 jogos mais vendidos de {console_name} {preposition} {region_name}:")
            display(top_games)

def shorten_title(title, max_length=40):
    if len(title) > max_length:
        return title[:max_length] + '...'
    return title

def get_top_rated_score(df, gen, score_type, count_type):
    df_filtered = df[df[count_type] >= df[count_type].mean()]
    df_avg_score = df_filtered.groupby('title').agg(
    mean_score=(score_type, 'mean')).reset_index()

    top_rated = df_avg_score.sort_values(
        by='mean_score', 
        ascending=False
    ).head(10)

    return top_rated

def get_genres_count_by_publishers(df, publishers):
    df_filtered = df[df['publisher'].isin(publishers)]
    genres_by_publishers = df_filtered.groupby(['publisher', 'genre']).size().unstack(fill_value=0)
    genres_by_publishers = genres_by_publishers.sort_index()
    return genres_by_publishers

def get_top_publishers_by_region(df, region_sales):
    total_sales = df.groupby('publisher')[region_sales].sum().sort_values(ascending=False)
    top_publishers = total_sales.head(10)
    return top_publishers

def display_top_10_games(df, region_sales):
    for region_sales in region_sales:
        top_10_games = (
            df.groupby('title')[region_sales]
              .sum()
              .sort_values(ascending=False)
              .head(10)
              .reset_index()
        )

        titles_info = df[['title', 'publisher', 'developer', 'genre', 'rating', 'critic_score', 'user_score']]
        top_10_games = top_10_games.merge(titles_info, on='title', how='left')
        top_10_games.index = range(1, len(top_10_games) + 1)
        
        region_name = region_info[region_sales]['region_name']
        preposition = region_prepositions.get(region_name, 'em')

        print(f"\nTop 10 jogos mais vendidos da 7ª geração {preposition} {region_name}:\n")
        display(top_10_games)

def display_top_10_games_by_platform(df, gen, regions):
    for platform, info in gen.items():
        platform_df = df[df['platform'] == platform]
        console_name = info['console_name']
        
        for region in regions:
            top_10_games = (
                platform_df.groupby('title')[region]
                .sum()
                .sort_values(ascending=False)
                .head(10)
                .reset_index()
            )

            titles_info = platform_df[['title', 'publisher', 'developer', 'genre', 'rating', 'critic_score', 'user_score']]
            top_10_games = top_10_games.merge(titles_info, on='title', how='left')
            top_10_games.index = range(1, len(top_10_games) + 1)
            
            region_name = region_info[region]['region_name']
            preposition = region_prepositions.get(region_name, 'em')

            print(f"\nTop 10 jogos mais vendidos para {console_name} {preposition} {region_name}:\n")
            display(top_10_games)

def filter_and_print_top_exclusives(df, gen, regions):
    for platform in gen.keys():
        console_name = gen[platform]['console_name']
        exclusives = df[
            (df['platform'] == platform) &
            ~(df['title'].isin(df[df['platform'] != platform]['title']))
        ]

        for region in regions:
            region_name = region_info[region]['region_name']
            top_region_sales = (
                exclusives[['title', 'year_of_release', region, 'genre', 'rating']]
                .sort_values(by=region, ascending=False)
                .head(10)
            )
            top_region_sales.index = range(1, len(top_region_sales) + 1)

            print(f"\n{console_name} - Top 10 títulos exclusivos mais vendidos em {region_name}:")
            display(top_region_sales)

def get_publisher_sales(df, publisher, region):
    publisher_sales = df[df['publisher'] == publisher].groupby('publisher')[region].sum()
    return publisher_sales

def print_publisher_sales(df, publishers, region):
    for publisher in publishers:
        sales = get_publisher_sales(df, publisher, region)
        print(f"{publisher}: {sales.values[0]:,.2f}")


def filter_and_print_exclusives(df, platform, gen, regions):
    exclusives = df[
        (df['platform'] == platform) &
        ~(df['title'].isin(df[df['platform'] != platform]['title']))
    ]
    num_exclusives = exclusives['title'].nunique()
    console_name = gen[platform]['console_name']

    print(f"{color.UNDERLINE}{console_name}{color.END}")
    print(f"Exclusivos: {num_exclusives}")

    for region in regions:
        region_sales = round(exclusives[region].sum(), 2)
        region_name = region_info[region]['region_name']
        print(f"Cópias vendidas em {region_name}: {region_sales:,.2f}")

    print()

def print_exclusives_by_platforms(df, gen, regions):
    print(f"{color.BOLD}Vendas de títulos exclusivos por console{color.END}\n")
    for platform in gen:
        filter_and_print_exclusives(df, platform, gen, regions)

class color:
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    GREEN = '\033[92m'
    END = '\033[0m'

def get_region(df, region_sales):
    if region_sales == "jp_sales":
        return df[(df["na_sales"] == 0) &
                  (df["eu_sales"] == 0) &
                  (df["other_sales"] == 0) &
                  (df["jp_sales"] > 0)]
    elif region_sales == "na_sales":
        return df[(df["jp_sales"] == 0) &
                  (df["eu_sales"] == 0) &
                  (df["other_sales"] == 0) &
                  (df["na_sales"] > 0)]
    else:
        return None

def get_n_exclusives(df, platform, region_sales):
    region_sales_df = get_region(df, region_sales)
    if region_sales_df is not None:
        return len(region_sales_df[region_sales_df['platform'] == platform])
    else:
        return 0

def get_region_only_sales(df, platform, region_sales):
    region_sales_df = get_region(df, region_sales)
 
    return round(region_sales_df[region_sales_df['platform'] == platform][region_sales].sum(), 2)

def print_exclusives_by_region(df, gen, regions): 
    print(color.BOLD + "Títulos exclusivos por região" + color.END)
    print("")

    for platform, info in gen.items():  # use 'gen', não 'gen7'
        console_name = info['console_name']
        print(color.UNDERLINE + console_name + color.END)

        for region in regions:
            region_name = region_info[region]['region_name']
            count = get_n_exclusives(df, platform, region)
            sales = get_region_only_sales(df, platform, region)
            print(f"{region_name}: {count} jogos exclusivos, com um total de vendas de {sales} milhões de cópias vendidas.")

        # Adiciona uma linha de separação entre consoles, exceto após o último
        if platform != list(gen.keys())[-1]:
            print()

def get_sales_and_exclusives(df, gen, regions):
    data = {'console': [], 'region': [], 'sales': []}
    
    for platform, info in gen.items():
        console_name = info['console_name']
        for region in regions:
            sales = get_region_only_sales(df, platform, region)
            data['console'].append(console_name)
            data['region'].append(region)
            data['sales'].append(sales)
    
    return pd.DataFrame(data)

def group_and_sum_sales_by_rating(df, gen, regions):
    results = {}
    
    for platform, info in gen.items():
        platform_df = df[df['platform'] == platform]
        grouped = platform_df.groupby('rating')[regions].sum()
        grouped = grouped.sort_values(by=regions, ascending=False)
        results[platform] = grouped

    return results













