import pandas as pd
from pandas import read_csv, read_excel
import glob
import os, json

limited_columns = ["snippet_title","views","likes","dislikes","comment_count","%_dislikes","time_up"]

# Lista os valores únicos da coluna 
def get_title_names(data):
    return sorted(list(pd.Series(data["snippet_title"]).unique()))

# Lista os labels da coluna 
def get_title_labels(data):
    return [x.title() for x in get_title_names(data)]


def get_title_id_map(data):
    return {x:i for (i,x) in enumerate(get_title_names(data))}


def get_title_ids(data):
    return sorted(get_title_id_map(data).values())

# Leitura do arquivo
def get_raw_data():
    data_file = "arquivos/df_youTube.csv"
    return pd.read_csv(data_file)



def get_title_data(snippet_title, pddata):
    return pddata[(pddata["snippet_title"] == snippet_title)]


def get_title_counts(pddata, lower_bound=0):
    counts = []
    filtered_title = []
    for title in get_all_snippet_title():
        data = get_title_data(title, pddata)
        count = len(data.index)
        if count >= lower_bound:
            filtered_title.append(title)
            counts.append(count)
    return (filtered_title, list(zip(filtered_title, counts)))


def get_limited_data(cols = None, lower_bound = None):
    if not cols:
        cols = limited_columns
    data = get_raw_data()[cols]
    if lower_bound:
        (title, _) = get_title_counts(data, lower_bound)
        data = data[data["snippet_title"].isin(title)]
    return data


def norm_column(col_name, pddata, inverted = False):
    pddata[col_name] -= pddata[col_name].min()
    pddata[col_name] /= pddata[col_name].max()
    if inverted:
        pddata[col_name] = 1 - pddata[col_name]


def norm_columns(col_names, pddata):
    for col in col_names:
        norm_column(col, pddata)


def invert_norm_columns(col_names, pddata):
    for col in col_names:
        norm_column(col, pddata, inverted = True)


def get_all_snippet_title():
     return pd.Series(get_raw_data()["snippet_title"]).unique()


def get_numeric_data(pddata):
    return pddata.replace({"title": get_title_id_map(pddata)})

# Gravação do arquivo ml
def save_raw_data_ml():
    data_file = "ml_dados.csv"
    return dados2.to_csv(data_file)


# Leitura dos arquivos *.csv do diretório 
full_df= pd.DataFrame()
def get_concat_save_data():
    all_files = glob.glob("arquivos/*.csv")
    df_list = []
    global full_df
    
    for filename in sorted(all_files):
        df_list.append(pd.read_csv(filename, encoding = "latin-1", delimiter=","))
        full_df = pd.concat(df_list)
    
    data_file = "Dados/merged_files.csv"    
    return full_df.to_csv(data_file)