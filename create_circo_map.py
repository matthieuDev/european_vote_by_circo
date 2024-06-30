import geopandas
import matplotlib.pyplot as plt
from values import party_colors

from generate_data_frame import generate_normed_df_votes_by_allignement
from load_files import load_code_circo2name

def create_main_circo() :
    data_folder = 'imported_data/map_circo/'
    map_file = data_folder + 'france-circonscriptions-legislatives-2012.shp'

    gdf = geopandas.read_file(map_file)
    circo_name2code = {name: code for code, name in load_code_circo2name().items()}

    df_votes_by_allignement = generate_normed_df_votes_by_allignement()

    circo2color = {}
    for circo, row in df_votes_by_allignement.iterrows():
        circo2color[circo_name2code[circo]] = party_colors[row.argmax()]

    gdf['circo_color'] = gdf.apply(
        lambda line: circo2color.get(f'{line["code_dpt"]}{int(line["num_circ"]):02d}'),
        axis=1,
    )
    gdf = gdf[~gdf['circo_color'].isna()]
    return gdf

if __name__ == '__main__' :
    gdf=create_main_circo()
    plt.figure()
    gdf.plot("ID", legend=False, color=gdf['circo_color'])
    plt.savefig('data/political_leaning_repartition_map.png')
