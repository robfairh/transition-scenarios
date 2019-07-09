"""
Running this script generates .xml files and runs them producing the .sqlite
files for all the prediction methods.

The user can choose a demand equation (demand_eq).
There is no buffer defined and the installed capacity feature is used.
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

direc = os.listdir('./')

# Delete previously generated files
#hit_list = glob.glob('*.png') + glob.glob('*.csv') + glob.glob('*.sqlite')
#for file in hit_list:
#    os.remove(file)

ENV = dict(os.environ)
ENV['PYTHONPATH'] = ".:" + ENV.get('PYTHONPATH', '')

calc_methods = ["ma", "arma", "arch", "poly", "exp_smoothing", "holt_winters", "fft", "sw_seasonal"]

demand_eq = "60000"

control = """
<control>
    <duration>1440</duration>
    <startmonth>1</startmonth>
    <startyear>2000</startyear>
    <decay>lazy</decay>
</control>

<archetypes>
        <spec>
            <lib>cycamore</lib>
            <name>Source</name>
        </spec>
        <spec>
            <lib>cycamore</lib>
            <name>Enrichment</name>
        </spec>
        <spec>
            <lib>cycamore</lib>
            <name>Reactor</name>
        </spec>
        <spec>
            <lib>cycamore</lib>
            <name>Storage</name>
        </spec>
        <spec>
            <lib>cycamore</lib>
            <name>Separations</name>
        </spec>
        <spec>
            <lib>cycamore</lib>
            <name>Mixer</name>
        </spec>
        <spec>
            <lib>cycamore</lib>
            <name>Sink</name>
        </spec>
        <spec>
            <lib>agents</lib>
            <name>NullRegion</name>
        </spec>
        <spec>
            <lib>agents</lib>
            <name>NullInst</name>
        </spec>
        <spec>
            <lib>cycamore</lib>
            <name>DeployInst</name>
        </spec>
        <spec>
            <lib>d3ploy.demand_driven_deployment_inst</lib>
            <name>DemandDrivenDeploymentInst</name>
        </spec>
        <spec>
            <lib>d3ploy.supply_driven_deployment_inst</lib>
            <name>SupplyDrivenDeploymentInst</name>
        </spec>
</archetypes>

<facility>
    <name>source</name>
    <config>
        <Source>
            <outcommod>sourceout</outcommod>
            <outrecipe>sourceoutrecipe</outrecipe>
            <throughput>1e9</throughput>
        </Source>
    </config>
</facility>

<facility>
    <name>enrichment</name>
    <config>
        <Enrichment>
            <feed_commod>sourceout</feed_commod>
            <feed_recipe>sourceoutrecipe</feed_recipe>
            <product_commod>enrichmentout</product_commod>
            <tails_assay>0.0025</tails_assay>
            <tails_commod>enrichmentwaste</tails_commod>
            <swu_capacity>1e100</swu_capacity>
            <initial_feed>5e7</initial_feed>
            <max_feed_inventory>1e8</max_feed_inventory>
        </Enrichment>
    </config>
</facility>

<facility>
    <name>lwr</name>
    <lifetime>960</lifetime>
    <config>
        <Reactor>
            <fuel_inrecipes>
                <val>lwrinrecipe</val>
            </fuel_inrecipes>
            <fuel_outrecipes>
                <val>lwroutrecipe</val>
            </fuel_outrecipes>
            <fuel_incommods>
                <val>enrichmentout</val>
            </fuel_incommods>
            <fuel_outcommods>
                <val>lwrout</val>
            </fuel_outcommods>
            <cycle_time>18</cycle_time>
            <refuel_time>0</refuel_time>
            <assem_size>29863.3</assem_size>
            <n_assem_core>3</n_assem_core>
            <n_assem_batch>1</n_assem_batch>
            <power_cap>1000</power_cap>
        </Reactor>
    </config>
</facility>

<facility>
    <name>lwr1</name>
    <lifetime>960</lifetime>
    <config>
        <Reactor>
            <fuel_inrecipes>
                <val>lwrinrecipe</val>
            </fuel_inrecipes>
            <fuel_outrecipes>
                <val>lwroutrecipe</val>
            </fuel_outrecipes>
            <fuel_incommods>
                <val>enrichmentout</val>
            </fuel_incommods>
            <fuel_outcommods>
                <val>lwrout</val>
            </fuel_outcommods>
            <cycle_time>18</cycle_time>
            <refuel_time>0</refuel_time>
            <assem_size>29863.3</assem_size>
            <n_assem_core>3</n_assem_core>
            <n_assem_batch>1</n_assem_batch>
            <power_cap>1000</power_cap>
        </Reactor>
    </config>
</facility>

<facility>
    <name>lwr2</name>
    <lifetime>980</lifetime>
    <config>
        <Reactor>
            <fuel_inrecipes>
                <val>lwrinrecipe</val>
            </fuel_inrecipes>
            <fuel_outrecipes>
                <val>lwroutrecipe</val>
            </fuel_outrecipes>
            <fuel_incommods>
                <val>enrichmentout</val>
            </fuel_incommods>
            <fuel_outcommods>
                <val>lwrout</val>
            </fuel_outcommods>
            <cycle_time>18</cycle_time>
            <refuel_time>0</refuel_time>
            <assem_size>29863.3</assem_size>
            <n_assem_core>3</n_assem_core>
            <n_assem_batch>1</n_assem_batch>
            <power_cap>1000</power_cap>
        </Reactor>
    </config>
</facility>

<facility>
    <name>lwr3</name>
    <lifetime>1000</lifetime>
    <config>
        <Reactor>
            <fuel_inrecipes>
                <val>lwrinrecipe</val>
            </fuel_inrecipes>
            <fuel_outrecipes>
                <val>lwroutrecipe</val>
            </fuel_outrecipes>
            <fuel_incommods>
                <val>enrichmentout</val>
            </fuel_incommods>
            <fuel_outcommods>
                <val>lwrout</val>
            </fuel_outcommods>
            <cycle_time>18</cycle_time>
            <refuel_time>0</refuel_time>
            <assem_size>29863.3</assem_size>
            <n_assem_core>3</n_assem_core>
            <n_assem_batch>1</n_assem_batch>
            <power_cap>1000</power_cap>
        </Reactor>
    </config>
</facility>

<facility>
    <name>lwr4</name>
    <lifetime>1020</lifetime>
    <config>
        <Reactor>
            <fuel_inrecipes>
                <val>lwrinrecipe</val>
            </fuel_inrecipes>
            <fuel_outrecipes>
                <val>lwroutrecipe</val>
            </fuel_outrecipes>
            <fuel_incommods>
                <val>enrichmentout</val>
            </fuel_incommods>
            <fuel_outcommods>
                <val>lwrout</val>
            </fuel_outcommods>
            <cycle_time>18</cycle_time>
            <refuel_time>0</refuel_time>
            <assem_size>29863.3</assem_size>
            <n_assem_core>3</n_assem_core>
            <n_assem_batch>1</n_assem_batch>
            <power_cap>1000</power_cap>
        </Reactor>
    </config>
</facility>

<facility>
    <name>lwr5</name>
    <lifetime>1040</lifetime>
    <config>
        <Reactor>
            <fuel_inrecipes>
                <val>lwrinrecipe</val>
            </fuel_inrecipes>
            <fuel_outrecipes>
                <val>lwroutrecipe</val>
            </fuel_outrecipes>
            <fuel_incommods>
                <val>enrichmentout</val>
            </fuel_incommods>
            <fuel_outcommods>
                <val>lwrout</val>
            </fuel_outcommods>
            <cycle_time>18</cycle_time>
            <refuel_time>0</refuel_time>
            <assem_size>29863.3</assem_size>
            <n_assem_core>3</n_assem_core>
            <n_assem_batch>1</n_assem_batch>
            <power_cap>1000</power_cap>
        </Reactor>
    </config>
</facility>

<facility>
    <name>lwr6</name>
    <lifetime>1060</lifetime>
    <config>
        <Reactor>
            <fuel_inrecipes>
                <val>lwrinrecipe</val>
            </fuel_inrecipes>
            <fuel_outrecipes>
                <val>lwroutrecipe</val>
            </fuel_outrecipes>
            <fuel_incommods>
                <val>enrichmentout</val>
            </fuel_incommods>
            <fuel_outcommods>
                <val>lwrout</val>
            </fuel_outcommods>
            <cycle_time>18</cycle_time>
            <refuel_time>0</refuel_time>
            <assem_size>29863.3</assem_size>
            <n_assem_core>3</n_assem_core>
            <n_assem_batch>1</n_assem_batch>
            <power_cap>1000</power_cap>
        </Reactor>
    </config>
</facility>

<facility>
    <name>lwr7</name>
    <lifetime>1080</lifetime>
    <config>
        <Reactor>
            <fuel_inrecipes>
                <val>lwrinrecipe</val>
            </fuel_inrecipes>
            <fuel_outrecipes>
                <val>lwroutrecipe</val>
            </fuel_outrecipes>
            <fuel_incommods>
                <val>enrichmentout</val>
            </fuel_incommods>
            <fuel_outcommods>
                <val>lwrout</val>
            </fuel_outcommods>
            <cycle_time>18</cycle_time>
            <refuel_time>0</refuel_time>
            <assem_size>29863.3</assem_size>
            <n_assem_core>3</n_assem_core>
            <n_assem_batch>1</n_assem_batch>
            <power_cap>1000</power_cap>
        </Reactor>
    </config>
</facility>

<facility>
    <name>lwr8</name>
    <lifetime>1100</lifetime>
    <config>
        <Reactor>
            <fuel_inrecipes>
                <val>lwrinrecipe</val>
            </fuel_inrecipes>
            <fuel_outrecipes>
                <val>lwroutrecipe</val>
            </fuel_outrecipes>
            <fuel_incommods>
                <val>enrichmentout</val>
            </fuel_incommods>
            <fuel_outcommods>
                <val>lwrout</val>
            </fuel_outcommods>
            <cycle_time>18</cycle_time>
            <refuel_time>0</refuel_time>
            <assem_size>29863.3</assem_size>
            <n_assem_core>3</n_assem_core>
            <n_assem_batch>1</n_assem_batch>
            <power_cap>1000</power_cap>
        </Reactor>
    </config>
</facility>

<facility>
    <name>lwr9</name>
    <lifetime>1120</lifetime>
    <config>
        <Reactor>
            <fuel_inrecipes>
                <val>lwrinrecipe</val>
            </fuel_inrecipes>
            <fuel_outrecipes>
                <val>lwroutrecipe</val>
            </fuel_outrecipes>
            <fuel_incommods>
                <val>enrichmentout</val>
            </fuel_incommods>
            <fuel_outcommods>
                <val>lwrout</val>
            </fuel_outcommods>
            <cycle_time>18</cycle_time>
            <refuel_time>0</refuel_time>
            <assem_size>29863.3</assem_size>
            <n_assem_core>3</n_assem_core>
            <n_assem_batch>1</n_assem_batch>
            <power_cap>1000</power_cap>
        </Reactor>
    </config>
</facility>

<facility>
    <name>lwr10</name>
    <lifetime>1140</lifetime>
    <config>
        <Reactor>
            <fuel_inrecipes>
                <val>lwrinrecipe</val>
            </fuel_inrecipes>
            <fuel_outrecipes>
                <val>lwroutrecipe</val>
            </fuel_outrecipes>
            <fuel_incommods>
                <val>enrichmentout</val>
            </fuel_incommods>
            <fuel_outcommods>
                <val>lwrout</val>
            </fuel_outcommods>
            <cycle_time>18</cycle_time>
            <refuel_time>0</refuel_time>
            <assem_size>29863.3</assem_size>
            <n_assem_core>3</n_assem_core>
            <n_assem_batch>1</n_assem_batch>
            <power_cap>1000</power_cap>
        </Reactor>
    </config>
</facility>

<facility>
    <name>fr</name>
    <lifetime>720</lifetime>
    <config>
        <Reactor>
            <fuel_inrecipes>
                <val>frinrecipe</val>
            </fuel_inrecipes>
            <fuel_outrecipes>
                <val>froutrecipe</val>
            </fuel_outrecipes>
            <fuel_incommods>
                <val>mixerout</val>
            </fuel_incommods>
            <fuel_outcommods>
                <val>frout</val>
            </fuel_outcommods>
            <cycle_time>12</cycle_time>
            <refuel_time>0</refuel_time>
            <assem_size>5867</assem_size>
            <n_assem_core>4</n_assem_core>
            <n_assem_batch>1</n_assem_batch>
            <power_cap>333.34</power_cap>
        </Reactor>
    </config>
</facility>

<facility>
    <name>lwrstorage</name>
    <config>
        <Storage>
            <in_commods>
                <val>lwrout</val>
            </in_commods>
            <residence_time>36</residence_time>
            <out_commods>
                <val>lwrstorageout</val>
            </out_commods>
            <max_inv_size>1e7</max_inv_size>
        </Storage>
    </config>
</facility>

<facility>
    <name>frstorage</name>
    <config>
        <Storage>
            <in_commods>
                <val>frout</val>
            </in_commods>
            <residence_time>36</residence_time>
            <out_commods>
                <val>frstorageout</val>
            </out_commods>
            <max_inv_size>1e7</max_inv_size>
        </Storage>
    </config>
</facility>

<facility>
    <name>lwrreprocessing</name>
    <config>
        <Separations>
            <feed_commods>
                <val>lwrstorageout</val>
            </feed_commods>
            <feedbuf_size>1e8</feedbuf_size>
            <throughput>1e8</throughput>
            <leftover_commod>lwrreprocessingwaste</leftover_commod>
            <leftoverbuf_size>1e8</leftoverbuf_size>
            <streams>
                <item>
                    <commod>lwrpu</commod>
                    <info>
                        <buf_size>1e8</buf_size>
                        <efficiencies>
                            <item>
                                <comp>Pu</comp>
                                <eff>1.0</eff>
                            </item>
                        </efficiencies>
                    </info>
                </item>
                <item>
                    <commod>lwru</commod>
                    <info>
                        <buf_size>1e8</buf_size>
                        <efficiencies>
                            <item>
                                <comp>U</comp>
                                <eff>1.0</eff>
                            </item>
                        </efficiencies>
                    </info>
                </item>
            </streams>
        </Separations>
    </config>
</facility>

<facility>
    <name>frreprocessing</name>
    <config>
        <Separations>
            <feed_commods>
                <val>frstorageout</val>
            </feed_commods>
            <feedbuf_size>1e8</feedbuf_size>
            <throughput>1e8</throughput>
            <leftover_commod>frreprocessingwaste</leftover_commod>
            <leftoverbuf_size>1e8</leftoverbuf_size>
            <streams>
                <item>
                    <commod>frpu</commod>
                    <info>
                        <buf_size>1e8</buf_size>
                        <efficiencies>
                            <item>
                                <comp>Pu</comp>
                                <eff>1.0</eff>
                            </item>
                        </efficiencies>
                    </info>
                </item>
                <item>
                    <commod>fru</commod>
                    <info>
                        <buf_size>1e8</buf_size>
                        <efficiencies>
                            <item>
                                <comp>U</comp>
                                <eff>1.0</eff>
                            </item>
                        </efficiencies>
                    </info>
                </item>
            </streams>
        </Separations>
    </config>
</facility>

<facility>
    <name>lwrmixer</name>
    <config>
        <Mixer>
            <in_streams>
                <stream>
                    <info>
                        <mixing_ratio>0.129</mixing_ratio>
                        <buf_size>1e6</buf_size>
                    </info>
                    <commodities>
                        <item>
                            <commodity>lwrpu</commodity>
                            <pref>1.0</pref>
                        </item>          
                    </commodities>
                </stream>
                <stream>
                    <info>
                        <mixing_ratio>0.714</mixing_ratio>
                        <buf_size>1e7</buf_size>
                    </info>
                    <commodities>
                        <item>
                            <commodity>lwru</commodity>
                            <pref>1.0</pref>
                        </item>                    
                    </commodities>
                </stream>
                <stream>
                    <info>
                        <mixing_ratio>0.157</mixing_ratio>
                        <buf_size>1e7</buf_size>
                    </info>
                    <commodities>
                        <item>
                            <commodity>sourceout</commodity>
                            <pref>1.0</pref>
                        </item>
                    </commodities>
                </stream>
            </in_streams>
            <out_commod>mixerout</out_commod>
            <out_buf_size>1e10</out_buf_size>
            <throughput>1e7</throughput>
        </Mixer>
    </config>
</facility>

<facility>
    <name>frmixer</name>
    <config>
        <Mixer>
            <in_streams>
                <stream>
                    <info>
                        <mixing_ratio>0.129</mixing_ratio>
                        <buf_size>1e6</buf_size>
                    </info>
                    <commodities>
                        <item>
                            <commodity>frpu</commodity>
                            <pref>1.0</pref>
                        </item>          
                    </commodities>
                </stream>
                <stream>
                    <info>
                        <mixing_ratio>0.714</mixing_ratio>
                        <buf_size>1e7</buf_size>
                    </info>
                    <commodities>
                        <item>
                            <commodity>fru</commodity>
                            <pref>1.0</pref>
                        </item>                    
                    </commodities>
                </stream>
                <stream>
                    <info>
                        <mixing_ratio>0.157</mixing_ratio>
                        <buf_size>1e7</buf_size>
                    </info>
                    <commodities>
                        <item>
                            <commodity>sourceout</commodity>
                            <pref>1.0</pref>
                        </item>
                    </commodities>
                </stream>
            </in_streams>
            <out_commod>mixerout</out_commod>
            <out_buf_size>1e10</out_buf_size>
            <throughput>1e7</throughput>
        </Mixer>
    </config>
</facility>

<facility>
    <name>lwrsink</name>
    <config>
        <Sink>
            <in_commods>
                <val>lwrreprocessingwaste</val>
            </in_commods>
            <max_inv_size>1e10</max_inv_size>
        </Sink>
    </config>
</facility>

<facility>
    <name>frsink</name>
    <config>
        <Sink>
            <in_commods>
                <val>frreprocessingwaste</val>
            </in_commods>
            <max_inv_size>1e10</max_inv_size>
        </Sink>
    </config>
</facility>
"""

recipes = """
<recipe>
    <name>sourceoutrecipe</name>
    <basis>mass</basis>
    <nuclide> <id>U235</id> <comp>0.711</comp> </nuclide>
    <nuclide> <id>U238</id> <comp>99.289</comp> </nuclide>
</recipe>
 
<recipe>
    <name>lwrinrecipe</name>
    <basis>mass</basis>
    <nuclide> <id>U234</id>  <comp>0.0002558883</comp> </nuclide> 
    <nuclide> <id>U235</id>  <comp>0.0319885317</comp> </nuclide> 
    <nuclide> <id>U238</id>  <comp>0.96775558</comp> </nuclide> 
</recipe> 

<recipe>
    <name>lwroutrecipe</name>
    <basis>mass</basis>
    <nuclide> <id>He4</id>  <comp>9.47457840128509E-07</comp> </nuclide> 
    <nuclide> <id>Ra226</id>  <comp>9.78856442957042E-14</comp> </nuclide> 
    <nuclide> <id>Ra228</id>  <comp>2.75087759176098E-20</comp> </nuclide> 
    <nuclide> <id>Pb206</id>  <comp>5.57475193532078E-18</comp> </nuclide> 
    <nuclide> <id>Pb207</id>  <comp>1.68592497990149E-15</comp> </nuclide> 
    <nuclide> <id>Pb208</id>  <comp>3.6888358546006E-12</comp> </nuclide> 
    <nuclide> <id>Pb210</id>  <comp>3.02386544437848E-19</comp> </nuclide> 
    <nuclide> <id>Th228</id>  <comp>8.47562285269577E-12</comp> </nuclide> 
    <nuclide> <id>Th229</id>  <comp>2.72787861516683E-12</comp> </nuclide> 
    <nuclide> <id>Th230</id>  <comp>2.6258831537493E-09</comp> </nuclide> 
    <nuclide> <id>Th232</id>  <comp>4.17481422959E-10</comp> </nuclide> 
    <nuclide> <id>Bi209</id>  <comp>6.60770597104927E-16</comp> </nuclide> 
    <nuclide> <id>Ac227</id>  <comp>3.0968621961773E-14</comp> </nuclide> 
    <nuclide> <id>Pa231</id>  <comp>9.24658854635179E-10</comp> </nuclide> 
    <nuclide> <id>U232</id>  <comp>0.000000001</comp> </nuclide> 
    <nuclide> <id>U233</id>  <comp>2.21390148606282E-09</comp> </nuclide> 
    <nuclide> <id>U234</id>  <comp>0.0001718924</comp> </nuclide> 
    <nuclide> <id>U235</id>  <comp>0.0076486597</comp> </nuclide> 
    <nuclide> <id>U236</id>  <comp>0.0057057461</comp> </nuclide> 
    <nuclide> <id>U238</id>  <comp>0.9208590237</comp> </nuclide> 
    <nuclide> <id>Np237</id>  <comp>0.0006091729</comp> </nuclide> 
    <nuclide> <id>Pu238</id>  <comp>0.000291487</comp> </nuclide> 
    <nuclide> <id>Pu239</id>  <comp>0.0060657301</comp> </nuclide> 
    <nuclide> <id>Pu240</id>  <comp>0.0029058707</comp> </nuclide> 
    <nuclide> <id>Pu241</id>  <comp>0.0017579218</comp> </nuclide> 
    <nuclide> <id>Pu242</id>  <comp>0.0008638616</comp> </nuclide> 
    <nuclide> <id>Pu244</id>  <comp>2.86487251922763E-08</comp> </nuclide> 
    <nuclide> <id>Am241</id>  <comp>6.44271331287386E-05</comp> </nuclide> 
    <nuclide> <id>Am242m</id>  <comp>8.53362027193319E-07</comp> </nuclide> 
    <nuclide> <id>Am243</id>  <comp>0.0001983912</comp> </nuclide> 
    <nuclide> <id>Cm242</id>  <comp>2.58988475560194E-05</comp> </nuclide> 
    <nuclide> <id>Cm243</id>  <comp>0.000000771</comp> </nuclide> 
    <nuclide> <id>Cm244</id>  <comp>8.5616190260478E-05</comp> </nuclide> 
    <nuclide> <id>Cm245</id>  <comp>5.72174539442251E-06</comp> </nuclide> 
    <nuclide> <id>Cm246</id>  <comp>7.29567535786554E-07</comp> </nuclide> 
    <nuclide> <id>Cm247</id>  <comp>0.00000001</comp> </nuclide> 
    <nuclide> <id>Cm248</id>  <comp>7.69165773748653E-10</comp> </nuclide> 
    <nuclide> <id>Cm250</id>  <comp>4.2808095130239E-18</comp> </nuclide> 
    <nuclide> <id>Cf249</id>  <comp>1.64992658175413E-12</comp> </nuclide> 
    <nuclide> <id>Cf250</id>  <comp>2.04190913935875E-12</comp> </nuclide> 
    <nuclide> <id>Cf251</id>  <comp>9.86556100338561E-13</comp> </nuclide> 
    <nuclide> <id>Cf252</id>  <comp>6.57970721693466E-13</comp> </nuclide> 
    <nuclide> <id>H3</id>  <comp>8.58461800264195E-08</comp> </nuclide> 
    <nuclide> <id>C14</id>  <comp>4.05781943561107E-11</comp> </nuclide> 
    <nuclide> <id>Kr81</id>  <comp>4.21681236076192E-11</comp> </nuclide> 
    <nuclide> <id>Kr85</id>  <comp>3.44484671160181E-05</comp> </nuclide> 
    <nuclide> <id>Sr90</id>  <comp>0.0007880649</comp> </nuclide> 
    <nuclide> <id>Tc99</id>  <comp>0.0011409492</comp> </nuclide> 
    <nuclide> <id>I129</id>  <comp>0.0002731878</comp> </nuclide> 
    <nuclide> <id>Cs134</id>  <comp>0.0002300898</comp> </nuclide> 
    <nuclide> <id>Cs135</id>  <comp>0.0006596706</comp> </nuclide> 
    <nuclide> <id>Cs137</id>  <comp>0.0018169192</comp> </nuclide> 
    <nuclide> <id>H1</id>  <comp>0.0477938151</comp> </nuclide> 
</recipe> 

<recipe>
    <name>frinrecipe</name>
    <basis>mass</basis>
    <nuclide> <id>U234</id>  <comp>9.7224110389438E-05</comp> </nuclide> 
    <nuclide> <id>U235</id>  <comp>0.0039469814</comp> </nuclide> 
    <nuclide> <id>U236</id>  <comp>0.0021573569</comp> </nuclide> 
    <nuclide> <id>U238</id>  <comp>0.8665733427</comp> </nuclide> 
    <nuclide> <id>Np237</id>  <comp>0.0060565044</comp> </nuclide> 
    <nuclide> <id>Pu238</id>  <comp>0.0030040068</comp> </nuclide> 
    <nuclide> <id>Pu239</id>  <comp>0.0606135352</comp> </nuclide> 
    <nuclide> <id>Pu240</id>  <comp>0.0286774758</comp> </nuclide> 
    <nuclide> <id>Pu241</id>  <comp>0.0134998465</comp> </nuclide> 
    <nuclide> <id>Pu242</id>  <comp>0.0084034605</comp> </nuclide> 
    <nuclide> <id>Am241</id>  <comp>0.0042991968</comp> </nuclide> 
    <nuclide> <id>Am242m</id>  <comp>7.73428708584307E-06</comp> </nuclide> 
    <nuclide> <id>Am243</id>  <comp>0.0019207217</comp> </nuclide> 
    <nuclide> <id>Cm243</id>  <comp>6.47352555460846E-06</comp> </nuclide> 
    <nuclide> <id>Cm244</id>  <comp>0.0006812961</comp> </nuclide> 
    <nuclide> <id>Cm245</id>  <comp>5.48431266087054E-05</comp> </nuclide> 
    <nuclide> <id>H1</id>  <comp>0</comp> </nuclide> 
</recipe>

<recipe>
    <name>froutrecipe</name>
    <basis>mass</basis>
    <nuclide> <id>H1</id>  <comp>2.1237926533769418e-06</comp> </nuclide> 
    <nuclide> <id>H1</id>  <comp>2.1237926533769418e-06</comp> </nuclide> 
    <nuclide> <id>H2</id>  <comp>6.506416799362884e-07</comp> </nuclide> 
    <nuclide> <id>H3</id>  <comp>8.716143259523863e-06</comp> </nuclide> 
    <nuclide> <id>He3</id>  <comp>8.716143259523863e-06</comp> </nuclide> 
    <nuclide> <id>He4</id>  <comp>0.0001344250263264596</comp> </nuclide> 
    <nuclide> <id>Br85</id>  <comp>0.00037872256275536787</comp> </nuclide> 
    <nuclide> <id>Kr82</id>  <comp>3.375970980801497e-07</comp> </nuclide> 
    <nuclide> <id>Kr85</id>  <comp>8.470618097283756e-05</comp> </nuclide> 
    <nuclide> <id>Kr85m</id>  <comp>0.00037872256275536787</comp> </nuclide> 
    <nuclide> <id>Sr90</id>  <comp>0.0012466540112741529</comp> </nuclide> 
    <nuclide> <id>Zr95</id>  <comp>0.002873872024020474</comp> </nuclide> 
    <nuclide> <id>Nb94</id>  <comp>1.565222909280694e-09</comp> </nuclide> 
    <nuclide> <id>Nb95</id>  <comp>0.0028726443982092734</comp> </nuclide> 
    <nuclide> <id>Nb95m</id>  <comp>3.105893302337377e-05</comp> </nuclide> 
    <nuclide> <id>Mo94</id>  <comp>2.946301946881306e-12</comp> </nuclide> 
    <nuclide> <id>Mo96</id>  <comp>1.0434819395204624e-06</comp> </nuclide> 
    <nuclide> <id>Mo99</id>  <comp>0.003572391110593584</comp> </nuclide> 
    <nuclide> <id>Tc99</id>  <comp>0.003572391110593584</comp> </nuclide> 
    <nuclide> <id>Ru103</id>  <comp>0.0040450270479057936</comp> </nuclide> 
    <nuclide> <id>Ru106</id>  <comp>0.0025350473001291237</comp> </nuclide> 
    <nuclide> <id>Rh106</id>  <comp>0.0025350473001291237</comp> </nuclide> 
    <nuclide> <id>Sn121m</id>  <comp>3.2532083996814424e-06</comp> </nuclide> 
    <nuclide> <id>Sb122</id>  <comp>9.391337455684162e-09</comp> </nuclide> 
    <nuclide> <id>Sb124</id>  <comp>9.45271874624419e-07</comp> </nuclide> 
    <nuclide> <id>Sb125</id>  <comp>8.470618097283756e-05</comp> </nuclide> 
    <nuclide> <id>Te132</id>  <comp>0.003019959495553339</comp> </nuclide> 
    <nuclide> <id>I129</id>  <comp>0.0008040949063363564</comp> </nuclide> 
    <nuclide> <id>I131</id>  <comp>0.002510494783905113</comp> </nuclide> 
    <nuclide> <id>I133</id>  <comp>0.004290552210145902</comp> </nuclide> 
    <nuclide> <id>I135</id>  <comp>0.003830192530945698</comp> </nuclide> 
    <nuclide> <id>Xe128</id>  <comp>1.5345322640006803e-09</comp> </nuclide> 
    <nuclide> <id>Xe130</id>  <comp>1.4179078119366286e-06</comp> </nuclide> 
    <nuclide> <id>Xe131m</id>  <comp>2.7253293008652085e-05</comp> </nuclide> 
    <nuclide> <id>Xe133</id>  <comp>0.004315104726369913</comp> </nuclide> 
    <nuclide> <id>Xe133m</id>  <comp>0.00013688027794886068</comp> </nuclide> 
    <nuclide> <id>Xe135</id>  <comp>0.004603596792002041</comp> </nuclide> 
    <nuclide> <id>Xe135m</id>  <comp>0.001209211424032536</comp> </nuclide> 
    <nuclide> <id>Cs134</id>  <comp>7.05884841440313e-07</comp> </nuclide> 
    <nuclide> <id>Cs137</id>  <comp>0.003897711950561728</comp> </nuclide> 
    <nuclide> <id>Ba140</id>  <comp>0.003255049838398243</comp> </nuclide> 
    <nuclide> <id>La140</id>  <comp>0.0032679399094158487</comp> </nuclide> 
    <nuclide> <id>Ce141</id>  <comp>0.0030752026570573633</comp> </nuclide> 
    <nuclide> <id>Ce144</id>  <comp>0.0021508004212233535</comp> </nuclide> 
    <nuclide> <id>Pr144</id>  <comp>0.002151414234128954</comp> </nuclide> 
    <nuclide> <id>Nd142</id>  <comp>1.540670393056683e-09</comp> </nuclide> 
    <nuclide> <id>Nd144</id>  <comp>0.002151414234128954</comp> </nuclide> 
    <nuclide> <id>Nd147</id>  <comp>0.001184045094902925</comp> </nuclide> 
    <nuclide> <id>Pm147</id>  <comp>0.001184045094902925</comp> </nuclide> 
    <nuclide> <id>Pm148</id>  <comp>7.365754867203266e-09</comp> </nuclide> 
    <nuclide> <id>Pm148m</id>  <comp>1.780057426240789e-08</comp> </nuclide> 
    <nuclide> <id>Pm149</id>  <comp>0.0007826114546403469</comp> </nuclide> 
    <nuclide> <id>Pm151</id>  <comp>0.0004885950728578165</comp> </nuclide> 
    <nuclide> <id>Sm148</id>  <comp>2.3938703318410615e-08</comp> </nuclide> 
    <nuclide> <id>Sm150</id>  <comp>3.130445818561388e-06</comp> </nuclide> 
    <nuclide> <id>Sm151</id>  <comp>0.0004892088857634169</comp> </nuclide> 
    <nuclide> <id>Sm153</id>  <comp>0.00024552516224010884</comp> </nuclide> 
    <nuclide> <id>Eu151</id>  <comp>0.0004892088857634169</comp> </nuclide> 
    <nuclide> <id>Eu152</id>  <comp>2.9463019468813056e-10</comp> </nuclide> 
    <nuclide> <id>Eu154</id>  <comp>7.795423901123456e-08</comp> </nuclide> 
    <nuclide> <id>Eu155</id>  <comp>0.00010496200685764655</comp> </nuclide> 
    <nuclide> <id>Pu238</id>  <comp>0.00109335928440193</comp> </nuclide> 
    <nuclide> <id>Pu239</id>  <comp>0.0930067275743179</comp> </nuclide> 
    <nuclide> <id>Pu240</id>  <comp>0.030500623501972753</comp> </nuclide> 
    <nuclide> <id>Pu241</id>  <comp>0.0034020252053028497</comp> </nuclide> 
    <nuclide> <id>Pu242</id>  <comp>0.00170935846724797</comp> </nuclide> 
    <nuclide> <id>Pu244</id>  <comp>5.9667566e-09</comp> </nuclide> 
    <nuclide> <id>U232</id>  <comp>7.764620174645652e-09</comp> </nuclide> 
    <nuclide> <id>U233</id>  <comp>5.365956105805943e-09</comp> </nuclide> 
    <nuclide> <id>U234</id>  <comp>0.00015792257454093998</comp> </nuclide> 
    <nuclide> <id>U235</id>  <comp>0.00019371425185969997</comp> </nuclide> 
    <nuclide> <id>U236</id>  <comp>0.00030462860329308</comp> </nuclide> 
    <nuclide> <id>U238</id>  <comp>0.7843763214602618</comp> </nuclide> 
    <nuclide> <id>Am241</id>  <comp>0.0051501477520177</comp> </nuclide> 
    <nuclide> <id>Am242m</id>  <comp>0.000335357136931</comp> </nuclide> 
    <nuclide> <id>Am243</id>  <comp>0.0015164335378926998</comp> </nuclide> 
    <nuclide> <id>Cm242</id>  <comp>0.00022459089899389998</comp> </nuclide> 
    <nuclide> <id>Cm243</id>  <comp>1.3657049394099997e-05</comp> </nuclide> 
    <nuclide> <id>Cm244</id>  <comp>0.0007493459387043999</comp> </nuclide> 
    <nuclide> <id>Cm245</id>  <comp>0.00016582831469939997</comp> </nuclide> 
    <nuclide> <id>Cm246</id>  <comp>6.0434845141199995e-05</comp> </nuclide> 
    <nuclide> <id>Cm247</id>  <comp>2.2397642322999996e-06</comp> </nuclide> 
    <nuclide> <id>Cm248</id>  <comp>1.6006247130135967e-07</comp> </nuclide> 
    <nuclide> <id>Cm250</id>  <comp>2.6991508458592675e-14</comp> </nuclide> 
    <nuclide> <id>Cf249</id>  <comp>2.7154845877404104e-09</comp> </nuclide> 
    <nuclide> <id>Cf250</id>  <comp>2.823695627703007e-10</comp> </nuclide> 
    <nuclide> <id>Cf251</id>  <comp>8.017825545907209e-12</comp> </nuclide> 
    <nuclide> <id>Cf252</id>  <comp>1.691154800019082e-13</comp> </nuclide> 
    <nuclide> <id>Np237</id>  <comp>0.0029948016924556</comp> </nuclide> 
</recipe>
"""

region = {}

for calc_method in calc_methods:
    region[calc_method]= """
    <region>
        <config>
            <NullRegion>
            </NullRegion>
        </config>

        <institution>
        <config>
        <DemandDrivenDeploymentInst>
            <calc_method>%s</calc_method>
            <demand_eq>%s</demand_eq>
            <installed_cap>1</installed_cap>
            <steps>1</steps>
            <facility_commod>
            <item>
              <facility>source</facility>
              <commod>sourceout</commod>
            </item>
            <item>
              <facility>enrichment</facility>
              <commod>enrichmentout</commod>
            </item>
            <item>
              <facility>lwr</facility>
              <commod>POWER</commod>
            </item>
            <item>
              <facility>lwr1</facility>
              <commod>POWER</commod>
            </item>
            <item>
              <facility>lwr2</facility>
              <commod>POWER</commod>
            </item>
            <item>
              <facility>lwr3</facility>
              <commod>POWER</commod>
            </item>
            <item>
              <facility>lwr4</facility>
              <commod>POWER</commod>
            </item>
            <item>
              <facility>lwr5</facility>
              <commod>POWER</commod>
            </item>
            <item>
              <facility>lwr6</facility>
              <commod>POWER</commod>
            </item>
            <item>
              <facility>lwr7</facility>
              <commod>POWER</commod>
            </item>
            <item>
              <facility>lwr8</facility>
              <commod>POWER</commod>
            </item>
            <item>
              <facility>lwr9</facility>
              <commod>POWER</commod>
            </item>
            <item>
              <facility>lwr10</facility>
              <commod>POWER</commod>
            </item>
            <item>
              <facility>fr</facility>
              <commod>POWER</commod>
            </item>
            </facility_commod>
            <facility_capacity>
            <item>
              <facility>source</facility>
              <capacity>1e9</capacity>
            </item>    
            <item>
              <facility>enrichment</facility>
              <capacity>1e100</capacity>
            </item>
            <item>
              <facility>lwr</facility>
              <capacity>1000</capacity>
            </item>
            <item>
              <facility>lwr1</facility>
              <capacity>1000</capacity>
            </item>
            <item>
              <facility>lwr2</facility>
              <capacity>1000</capacity>
            </item>
            <item>
              <facility>lwr3</facility>
              <capacity>1000</capacity>
            </item>
            <item>
              <facility>lwr4</facility>
              <capacity>1000</capacity>
            </item>
            <item>
              <facility>lwr5</facility>
              <capacity>1000</capacity>
            </item>
            <item>
              <facility>lwr6</facility>
              <capacity>1000</capacity>
            </item>
            <item>
              <facility>lwr7</facility>
              <capacity>1000</capacity>
            </item>
            <item>
              <facility>lwr8</facility>
              <capacity>1000</capacity>
            </item>
            <item>
              <facility>lwr9</facility>
              <capacity>1000</capacity>
            </item>
            <item>
              <facility>lwr10</facility>
              <capacity>1000</capacity>
            </item>
            <item>
              <facility>fr</facility>
              <capacity>333.34</capacity>
            </item>
            </facility_capacity>
            <facility_pref>
            <item>
              <facility>lwr</facility>
              <pref>(959-t)*(t-10)</pref>
            </item>
            <item>
              <facility>lwr1</facility>
              <pref>-1</pref>
            </item>
            <item>
              <facility>lwr2</facility>
              <pref>-1</pref>
            </item>
            <item>
              <facility>lwr3</facility>
              <pref>-1</pref>
            </item>
            <item>
              <facility>lwr4</facility>
              <pref>-1</pref>
            </item>
            <item>
              <facility>lwr5</facility>
              <pref>-1</pref>
            </item>
            <item>
              <facility>lwr6</facility>
              <pref>-1</pref>
            </item>
            <item>
              <facility>lwr7</facility>
              <pref>-1</pref>
            </item>
            <item>
              <facility>lwr8</facility>
              <pref>-1</pref>
            </item>
            <item>
              <facility>lwr9</facility>
              <pref>-1</pref>
            </item>
            <item>
              <facility>lwr10</facility>
              <pref>-1</pref>
            </item>
            <item>
              <facility>fr</facility>
              <pref>t-960</pref>
            </item>
            </facility_pref>
        </DemandDrivenDeploymentInst>
        </config>
        <name>timeseriesinst</name>
        <initialfacilitylist>
            <entry>
              <number>6</number>
              <prototype>lwr1</prototype>
            </entry>
            <entry>
              <number>6</number>
              <prototype>lwr2</prototype>
            </entry>
            <entry>
              <number>6</number>
              <prototype>lwr3</prototype>
            </entry>
            <entry>
              <number>6</number>
              <prototype>lwr4</prototype>
            </entry>
            <entry>
              <number>6</number>
              <prototype>lwr5</prototype>
            </entry>
            <entry>
              <number>6</number>
              <prototype>lwr6</prototype>
            </entry>
            <entry>
              <number>6</number>
              <prototype>lwr7</prototype>
            </entry>
            <entry>
              <number>6</number>
              <prototype>lwr8</prototype>
            </entry>
            <entry>
              <number>6</number>
              <prototype>lwr9</prototype>
            </entry>
            <entry>
              <number>6</number>
              <prototype>lwr10</prototype>
            </entry>
            </initialfacilitylist>
        </institution>

        <institution>
        <config>
        <SupplyDrivenDeploymentInst>
            <calc_method>%s</calc_method>
            <facility_commod>
            <item>
                <facility>lwrreprocessing</facility>
                <commod>lwrstorageout</commod>
            </item>
            <item>
                <facility>frreprocessing</facility>
                <commod>frstorageout</commod>
            </item>
            <item>
                <facility>lwrmixer</facility>
                <commod>lwrpu</commod>
            </item>
            <item>
                <facility>frmixer</facility>
                <commod>frpu</commod>
            </item>
            <item>
                <facility>lwrstorage</facility>
                <commod>lwrout</commod>
            </item>
            <item>
                <facility>frstorage</facility>
                <commod>frout</commod>
            </item>
            <item>
                <facility>lwrsink</facility>
                <commod>lwrreprocessingwaste</commod>
            </item>
            <item>
                <facility>frsink</facility>
                <commod>frreprocessingwaste</commod>
            </item>
            </facility_commod>
            <facility_capacity>
            <item>
                <facility>lwrreprocessing</facility>
                <capacity>1e8</capacity>
            </item>
            <item>
                <facility>frreprocessing</facility>
                <capacity>1e8</capacity>
            </item>
            <item>
                <facility>lwrmixer</facility>
                <capacity>1e6</capacity>
            </item>
            <item>
                <facility>frmixer</facility>
                <capacity>1e6</capacity>
            </item>
            <item>
                <facility>lwrstorage</facility>
                <capacity>1e7</capacity>
            </item>
            <item>
                <facility>frstorage</facility>
                <capacity>1e7</capacity>
            </item>
            <item>
                <facility>lwrsink</facility>
                <capacity>1e10</capacity>
            </item>
            <item>
                <facility>frsink</facility>
                <capacity>1e10</capacity>
            </item>
            </facility_capacity>
        </SupplyDrivenDeploymentInst>
        </config>
        <name>supplydrivendeploymentinst</name>
        </institution>

        <name>SingleRegion</name>
    </region>
    """%(calc_method,demand_eq,calc_method)

metric_dict = {}
agent_entry_dict = {}
all_dict = {}
commod_dict = {'enrichmentout': ['enrichment'],
               'sourceout': ['source'],
               'power': ['lwr', 'fr'],
               'lwrstorageout': ['lwrreprocessing'],
               'frstorageout': ['frreprocessing'],
               'lwrout': ['lwrstorage'],
               'frout': ['frstorage'],
               'lwrpu': ['pumixerlwr'],
               'frpu': ['pumixerfr'],
               'lwrreprocessingwaste': ['lwrsink'],
               'frreprocessingwaste': ['frsink']}

front_commods = ['sourceout', 'enrichmentout']
back_commods = ['lwrstorageout', 'frstorageout', 'lwrout', 'frout',
                'lwrreprocessingwaste', 'frreprocessingwaste', 'frpu',
                'lwrpu']

for calc_method in calc_methods:

    input_file = 'eg01-eg23-flatpower-d3ploy-installed-'+ calc_method +'.xml'
    output_file = 'eg01-eg23-flatpower-d3ploy-installed-'+ calc_method +'.sqlite'
   
    with open(input_file, 'w') as f:
        f.write('<simulation>\n')
        f.write(control)
        f.write(region[calc_method])
        f.write(recipes)
        f.write('</simulation>')

    s = subprocess.check_output(['cyclus', '-o', output_file, input_file],
                            universal_newlines=True, env=ENV)

"""
    for commod, facility in commod_dict.items():
        agent_entry_dict[commod] = tester.get_agent_dict(output_file, facility)

    all_dict['power'] = tester.supply_demand_dict_driving(
    output_file, demand_eq, 'power')

    plotter.plot_demand_supply_agent(all_dict['power'], agent_entry_dict['power'],
                                 'power', 'eg01-eg23-flatpower-d3ploy'+ calc_method +'_power',
                                 True, True, False, 1)

    metric_dict = tester.metrics(
        all_dict['power'], metric_dict, calc_method, 'power', True)

    for commod in front_commods:
        all_dict[commod] = tester.supply_demand_dict_nondriving(output_file,
                                                                commod, True)
        metric_dict = tester.metrics(
            all_dict[commod], metric_dict, calc_method, commod, True)

    for commod in back_commods:
        all_dict[commod] = tester.supply_demand_dict_nondriving(output_file,
                                                                commod, False)
        metric_dict = tester.metrics(
            all_dict[commod], metric_dict, calc_method, commod, False)
  
    df = pd.DataFrame(metric_dict)
    df.to_csv('eg01-eg23-flatpower-d3ploy.csv')
"""

