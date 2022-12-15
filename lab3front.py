#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 13 19:45:22 2020

@author: antruong

frontend

GUI
will read from the SQL database to display data to the user
"""


import tkinter as tk
import matplotlib
matplotlib.use('Agg') #removes matplot interactive window
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 
import matplotlib.pyplot as plt
import sqlite3
import numpy as np

class MainWin(tk.Tk):
    
    def __init__(self):
        super().__init__()
        
        self.title('Covid - 19 Cases')
        
        self.conn = sqlite3.connect('covid.db')
        self.cur = self.conn.cursor()
        
        world = [elem for elem in self.cur.execute('''SELECT TotalCasesPer1Mpop, DeathsPer1Mpop
                                              FROM CovidDB WHERE Country = ?''', ('World',))]
        
        self._countries = [elem[0] for elem in self.cur.execute('SELECT Country FROM CovidDB WHERE Population NOT NULL ORDER BY Country')]
        
        self._newCases = [elem for elem in self.cur.execute('''SELECT Country, NewCases, NewDeaths FROM CovidDB WHERE Population NOT NULL
                                                            AND NewCases NOT NULL AND NewDeaths NOT NULL ORDER BY NewCases DESC''')]
                
        self._top20 = [elem for elem in self.cur.execute('''SELECT Country, TotalCasesPer1Mpop, DeathsPer1Mpop, TestsPer1Mpop FROM CovidDB 
                                WHERE Population NOT NULL ORDER BY TotalCases DESC LIMIT 20''')]
    
        #print(world)
        #print(self._newCases)
        #print(self._top20)
        
        worldCountries = 'Worldwide: ' + str(len(self._countries)) + ' countries'
        wCase = 'Worldwide: ' + str(world[0][0]) + ' cases per 1M people'
        dCase = 'Worldwide: ' + str(world[0][1]) + ' deaths per 1M people'        
        
        tk.Label(self, text=worldCountries).grid(row=0, column=0, sticky='w') # total num of countries in database
        tk.Label(self, text=wCase).grid(row=1, column=0, sticky='w') # num of Covid-19 cases per million people worldwide
        tk.Label(self, text=dCase).grid(row=2, column=0, sticky='w') # num of deaths per million people worldwide
        
        buttonFrame = tk.Frame(self)
        buttonFrame.grid(row=3, column=0)
        tk.Button(buttonFrame, text='New Cases', command=self.displayNew, fg='blue').grid(row=0, column=0) # number of new cases and new deaths for that day
        tk.Button(buttonFrame, text='Top 20 Cases', command=self.displayTop, fg='blue').grid(row=0, column=1) # the 20 countries with the highest number of cases 
        tk.Button(buttonFrame, text='Compare Countries', command=self.compareCountry, fg='blue').grid(row=0, column=2) # a plot of the number of cases for the countries 
                                                  
        self.protocol('WM_DELETE_WINDOW', self.closeConn)
        
    def closeConn(self):
        '''
        closes connection and destroys window when 'x' button is clicked on
        '''
        self.conn.close()
        self.destroy()
        self.quit()       
     
        
    def displayNew(self):
        '''
        displays top 10 countries ordered by new cases
        '''
        COLUMNS = (('Country', 17), ('NewCases', 7), ('NewDeaths', 7))
        DisplayWin(self, 'New Cases', COLUMNS, self._newCases, 10, scroll=1)
    
        
    def displayTop(self):
        '''
        displays top 20 countries ordered by total cases per 1M population
        '''
        COLUMNS = (('Country', 17), ('TotalCases', 7), ('Deaths', 7), ('Tests', 7))
        DisplayWin(self, 'Top 20: Per 1M Population', COLUMNS, self._top20, 20)
    
    
    def compareCountry(self): 
        dwin = DialogWin(self)
        
        self.wait_window(dwin)
        
        countries = dwin.getData()
        
        caseData = []
        
        if countries:
            for country in countries: 
                for elem in self.cur.execute('SELECT TotalCasesPer1Mpop FROM CovidDB WHERE Country = ?', (country, )): 
                    caseData.append(elem[0])
                
            PlotWin(self, np.array(countries), np.array(caseData))        
        


class MultiListBox(tk.Frame): 
    '''
    MuliListBox Widget
    '''   
    
    def __init__(self, main, cols, colsize, scroll=None): 
        
        super().__init__(main)
        
        
        self.lbContain = []
        
        for e, column in enumerate(cols, 0):
            
            tk.Label(self, text=column[0]).grid(row=0, column=e, sticky='w')
            lb = tk.Listbox(self, width=column[1], height=colsize)
            
            lb.grid(row=1, column=e, sticky='e')          
            self.lbContain.append(lb)
        
        if scroll:
            self.sb = tk.Scrollbar(self, command=self._yview, orient=tk.VERTICAL)
            self.sb.grid(row=1, column=len(cols), sticky='ns')

  
    def _yview(self, *args): 
        '''
        Links scrollbar to all listboxes
        '''
        
        for box in self.lbContain:
            box.yview(*args)
            box.config(yscrollcommand = self.sb.set)
            
    
    def insert(self, index, *elements): 
        '''
        inserts data to each listbox
        '''
        
        for e, box in enumerate(self.lbContain): 
            for data in elements: 
                box.insert(tk.END, data[e])
        
        

class DisplayWin(tk.Toplevel):
    '''
    displays multiple listbox widgets
    '''  
    
    def __init__(self, main, tableName, cols, query, colsize, scroll=None):
        super().__init__(main)
        
        self.title(tableName)
        
        multListBox = MultiListBox(self, cols, colsize, scroll)
        multListBox.insert(tk.END, *query)
        multListBox.grid()
        
        if scroll: 
            highest = 'Highest: ' + str(query[0][1]) + ' new cases in ' + str(query[0][0])
            labelFrame = tk.Frame(self)
            labelFrame.grid(row=3, column=0)
            tk.Label(labelFrame, text=highest).grid(row=0, column=0)            
        

        
class DialogWin(tk.Toplevel):
    '''
    Allows user to choose countries to compare(Total Cases per 1M pop)
    '''
    
    def __init__(self, main):
        super().__init__(main)
        
        self.mainWin = main
        
        self.countries = main._countries
        
        self.countryChosen = []
        
        self.grab_set()
        self.focus_set()
        
        self.title('Choose Countries')
        scroll = tk.Scrollbar(self)
        scroll.grid(row=0, column=1, sticky='ns')
        
                        
        #creates visible list of colleges for user
        self.Countries = tk.Listbox(self, selectmode='multiple', height=10, yscrollcommand=scroll.set)
        
        self.Countries.insert(tk.END, *self.countries)
        self.Countries.grid(row=0, column=0)
        
        self.grab_set()
        self.focus_set()
        
        plotButton = tk.Button(self, text='OK', command=self.sendData).grid(row=1, column=0)
        
        
    def sendData(self): 
        '''
        gets curselection data
        '''
        
        chosen = self.Countries.curselection()        
        self.destroy()
               
        self.countryChosen = [self.countries[index] for index in chosen]

       
    def getData(self): 
        '''
        returns curselection data as a list
        '''

        if len(self.countryChosen) != 0:
            return self.countryChosen
        else: return
        

        
class PlotWin(tk.Toplevel):
    '''
    Plots Number of Cases per 1M People sent from Main Window
    '''
    
    def __init__(self, main, countries, cases):
        super().__init__(main)
        
        fig = plt.figure(figsize=(4, 5))
        
        plt.title('Number of Cases for Chosen Countries')        
        plt.bar(countries, cases, align='center')
        plt.ylabel('Number of Cases per 1M people')
        plt.xticks(rotation=45)
        plt.tight_layout()  
        
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.get_tk_widget().grid()
        canvas.draw()
        


UI = MainWin()
UI.mainloop()