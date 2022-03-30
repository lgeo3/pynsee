# -*- coding: utf-8 -*-
# Copyright : INSEE, 2021

import pandas as pd
from functools import lru_cache

from pynsee.utils._request_insee import _request_insee
from pynsee.sirene._make_dataframe_from_dict import _make_dataframe_from_dict
from pynsee.sirene.SireneDataframe import SireneDataframe

@lru_cache(maxsize=None)
def _warning_get_data():
    print("\n!!! This function may return personal data, please check and\n comply with the legal framework relating to personal data protection !!!")


def get_data(id, kind='siret'):
    """Get data about one or several companies from siren or siret identifiers

    Notes:
        This function may return personal data, please check and comply with the legal framework relating to personal data protection

    Examples:
        >>> from pynsee.sirene import get_data
        >>> df = get_data("552081317", kind = 'siren')
        >>> df = get_data(['32227167700021', '26930124800077'], kind='siret')
    """

    if type(id) == str:
        id = [id]
        
    if type(id) != list:
        raise ValueError('!!! id should be a list or a str !!!')
        
    if kind == 'siren':
        main_key = 'uniteLegale'
    elif kind == 'siret':
        main_key = 'etablissement'
    else:
        raise ValueError('!!! kind should be among : siren, siret !!!')

    INSEE_api_sirene = "https://api.insee.fr/entreprises/sirene/V3/" + kind

    list_data = []

    for i in range(len(id)):
        link = INSEE_api_sirene + '/' + str(id[i])
        request = _request_insee(
            api_url=link, file_format='application/json;charset=utf-8')
        try:
            data_request = request.json()

            try:
                data = data_request[main_key]
            except:
                main_key_list = [key for key in list(
                    data_request.keys()) if key != "header"]
                main_key = main_key_list[0]
                data = data_request[main_key]

            data_final = _make_dataframe_from_dict(data)
        except:
            pass
        else:
            list_data.append(data_final)

    data_final = pd.concat(list_data).reset_index(drop=True)

    _warning_get_data()

    SireneDF = SireneDataframe(data_final)

    return(SireneDF)
