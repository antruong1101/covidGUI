#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 13 19:45:22 2020

@author: antruong

backend

will produce JSON file and an SQL database file
"""

import requests
from bs4 import BeautifulSoup
import json
import sqlite3


class getJson():
    def __init__(self):
        
        try: 
            
            page = requests.get('https://www.worldometers.info/coronavirus/', timeout=3)
            page.raise_for_status()
            print(page.status_code)
            
        except requests.exceptions.HTTPError as e: 
            print('HTTP Error: ', e)
            
        except requests.exceptions.ConnectTimeout as e: 
            print('Error Connecting: ', e)
            
        except requests.exceptions.Timeout as e: 
            print('Timeout Error: ', e)
            
        except requests.exceptions.RequestException as e: 
            print('Request Exception: ', e)
            
        
        soup = BeautifulSoup(page.content, 'lxml')        

        bigData = []
        
        with open('data.json', 'w') as fh: 
            for elem in soup.select('table#main_table_countries_today tr'):
                                    
                line = elem.get_text().split('\n')
                
                uline = [None if item.isspace() or item == "" or item == 'N/A'else
                         item.replace(',', "").replace("+","") for item in line[2:-2]]
                
                
                if not uline[0]: 
                    uline.remove(uline[0])                
                
                if not uline[1]: 
                    uline.remove(uline[1])
                    
                if not uline[0]: #removes 721 line that is not displayed
                    continue
                                     
                bigData.append(uline)
            
            json.dump(bigData[1:-8], fh, indent=3)
        
        
        for data in bigData: 
            print(data)
               
        

class readJson():
    def __init__(self):
        
        self.colNames = (('TotalCases', 'INTEGER'), ('NewCases', 'INTEGER'),
                         ('TotalDeaths', 'INTEGER'), ('NewDeaths', 'INTEGER'), 
                         ('Total Recovered', 'INTEGER'), ('ActiveCases', 'INTEGER'), ('SeriousCases', 'INTEGER'),
                         ('TotalCasesPer1Mpop', 'INTEGER'), ('DeathsPer1Mpop', 'INTEGER'), 
                         ('TotalTest', 'INTEGER'), ('TestsPer1Mpop', 'INTEGER'), ('Population', 'INTEGER'))
        
        #print(len(self.colNames))
        
        conn = sqlite3.connect('covid.db')
        cur = conn.cursor()
        cur.execute('DROP TABLE IF EXISTS CovidDB')
        cur.execute('CREATE TABLE CovidDB(Country TEXT)')
        for col in self.colNames: #adds columns from self.colNames
            cur.execute('ALTER TABLE CovidDB ADD COLUMN "{}" "{}"'.format(col[0], col[1]))
            
        conn.commit()
            
        with open('data.json', 'r') as fh: 
            data = json.load(fh)
            for item in data: 
                cur.execute('''INSERT INTO CovidDB
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (item[:13]))
            
            conn.commit()            
            
        conn.close()
            
            
            
            
#getJson()
#readJson()

