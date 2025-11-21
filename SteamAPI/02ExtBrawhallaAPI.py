# ----
# Script de extração de dados da API da SteamWorks
# Análise dos resultados pode ser encontrada no
# arquivo "01testeSteamAPI.ipynb"
# ----

# Setup ----
import requests
import pandas as pd
import time


def extrairReviews(params: dict, limite: int = 1e3):
    """
    Acessa a API da SteamWorks utilizando uma operação GET.

    params: Dicionário dos parâmetros da função.
    limite: Número máximo de reviews para serem pegas
    """
    reviews = []
    while len(reviews) < limite:
        # Simula o GET
        resp = requests.get(f'https://store.steampowered.com/appreviews/{app_id}', params=params)
        data = resp.json()
        # Pega as reviews da variável em json
        reviews_atual = data.get('reviews')
        
        if not reviews_atual:
            break

        reviews.extend(reviews_atual)

        # Move para a próxima página
        cursor = data.get('cursor')
        if not cursor or cursor == params['cursor']:
            break

        params['cursor'] = cursor

        # Print do total de reviews:
        print("Total extraído: ", len(reviews))

        # Espera para não acharem ser DDOS
        time.sleep(1)

    # Por agora tá tacando literalmente todas as infos no .csv
    return pd.DataFrame(reviews)


# Extração ----
app_id = 291550  # Código do Brawhalla

# Dicionário de parâmetros
params = {
    'json': 1,
    'review_type': 'positive',
    # Em inglês tem mais reviews (em geral)
    'language': 'english',
    'filter': 'recent',
    'num_per_page': 100,
    'cursor': '*',
    'filter_offtopic_activity':0,
    'purchase_type':'all'
}

limite = 5200

# Positivos
params["review_type"] = 'positive'

print("Extraindo reviews positivas.")
reviews = extrairReviews(params, limite)
reviews.to_csv('SteamAPI/brawhalla_pos.csv', index=False)
print(f"Reviews positivas coletadas: {len(reviews)}.")

# Negativos
params["review_type"] = 'negative'

print("Extraindo reviews negativas.")
reviews = extrairReviews(params, limite)
reviews.to_csv('SteamAPI/brawhalla_neg.csv', index=False)
print(f"Reviews negativas coletadas: {len(reviews)}.")
