import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import pvModel
import wtModel
import batteryModel


###################
### INPUT DATA ###
###################

# Import load data
fname = 'load.csv'
load_data = np.genfromtxt(fname, 
                     delimiter=',', 
                     usecols = 0, 
                     missing_values='NA', 
                     usemask=True) 

# Import weather data
fname2 = 'weather_2014_nov_9.csv'
data = np.genfromtxt(fname2, 
                     delimiter=',', 
                     skip_header=1, 
                     usecols = np.array([0,10,20]), 
                     missing_values='NA', 
                     usemask=True) 

# Extract weather data
td = data[:,0] # time in epoch
td2 = pd.to_datetime(td, unit='s')
td3 = np.array(td2[:-1], dtype=np.datetime64)
wind_speed_data = data[:,1] # wind speed
rad_data = data[:,2] # irradiance


####################################
### SIMULATION: CREATE MICROGRID ###
###################################

# Simulation parameters
dt = 60 # s

# PV model
eta_pv1 = 0.15 # conversion efficiency
S_pv1 = 100; # area in m2
pv1 = pvModel.pvModel(eta_pv1, S_pv1)

# Battery model
Capa_batt1 = 20*1e3 # Wh
maxChargePower_batt1 = -10e3 # W
maxDischargePower_batt1 = 10e3 # W
initSoc_batt1 = 80 # %
batt1 = batteryModel.batteryModel(Capa_batt1, 
                                  maxChargePower_batt1, 
                                  maxDischargePower_batt1, 
                                  initSoc_batt1, 
                                  dt*1.0/3600)


##################################
### RUN SIMULATION WITH CONTROL ###
##################################

# Initialize output vectors
simLen = len(load_data)
load1 = np.zeros(simLen) 
pv1_out = np.zeros(simLen) 
batt1_out = np.zeros(simLen) 
batt1_soc = np.zeros(simLen) 
net_out = np.zeros(simLen) 

# Get system output
for ind in enumerate(load_data):
    i = ind[0]
    
    # Get load value
    load1[i] = load_data[i]*0.5
 
    # Get PV output   
    pv1_out[i] = pv1.get_output(rad_data[i])

    # Get battery output
    batt1_out[i] = load1[ind[0]] - pv1_out[i]
    batt1_soc[i] = batt1.get_soc(batt1_out[i])
    
    # Get net output
    net_out[i] = pv1_out[i] + batt1_out[i] - load1[i]


####################
### PLOT RESULTS ###
####################

fig = plt.figure(figsize=(10,10))
# Plot output
ax = plt.subplot(211)
plt.title('Output profile')
l_pv1 = plt.plot_date(td3, -pv1_out/1e3, fmt='b', tz='CET', 
                      xdate=True, ydate=False, 
                      alpha=0.5)
l_batt1 = plt.plot_date(td3, batt1_out/1e3, fmt='c', tz='CET', 
                      xdate=True, ydate=False, 
                      alpha=0.5)
l_load1 = plt.plot_date(td3, load1/1e3, fmt='r', tz='CET', 
                      xdate=True, ydate=False, 
                      alpha=0.5)
l_net = plt.plot_date(td3, net_out/1e3, fmt='g', tz='CET', 
                      xdate=True, ydate=False, 
                      alpha=0.5)
plt.xlabel('Time')
plt.ylabel('Output [kW]')
plt.legend(l_load1 + l_pv1 + l_batt1 + l_net, ['Load','PV output','Battery output','Net load'], loc='upper left')
plt.grid()
ax.text(0.985, 0.94, 'Resolution: 1 minute',
        verticalalignment='bottom', horizontalalignment='right',
        transform=ax.transAxes,
        color='grey', fontsize=8)

# Plot soc
ax2 = plt.subplot(212)
plt.title('SOC profile')
l_soc1 = plt.plot_date(td3, batt1_soc, fmt='b', tz='CET', 
                      xdate=True, ydate=False, 
                      alpha=0.5)
plt.xlabel('Time')
plt.ylabel('SOC [%]')
plt.legend(l_soc1, ['SOC'], loc='upper left')
plt.grid()
plt.show()

