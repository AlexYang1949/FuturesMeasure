from charge.chargeResult import chargeResult
from charge.chargeModel import chargeModel
from strategy import ma

class chargeManager():
    def __init__(self,chargeResult,chargeModel):
        self.data = {}
        self.chargeResult = chargeResult
        self.chargeModel = chargeModel

    def startCharge(self):
        pass