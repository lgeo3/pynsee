# -*- coding: utf-8 -*-
"""
Created on Fri Feb  5 11:51:33 2021

@author: XLAPDO
"""
#proxy
proxy_file_folder = 'C:/Users/XLAPDO/Desktop/insee_pylib'
proxy_file = proxy_file_folder + '/proxy.py'
try:
    f = open(proxy_file)
    exec(f.read())
    print("Proxy file executed")
except IOError:
    print("Proxy file not accessible")

from unittest import TestCase
import pandas as pd

import insee_macrodata as imac

class TestFunction(TestCase):
    
    def test_get_column_title(self):
        data = imac.get_column_title()
        self.assertTrue(isinstance(data, pd.DataFrame))
    
    def test_get_idbank_list(self):
        data = imac.get_idbank_list('CLIMAT-AFFAIRES')
        self.assertTrue(isinstance(data, pd.DataFrame))
        
    def test_get_insee_idbank(self):
        data = imac.get_insee_idbank("001769682", "001769683")
        self.assertTrue(isinstance(data, pd.DataFrame))
    
    def test_get_insee_1(self):
        data = imac._get_insee("https://bdm.insee.fr/series/sdmx/data/SERIES_BDM/001769682")
        self.assertTrue(isinstance(data, pd.DataFrame))
        
    def test_get_insee_2(self):
        data = imac._get_insee("https://bdm.insee.fr/series/sdmx/data/BALANCE-PAIEMENTS")
        self.assertTrue(isinstance(data, pd.DataFrame))
        
    def test_get_insee_dataset_1(self):
        data = imac.get_insee_dataset('BALANCE-PAIEMENTS')
        self.assertTrue(isinstance(data, pd.DataFrame))
    
    def test_get_insee_dataset_2(self):
        data = imac.get_insee_dataset("CNA-2014-CPEB",
                              filter = "A.CNA_CPEB.A38-CB.VAL.D39.VALEUR_ABSOLUE.FE.EUROS_COURANTS.BRUT",
                              lastNObservations = 1)
        self.assertTrue(isinstance(data, pd.DataFrame))
        
    def test_get_insee_dataset_3(self):
        data1 = imac.get_insee_dataset("IPC-2015", filter = "M......ENSEMBLE...CVS.2015")
        data2 = imac.get_insee_dataset("IPC-2015", filter = "M......ENSEMBLE...CVS.2015",
                   includeHistory = True,
                   updatedAfter = "2017-07-11T08:45:00")        
        self.assertTrue(len(data1.index) < len(data2.index))
        
    def test_split_title(self):
        data = imac.get_insee_idbank("001769682", "001769683")   
        df = imac.split_title(data)
        self.assertTrue(isinstance(df, pd.DataFrame))
        