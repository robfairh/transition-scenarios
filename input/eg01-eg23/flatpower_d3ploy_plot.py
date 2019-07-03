"""
This script creates the .csv file and the .png file for power
asociated to a scenario run with multiple calculations methods
"""
import json
import re
import subprocess
import os
import sqlite3 as lite
import copy
import glob
import sys
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import d3ploy.tester as tester
import d3ploy.plotter as plotter
import collections

def supply_demand_dict_nondriving(sqlite, commod, demand_driven):
    """ Puts supply, demand, calculated demand and
    calculated supply into a nice dictionary format
    if given the sql file and commodity name
    for a non-driving commodity
    Parameters
    ----------
    sqlite: sql file to analyze
    commod: string of commod name
    demand_driven: Boolean. If true, the commodity is demand driven,
    if false, the commodity is supply driven
    Returns
    -------
    returns 4 dicts: dictionaries of supply, demand, calculated
    demand and calculated supply
    """
    cur = get_cursor(sqlite)
    tables = {}
    tables[0] = "timeseriessupply" + commod
    tables[1] = "timeseriesdemand" + commod

    fuel_demand = cur.execute(
        "select time, sum(value) from " +
        tables[1] +
        " group by time").fetchall()
    fuel_supply = cur.execute(
        "select time, sum(value) from " +
        tables[0] +
        " group by time").fetchall()
    
    dict_demand = {}
    dict_supply = {}

    for x in range(0, len(fuel_supply)):
        dict_supply[fuel_supply[x][0]] = fuel_supply[x][1]

    t = np.fromiter(dict_supply.keys(), dtype=float)
    for x in range(0, len(t)):
        dict_demand[t[x]] = 0
    for x in range(0, len(fuel_demand)):
        dict_demand[fuel_demand[x][0]] = fuel_demand[x][1]

    # give dict supply zeros at timesteps 1 and 2
    for key in dict_demand.keys():
        if key not in dict_supply:
            dict_supply[key] = 0.0

    all_dict = {}
    all_dict['dict_demand'] = dict_demand
    all_dict['dict_supply'] = dict_supply
    return all_dict

def plot_several(name, all_dict, commod, calc_methods, demand_eq):
    dict_demand = {}
    dict_supply = {}

    for calc_method in calc_methods:
        dict_demand[calc_method] = all_dict[calc_method]['dict_demand']
        dict_supply[calc_method] = all_dict[calc_method]['dict_supply']
    
    fig, ax = plt.subplots(figsize=(15, 7))
    
    #ax.yaxis.set_ticks(np.arange(5.e4, 13.e4, 5.e3))
    #plt.ylim(bottom = 5.8e4, top = 12.e4)

    ax.plot(*zip(*sorted(dict_demand[calc_method].items())), '-', color='red',
            label='Demand')
    
    for calc_method in calc_methods:
        ax.plot(*zip(*sorted(dict_supply[calc_method].items())), 'x',
                label=calc_method + ' Supply') 

    ax.set_xlabel('Time (month timestep)', fontsize=14)
    if commod.lower() == 'power':
        ax.set_ylabel('Power (MW)', fontsize=14)
    else:
        ax.set_ylabel('Mass (Kg)', fontsize=14)

    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels, fontsize=11, loc='upper center',
              bbox_to_anchor=(1.1, 1.0), fancybox=True)
    
    plt.savefig(name, dpi=300, bbox_inches='tight')
    plt.close()

# Delete previously generated files
direc = os.listdir('./')
hit_list = glob.glob('*.png') + glob.glob('*.csv')
for file in hit_list:
    os.remove(file)
ENV = dict(os.environ)
ENV['PYTHONPATH'] = ".:" + ENV.get('PYTHONPATH', '')

#calc_methods = ["ma", "arma", "arch", "poly", "exp_smoothing", "holt_winters", "fft", "sw_seasonal"]
calc_methods = ["ma", "arma", "arch", "poly", "exp_smoothing", "holt_winters", "fft"]

demand_eq = "60000"

metric_dict = {}
all_dict = {}

front_commods = ['sourceout', 'enrichmentout']
back_commods = ['lwrpu', 'frpu']

#back_commods = ['lwrstorageout', 'frstorageout', 'lwrout', 'frout',
#                'lwrreprocessingwaste', 'frreprocessingwaste', 'frpu',
#                'lwrpu']

#name = 'eg01-eg23-flatpower-d3ploy'
#name = 'eg01-eg23-flatpower-d3ploy-installed'
#name = 'eg01-eg23-flatpower-d3ploy-installed-buffer'

add = sys.argv[1]
name = 'eg01-eg23-flatpower-d3ploy' + add
#add = '-installed-buffer6000'

for calc_method in calc_methods:

    output_file = name + '-' + calc_method +'.sqlite'
 
    all_dict['power'] = tester.supply_demand_dict_driving(
    output_file, demand_eq, 'power')

    metric_dict = tester.metrics(
        all_dict['power'], metric_dict, calc_method, 'power', True)

    for commod in front_commods:
        all_dict[commod] = tester.supply_demand_dict_nondriving(output_file,
                                                                commod, True)
        metric_dict = tester.metrics(
            all_dict[commod], metric_dict, calc_method, commod, True)

    commod = 'mixerout'
    all_dict[commod] = tester.supply_demand_dict_nond3ploy(output_file,
                                                           commod)

    metric_dict = tester.metrics(
        all_dict[commod], metric_dict, calc_method, commod, True)

    for commod in back_commods:
        all_dict[commod] = tester.supply_demand_dict_nondriving(output_file,
                                                                commod, False)
        metric_dict = tester.metrics(
            all_dict[commod], metric_dict, calc_method, commod, False)
  
    df = pd.DataFrame(metric_dict)
    df.to_csv('asave/' + name + '.csv')

calc_methods1 = ["ma", "arma", "arch"]
calc_methods2 = ["poly", "exp_smoothing", "holt_winters", "fft"]
#calc_methods3 = ["sw_seasonal"]

for calc_method in calc_methods1:

    output_file = name +'-'+ calc_method +'.sqlite' 
    all_dict[calc_method] = tester.supply_demand_dict_driving(output_file, demand_eq, 'power')

plot_several('asave/23-power'+ add +'1', all_dict, 'power', calc_methods1, demand_eq)

for calc_method in calc_methods2:

    output_file = name +'-'+ calc_method +'.sqlite' 
    all_dict[calc_method] = tester.supply_demand_dict_driving(output_file, demand_eq, 'power')

plot_several('asave/23-power'+ add +'2', all_dict, 'power', calc_methods2, demand_eq)
