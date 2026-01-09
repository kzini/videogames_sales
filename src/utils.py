import requests
import pandas as pd
from datetime import datetime
import time
import os
from dotenv import load_dotenv
from src.constants import region_prepositions, region_info, color

def remove_duplicates_per_platform(df, gen):
    df_clean = []
    
    for platform in gen:
        platform_data = df[df['platform'] == platform].copy()
        console_name = gen[platform]['console_name']
        
        print(f"\n{console_name}:")
        print(f"  Linhas antes: {len(platform_data)}")
        
        duplicates_before = platform_data.duplicated().sum()
        platform_data = platform_data.drop_duplicates(keep='first')
        duplicates_after = platform_data.duplicated().sum()
        
        print(f"  Duplicatas exatas removidas: {duplicates_before}")
        print(f"  Linhas depois: {len(platform_data)}")
        
        titulos_dups = platform_data['title'].duplicated().sum()
        if titulos_dups > 0:
            print(f"{titulos_dups} títulos ainda duplicados")
            dup_titles = platform_data[platform_data['title'].duplicated(keep=False)]['title'].unique()
            for title in dup_titles:
                print(f"    - {title}")
        
        df_clean.append(platform_data)
    
    resultado = pd.concat(df_clean, ignore_index=True)
    
    return resultado

def display_null(df):
    print("Valores nulos em: df_7th_gen\n")
    for col in df.columns.tolist():
        print(col, df[col].isnull().sum())
    print('\n')

def update_year_of_release(df, year_dict):
    for title, year in year_dict.items():
        idx = df[df['title'] == title].index
        df.loc[idx, 'year_of_release'] = year

    print(f"Valores nulos restantes: {df['year_of_release'].isnull().sum()}")

def update_publisher(df, title, publisher):
    idx = df[df['title'] == title].index
    df.loc[idx, 'publisher'] = publisher

def update_esrb_ratings(df, esrb_dict):
    for game_title, esrb_rating in esrb_dict.items():
        idx = df[df['title'] == game_title].index
        df.loc[idx, 'rating'] = esrb_rating

    print(f"Valores nulos restantes em 'rating': {df['rating'].isnull().sum()}")

def get_sales_by_platform_region(df, platform, region):
    sales_by_platform = df.groupby('platform')[[region]].sum()
    total_sales = sales_by_platform.loc[platform, region]
    return round(total_sales, 2)

def calculate_percentage_sales(total_sales, total_global_sales):
    return (total_sales / total_global_sales) * 100

def count_titles_by_platform(df):
    return df['platform'].value_counts()

def get_top_console_titles_by_year(df, platform, year):
    title_counts = df['title'].value_counts()
    exclusives = df[
        (df['platform'] == platform) & 
        (df['year_of_release'] == year)
    ][['title', 'genre', 'year_of_release', 'rating', 'publisher', 'global_sales', 'na_sales', 'jp_sales', 'critic_score', 'user_score']]
    
    exclusives = exclusives.sort_values('global_sales', ascending=False)
    exclusives = exclusives.reset_index(drop=True)
    exclusives.index = exclusives.index + 1
    
    return exclusives

def get_console_releases_by_year(df, platform, year):
    title_counts = df['title'].value_counts()
    releases = df[
        (df['platform'] == platform) & 
        (df['year_of_release'] == year)
    ][['title', 'genre', 'publisher', 'rating', 'global_sales', 'na_sales', 'jp_sales']]
    
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

def display_top_10_games(df, region_sales_list):
    title_metadata = (
        df
        .groupby('title', as_index=False)
        .agg({
            'publisher': lambda x: x.dropna().mode().iloc[0] if not x.dropna().empty else None,
            'developer': lambda x: x.dropna().mode().iloc[0] if not x.dropna().empty else None,
            'genre': lambda x: x.dropna().mode().iloc[0] if not x.dropna().empty else None,
            'rating': lambda x: x.dropna().mode().iloc[0] if not x.dropna().empty else None,
        })
    )

    for region_sales in region_sales_list:
        top_10_games = (
            df
            .groupby('title')[region_sales]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
            .merge(title_metadata, on='title', how='left')
        )

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
                exclusives[['title', 'year_of_release', 'publisher', region, 'genre', 'rating']]
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

load_dotenv(dotenv_path='../.env')
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

def get_token():
    url = "https://id.twitch.tv/oauth2/token"
    params = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'client_credentials'
    }
    response = requests.post(url, params=params)
    return response.json()['access_token'] if response.status_code == 200 else None

def search_years_dict(titles): 
    token = get_token()
    if not token:
        print("Falha ao obter token")
        return {}
    
    url = "https://api.igdb.com/v4/games"
    headers = {
        'Client-ID': CLIENT_ID,
        'Authorization': f'Bearer {token}'
    }
    
    year_dict = {}
    
    print(f"Buscando {len(titles)} títulos...\n")
    
    for i, title in enumerate(titles, 1):
        # Busca 3 resultados para ter fallback
        body = f'fields name, first_release_date; search "{title}"; limit 3;'
        
        try:
            response = requests.post(url, headers=headers, data=body, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if data:
                    found_year = None
                    
                    for game in data:
                        if game.get('first_release_date'):
                            try:
                                year = datetime.fromtimestamp(game['first_release_date']).year
                                
                                if 2005 <= year <= 2016:
                                    found_year = year
                                    break  # Para no primeiro válido
                            except:
                                continue
                    
                    if found_year:
                        year_dict[title] = found_year
                        print(f"O {i:3d}/{len(titles)}: {title[:30]:30} {found_year}")
                    else:
                        if data[0].get('first_release_date'):
                            try:
                                bad_year = datetime.fromtimestamp(data[0]['first_release_date']).year
                                print(f"X {i:3d}/{len(titles)}: {title[:30]:30} {bad_year} (fora de 2005-2016)")
                            except:
                                print(f"X {i:3d}/{len(titles)}: {title[:30]:30} Sem ano válido")
                        else:
                            print(f"X {i:3d}/{len(titles)}: {title[:30]:30} Sem data")
                else:
                    print(f"X {i:3d}/{len(titles)}: {title[:30]:30} Não encontrado")
            else:
                print(f"X {i:3d}/{len(titles)}: {title[:30]:30} ERRO {response.status_code}")
        
        except Exception as e:
            print(f"X {i:3d}/{len(titles)}: {title[:30]:30} ERRO: {str(e)[:30]}")
        
        time.sleep(0.26)
    
    return year_dict

def get_esrb_ratings_igdb(titles):
    token = get_token()
    if not token:
        print("Falha ao obter token")
        return {}
    
    esrb_dict = {}
    
    print(f"Buscando classificações ESRB para {len(titles)} títulos...\n")
    
    for i, title in enumerate(titles, 1):
        try:
            body = f'''
            fields name, age_ratings.*;
            search "{title}";
            limit 3;
            '''
            
            headers = {
                'Client-ID': CLIENT_ID,
                'Authorization': f'Bearer {token}'
            }
            
            response = requests.post("https://api.igdb.com/v4/games", 
                                   headers=headers, data=body, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if data:
                    esrb_found = None
                    
                    for game in data:
                        if 'age_ratings' in game and game['age_ratings']:
                            for rating in game['age_ratings']:
                                # organization 1 = ESRB
                                if rating.get('organization') == 1:
                                    rating_category = rating.get('rating_category')
                                    if rating_category is not None:
                                        esrb_found = rating_category
                                        break
                        
                        if esrb_found:
                            break
                    
                    if esrb_found is not None:
                        esrb_text = convert_esrb_code(esrb_found)
                        
                        if esrb_text:
                            esrb_dict[title] = esrb_text
                            
                            if esrb_found == 6 and esrb_text == "M":
                                print(f"O {i:3d}/{len(titles)}: {title[:30]:30} {esrb_text} (AO -> M)")
                            else:
                                print(f"O {i:3d}/{len(titles)}: {title[:30]:30} {esrb_text}")

                    else:
                        print(f"X {i:3d}/{len(titles)}: {title[:30]:30} Sem ESRB")
                else:
                    print(f"X {i:3d}/{len(titles)}: {title[:30]:30} Não encontrado")
            else:
                print(f"X {i:3d}/{len(titles)}: {title[:30]:30} ERRO {response.status_code}")
        
        except Exception as e:
            print(f"X {i:3d}/{len(titles)}: {title[:30]:30} ERRO: {str(e)[:30]}")
        
        time.sleep(0.26)
    
    return esrb_dict


def convert_esrb_code(category):
    esrb_map = {
        1: "EC",
        2: "E", 
        3: "E10+",
        4: "T",
        5: "M",
        6: "M"
    }
    
    return esrb_map.get(category)
    