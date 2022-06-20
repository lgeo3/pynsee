import os

from pynsee.download._download_store_file import _download_store_file
from pynsee.download._load_data_from_schema import _load_data_from_schema

def download_file(id, variables=None, update=False):

    """
    User level function to download files from insee.fr

    Args:
        id (str): file id, check get_file_list to have a full list of available files
        update (bool, optional): Trigger an update, otherwise locally saved data is used. Defaults to False.

    Returns:
        Returns the request dataframe as a pandas object

    """
    
    try:

        dwn = _download_store_file(id, update=update)
        df = _load_data_from_schema(dwn, variables=variables)      

        return df
    except:
        raise ValueError("Download failed")
        