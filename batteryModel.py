import numpy as np

class batteryModel:

    soc = 80

    def __init__(self, Capa, maxChargePower, maxDischargePower, initSoc, dt):
        self.Capa = Capa
        self.maxChargePower = maxChargePower
        self.maxDischargePower = maxDischargePower
        self.initSoc = initSoc
        self.dt = dt
        global soc
        soc = initSoc
   
    def get_soc(self, battPower):
        global soc          
        soc_change = - np.maximum(np.minimum(battPower,self.maxDischargePower),self.maxChargePower)*self.dt/self.Capa*100               
        soc += soc_change
        return (soc)

