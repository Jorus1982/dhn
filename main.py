# import knižníc
import pandas as pd
import geopandas as gpd
import matplotlib as plt
import mapclassify as mc
import folium as fl

# slovník pre údaje v tabuľke "dhn.xlsx"
new_names = {
'OKRES': 'Okres', 
'IDN3': 'IDN3', 
'OKRES_SKRATKA': 'Skratka okresu',
'DHN_SPOLU': 'Počet poberateľov DHN',
'DHN_SPOLU_P': 'Podiel poberateľov DHN v rámci SR (%)',
'DHN_UOZ': 'z toho: počet poberateľov, kt. sú UoZ',
'DHN_AV': 'z toho: počet poberateľov, kt. môžu pracovať',
'DHN_AV_UOZ': 'z toho: počet poberateľov, kt. môžu pracovať a sú UoZ',
'DHN_AV_ACT': 'z toho: počet poberateľov, kt. môžu pracovať a poberajú aktivačný príspevok',
'DHN_UOZ_P': 'z toho v rámci okresu: podiel UoZ (%)',
'DHN_AV_P': 'z toho v rámci okresu: podiel poberateľov, kt. môžu pracovať (%)',
'DHN_AV_UOZ_P': 'z toho v rámci okresu: podiel poberateľov, kt. môžu pracovať a sú UoZ (%)',
'DHN_AV_ACT_P': 'z toho v rámci okresu: podiel poberateľov, kt. môžu pracovať a poberajú aktivačný príspevok (%)'
}

# údaje o poberateľoch dávky v hmotnej núdzi
dhn = pd.read_excel('data\dhn.xlsx')

# údaje s oddelovačom tisícov a bez desatinných miest
dhn['DHN_SPOLU'] = dhn['DHN_SPOLU'].astype(int).apply(lambda x: f"{x:,}".replace(',', ' '))
dhn['DHN_UOZ'] = dhn['DHN_UOZ'].astype(int).apply(lambda x: f"{x:,}".replace(',', ' '))
dhn['DHN_AV'] = dhn['DHN_AV'].astype(int).apply(lambda x: f"{x:,}".replace(',', ' '))
dhn['DHN_AV_UOZ'] = dhn['DHN_AV_UOZ'].astype(int).apply(lambda x: f"{x:,}".replace(',', ' '))
dhn['DHN_AV_ACT'] = dhn['DHN_AV_ACT'].astype(int).apply(lambda x: f"{x:,}".replace(',', ' '))

# údaje na dve desatinné miesta
dhn[['DHN_SPOLU_P', 'DHN_UOZ_P', 'DHN_AV_P', 'DHN_AV_UOZ_P','DHN_AV_ACT_P']] = dhn[['DHN_SPOLU_P', 'DHN_UOZ_P', 'DHN_AV_P', 'DHN_AV_UOZ_P','DHN_AV_ACT_P']].round(2)

# použitie názvov zo slovníka
dhn = dhn.rename(columns=new_names)

# podkladová mapa okresov SR
mapa = gpd.read_file('geodata\sk_dist.geojson')

# spojenie mapy a tabuľky s dátami
mapa_data = pd.merge(mapa, dhn, on='IDN3', how='left')

# Všetky mapy v jednej, výber pomocou "click"
m = mapa_data.explore(
    name="Poberatelia DHN",
    column='Podiel poberateľov DHN v rámci SR (%)',
    scheme="Quantiles",
    k=4,
    legend=True,
    cmap="OrRd",
    tooltip=(['Okres',
              'Počet poberateľov DHN',
              'Podiel poberateľov DHN v rámci SR (%)',
              'z toho: počet poberateľov, kt. sú UoZ',
              'z toho: počet poberateľov, kt. môžu pracovať',
              'z toho: počet poberateľov, kt. môžu pracovať a sú UoZ',
              'z toho: počet poberateľov, kt. môžu pracovať a poberajú aktivačný príspevok']),
    style_kwds=dict
            (
            color="Black"
            ),
    legend_kwds=dict
            (
            caption='Poberatelia dávky v hmotnej núdzi',
            )
  )           

mapa_data.explore(
    m=m,
    name="z toho v rámci okresu: UoZ",
    column='z toho v rámci okresu: podiel UoZ (%)',
    scheme="Quantiles",
    k=4,
    legend=True,
    cmap="OrRd",
    tooltip=(['Okres',
              'Počet poberateľov DHN', 
              'z toho: počet poberateľov, kt. sú UoZ',
              'z toho v rámci okresu: podiel UoZ (%)']),
    style_kwds=dict
            (
            color="Black"
            ),
    legend_kwds=dict
            (
            caption='Poberatelia dávky v hmotnej núdzi, kt. sú UoZ'
            )
  )

mapa_data.explore(
    m=m,
    name="z toho v rámci okresu: poberatelia, kt. môžu pracovať",
    column='z toho v rámci okresu: podiel poberateľov, kt. môžu pracovať (%)',
    scheme="Quantiles",
    k=4,
    legend=True,
    cmap="OrRd",
    tooltip=(['Okres',
              'Počet poberateľov DHN', 
              'z toho: počet poberateľov, kt. môžu pracovať',
              'z toho v rámci okresu: podiel poberateľov, kt. môžu pracovať (%)']),
    style_kwds=dict
            (
            color="Black"
            ),
    legend_kwds=dict
            (
            caption='Poberatelia dávky v hmotnej núdzi, kt. môžu pracovať'
            )
  )                

mapa_data.explore(
    m=m,
    name="z toho v rámci okresu: poberatelia, kt. môžu pracovať a sú UoZ",
    column='z toho v rámci okresu: podiel poberateľov, kt. môžu pracovať a sú UoZ (%)',
    scheme="Quantiles",
    k=4,
    legend=True,
    cmap="OrRd",
    tooltip=(['Okres',
              'Počet poberateľov DHN', 
              'z toho: počet poberateľov, kt. môžu pracovať a sú UoZ',
              'z toho v rámci okresu: podiel poberateľov, kt. môžu pracovať a sú UoZ (%)']),
    style_kwds=dict
            (
            color="Black"
            ),
    legend_kwds=dict
            (
            caption='Poberatelia dávky v hmotnej núdzi, kt. môžu pracovať a sú UoZ'
            )
  )            

mapa_data.explore(
    m=m,
    name="z toho v rámci okresu: poberatelia, kt. môžu pracovať a poberajú aktivačný príspevok",
    column='z toho v rámci okresu: podiel poberateľov, kt. môžu pracovať a poberajú aktivačný príspevok (%)',
    scheme="Quantiles",
    k=4,
    legend=True,
    cmap="OrRd",
    tooltip=(['Okres',
              'Počet poberateľov DHN', 
              'z toho: počet poberateľov, kt. môžu pracovať a poberajú aktivačný príspevok',
              'z toho v rámci okresu: podiel poberateľov, kt. môžu pracovať a poberajú aktivačný príspevok (%)']),
    style_kwds=dict
            (
            color="Black"
            ),
    legend_kwds=dict
            (
            caption='Poberatelia dávky v hmotnej núdzi, kt. môžu pracovať a poberajú aktivačný príspevok (%)'
            )
       
  )    

        
# use folium to add alternative tiles

""" fl.TileLayer("CartoDB positron", show=False).add_to(m)  
"""

# use folium to add layer control
fl.LayerControl().add_to(m)  

m  # show map