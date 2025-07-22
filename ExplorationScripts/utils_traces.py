from utils_common import *

"Function that stores the communes name in a dictionary"
def nameCommune(path):
    # List of communes names dictionary
    communes_info = pd.read_excel(path, sheet_name=None,
                                  engine='openpyxl')  # DEPENDENCY: pip install xlrd pip install openpyxl

    # Value COMMUNES_4326 is the name of the xlsx page
    communes_names = list(communes_info['COMMUNES_4326']['name'].values)
    communes_codes = list(communes_info['COMMUNES_4326']['tunit_code'].values)

    dictionary_communeName = dict()

    for name, tcode in zip(communes_names, communes_codes):
        dictionary_communeName[tcode] = name

    # for k,v in dictionary_communeName.items():
    #    print(k,v)
    return dictionary_communeName

"Function that receives a dictionary of names to be added to the current data frame"
"If it is CLC, we mapp as well the nomenclature"
def add_communeName(path, dictionary_communeName, is_CLC=False):
    clc_nomenclature_one = {
        "11-Urban fabric": "1-Artificial surfaces",
        "12-Industrial, commercial and transport units": "1-Artificial surfaces",
        "13-Mine, dump and construction sites": "1-Artificial surfaces",
        "14-Artificial, non-agricultural vegetated areas": "1-Artificial surfaces",
        "21-Arable land": "2-Agricultural areas",
        "22-Permanent crops": "2-Agricultural areas",
        "23-Pastures": "2-Agricultural areas",
        "24-Heterogeneous agricultural areas": "2-Agricultural areas",
        "31-Forests": "3-Forest and semi natural areas",
        "32-Scrub and/or herbaceous vegetation associations": "3-Forest and semi natural areas",
        "33-Open spaces with little or no vegetation": "3-Forest and semi natural areas",
        "41-Inland wetlands": "4-Wetlands",
        "42-Coastal wetlands": "4-Wetlands",
        "51-Inland waters": "5-Water bodies",
        "52-Marine waters": "5-Water bodies",
    }
    df = pd.read_csv(path)
    # print("Number of rows: ", df.shape)

    associated_name = list()
    for commune_code in df.tunit_code.values:
        associated_name.append(dictionary_communeName[commune_code])
    df["commune_name"] = associated_name

    df_sorted = df.sort_values(by='date')
    "If it is CLC, we mapp as well the nomenclature"
    if is_CLC:
        nomen_column_two = list()
        nomen_column_one = list()
        clc_nomenclature_dict = obtain_clc_nomenclature()
        for value in df["var"].values:
            level_two_key = clc_nomenclature_dict[value]
            nomen_column_two.append(level_two_key)
            nomen_column_one.append(clc_nomenclature_one[level_two_key])
        df_sorted["clc_nomenclature"] = nomen_column_two  # Level 2
        df_sorted["clc_nomenclature_one"] = nomen_column_one  # Level 2

    return df_sorted

"Function that obtain the CLC nomenclature"
def obtain_clc_nomenclature():
    clc_nomenclature_dict = dict()

    # Because the nomenclature remains the same for each case study, we can take the one of Evian to retrieve the values
    path = "Spectral_Indices_Dataset/Evian/aux_data/clc-nomenclature-c_2.xls"
    communes_info = pd.read_excel(path, sheet_name="nomenclature_clc_niveau_2",
                                  )  # DEPENDENCY:  pip install xlrd

    for code, nomen in zip(communes_info.code_clc_niveau_2, communes_info.libelle_en):
        clc_nomenclature_dict["clc_" + str(code)] = str(code) + "-" + nomen
    return clc_nomenclature_dict


"Function that obtains --- One commune One index from a given data frame"
def select_commune_indice(df_name, commune, indice):
    df_name['date'] = pd.to_datetime(df_name['date'])
    df_name['dtdate'] = df_name['date'].dt.date # We create a new column of date format

    selected_commune_index = df_name[(df_name["var"] == indice)]
    selected_commune_index = selected_commune_index[(selected_commune_index["commune_name"] == commune)]
    selected_commune_index = selected_commune_index.sort_values(by='date')
    return selected_commune_index

"Function that retrieves (filters) commune per season"
def filter_by_season(df_commune_index, season):
    if season == "winter":
        value = 'DJF'
        df_selected_season = df_commune_index[(df_commune_index["season"] == value)]
    elif season == "spring":
        value = 'MAM'
        df_selected_season = df_commune_index[(df_commune_index["season"] == value)]
    elif season == "summer":
        value = 'JJA'
        df_selected_season = df_commune_index[(df_commune_index["season"] == value)]
    elif season == "autumn":
        value = 'SON'
        df_selected_season = df_commune_index[(df_commune_index["season"] == value)]

    df_selected_season = df_selected_season.sort_values(by='date')
    return df_selected_season



"This functions completes with NAN's values missing data (NaN values are requiered for BEAST to work accuratly)"
def check_missing_data(selected_commune_index, complete_true_dates, is_CLC=False):
    current_dates = selected_commune_index["dtdate"].values
    missing_dates = list(set(complete_true_dates) - set(current_dates))

    fild_name = selected_commune_index.commune_name.values[0]
    fild_tunit_code = selected_commune_index.tunit_code.values[0]
    # print("missing_dates: ",missing_dates, " filds: ",fild_name,fild_tunit_code)
    for missing_d in missing_dates:
        # For every missing date, we create a new row in the data frame with NAN values
        if is_CLC:
            new_row = {'id': np.nan, 'tunit_code': fild_tunit_code, 'date': missing_d, 'var': np.nan, 'ha': np.nan,
                       'pcage': np.nan}
        # For every missing date, we create a new row in the data frame with NAN values
        else:
            new_row = {'id': np.nan, 'tunit_code': fild_tunit_code, 'date': missing_d, 'season': np.nan, 'var': np.nan,
                       'qual': np.nan, 'mean': np.nan, 'std': np.nan,
                       'commune_name': fild_name, 'dtdate': missing_d}
        # Append the new row to the DataFrame
        selected_commune_index = selected_commune_index.append(new_row, ignore_index=True)

    selected_commune_index = selected_commune_index.sort_values(by='dtdate')
    column_ids = list(range(1, len(selected_commune_index) + 1))
    "We add a new row called id to the dataframe"
    selected_commune_index['id'] = column_ids
    return selected_commune_index


"This function obtaines the data quality from our TEI dataset"
def obtain_quality_ts(by_season, selected_period, selected_commune, selected_indice, selected_study_area):
    # print(by_season,selected_period,selected_commune,selected_indice,selected_study_area)
    if selected_study_area == 'GG':
        if selected_indice == 'st':
            df = df_name_GG_lst
        else:
            df = df_name_GG_lis
    elif selected_study_area == 'Evian':
        if selected_indice == 'st':
            df = df_name_Ev_lst
        else:
            df = df_name_Ev_lis

    elif selected_study_area == 'Fribourg':
        if selected_indice == 'st':
            df = df_name_Fr_lst
        else:
            df = df_name_Fr_lis

    if by_season:
        acronym = None
        if selected_period == "summer":
            acronym = "JJA"
        elif selected_period == "spring":
            acronym = "MAM"
        elif selected_period == "winter":
            acronym = "DJF"
        elif selected_period == "autumn":
            acronym = "SON"
        df_qual = df[
            (df["commune_name"] == selected_commune) & (df["var"] == selected_indice) & (df["season"] == acronym)]
    else:
        df_qual = df[(df["commune_name"] == selected_commune) & (df["var"] == selected_indice)]
        # print(df_qual.head(2))
    # print(df.columns)
    df_qual = df_qual.sort_values(by='date')
    df_qual_values = df_qual.qual.values
    return df_qual_values


"This function select as sub data frames the CLC classes for a given commune"
def clc_select_commune_for_pie(selected_study_area, selected_commune):
    sub_frames = list()
    if selected_study_area == 'GG':
        df = df_name_GG_clc
    elif selected_study_area == 'Evian':
        df = df_name_Ev_clc
    elif selected_study_area == 'Fribourg':
        df = df_name_Fr_clc

    for date in df.date.unique():
        df_clc_year = df[(df["commune_name"] == selected_commune) & (df["date"] == date)]
        sub_frames.append(df_clc_year)

    return sub_frames





################################################################################################
"Obtain commune name for each commune code as dicctionary"
path = "Spectral_Indices_Dataset/COMMUNES.xlsx"
dictionary_communeName = nameCommune(path) # e.g., 'FR74001': 'Abondance',

"Add to our LIS_seasonaly_noot.csv their names "
df_name_GG_lis = add_communeName("Spectral_Indices_Dataset/GrandGeneve/LIS/LIS_seasonaly_noot.csv", dictionary_communeName)
df_name_GG_lst = add_communeName("Spectral_Indices_Dataset/GrandGeneve/LST/LST_seasonaly_noot.csv", dictionary_communeName)
"Add to our LIS_seasonaly_noot.csv their names "
df_name_Ev_lis = add_communeName("Spectral_Indices_Dataset/Evian/LIS/LIS_seasonaly_noot.csv", dictionary_communeName)
df_name_Ev_lst = add_communeName("Spectral_Indices_Dataset/Evian/LST/LST_seasonaly_noot.csv", dictionary_communeName)
"Add to our LIS_seasonaly_noot.csv their names "
df_name_Fr_lis = add_communeName("Spectral_Indices_Dataset/Fribourg/LIS/LIS_seasonaly_noot.csv", dictionary_communeName)
df_name_Fr_lst = add_communeName("Spectral_Indices_Dataset/Fribourg/LST/LST_seasonaly_noot.csv", dictionary_communeName)

print("Finish loading the 3 LIS/LST cs from Traces data ...")

"Add to our CLC.csv their names "
"If it is CLC, we mapp as well the nomenclature"
df_name_GG_clc = add_communeName("Spectral_Indices_Dataset/GrandGeneve/CLC/CLC.csv", dictionary_communeName, True)
df_name_Ev_clc = add_communeName("Spectral_Indices_Dataset/Evian/CLC/CLC.csv", dictionary_communeName, True)
df_name_Fr_clc = add_communeName("Spectral_Indices_Dataset/Fribourg/CLC/CLC.csv", dictionary_communeName, True)

print("Finish loading the 3 CLC/ cs from Traces data ...")
df_name_Fr_clc.head()


"Path to the bounderies Case studies frames"
GG_path = "Bouderies_map/COMMUNES_GrandGeneve_4326.gpkg"
Fb_path = "Bouderies_map/COMMUNES_Fribourg_4326.gpkg"
Ev_path = "Bouderies_map/COMMUNES_Evian_4326.gpkg"
