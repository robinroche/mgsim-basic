class pvModel:

    def __init__(self, eta, S):
        self.eta = eta
        self.S = S
   
    def get_output(self, irradiance):
        output = self.eta*self.S*irradiance
        return (output)

