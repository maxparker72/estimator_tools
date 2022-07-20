class item: 
    def __init__(self, desc, cost):
        self._desc = desc
        self._cost = cost
    
    def get_desc(self):
        return self._desc
    
    def get_cost(self):
        return self._cost