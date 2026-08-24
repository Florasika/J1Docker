"""
JOUR 1 / 10 — Docker
Application : pipeline ETL simple dans un conteneur

Ce script tourne DANS le conteneur Docker.
Il lit des données, les transforme, et écrit le résultat.
"""

import pandas as pd
import os
import json
from datetime import datetime

DATA_PATH   = os.getenv('DATA_PATH',   '/app/data')
OUTPUT_PATH = os.getenv('OUTPUT_PATH', '/app/output')


def extraire():
    """Génère des données de ventes simulées."""
    import random
    random.seed(42)

    produits = ['Laptop Pro','Smartphone X','Tablette Air','Écouteurs BT']
    prix     = {'Laptop Pro':1200,'Smartphone X':650,
                'Tablette Air':450,'Écouteurs BT':120}
    vendeurs = ['Alice','Karim','Lucie','Thomas','Nadia']

    rows = []
    for _ in range(30):
        p   = random.choice(produits)
        qte = random.randint(1, 10)
        rows.append({
            'date'    : datetime.now().strftime('%Y-%m-%d'),
            'produit' : p,
            'vendeur' : random.choice(vendeurs),
            'quantite': qte,
            'montant' : qte * prix[p],
        })

    df = pd.DataFrame(rows)
    print(f"[EXTRACT] {len(df)} lignes extraites")
    return df


def transformer(df: pd.DataFrame) -> pd.DataFrame:
    """Enrichit les données."""
    df = df.copy()
    df['marge']        = (df['montant'] * 0.42).round(2)
    df['taille_vente'] = pd.cut(
        df['montant'],
        bins=[0, 500, 2000, float('inf')],
        labels=['Petite', 'Moyenne', 'Grosse']
    ).astype(str)
    print(f"[TRANSFORM] Marge ajoutée — CA: {df['montant'].sum():.0f}€")
    return df


def charger(df: pd.DataFrame):
    """Sauvegarde les résultats dans /app/output (volume monté)."""
    os.makedirs(OUTPUT_PATH, exist_ok=True)
    date_str = datetime.now().strftime('%Y%m%d_%H%M%S')

    # CSV des données
    csv_path = f'{OUTPUT_PATH}/ventes_{date_str}.csv'
    df.to_csv(csv_path, index=False)

    # KPIs en JSON
    kpis = {
        'date'        : datetime.now().isoformat(),
        'ca_total'    : round(float(df['montant'].sum()), 2),
        'marge_totale': round(float(df['marge'].sum()), 2),
        'nb_ventes'   : len(df),
        'top_produit' : df.groupby('produit')['montant'].sum().idxmax(),
        'top_vendeur' : df.groupby('vendeur')['montant'].sum().idxmax(),
    }
    kpi_path = f'{OUTPUT_PATH}/kpis_{date_str}.json'
    with open(kpi_path, 'w') as f:
        json.dump(kpis, f, indent=2, ensure_ascii=False)

    print(f"[LOAD] CSV  → {csv_path}")
    print(f"[LOAD] KPIs → {kpi_path}")
    print(f"\n=== KPIs ===")
    for k, v in kpis.items():
        print(f"  {k:15} : {v}")


if __name__ == '__main__':
    print("=" * 40)
    print("  Pipeline ETL — Jour 1 Docker")
    print("=" * 40)

    df_raw   = extraire()
    df_clean = transformer(df_raw)
    charger(df_clean)

    print("\n✓ Pipeline terminé avec succès")
