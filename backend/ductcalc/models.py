from dataclasses import dataclass
import math
from backend.ductcalc.fitting_db import get_loss_coefficient

@dataclass
class DuctSegment:
    length_ft: float
    diameter_in: float
    airflow_cfm: float

    @property
    def area_sqft(self):
        diameter_ft = self.diameter_in / 12
        return math.pi * (diameter_ft ** 2) / 4

    @property
    def velocity_fpm(self):
        return self.airflow_cfm / self.area_sqft
    
    @property
    def velocity_pressure_inwg(self):
        return (self.velocity_fpm / 4005) ** 2
    

@dataclass
class Fitting:
    fitting_type: str
    airflow_cfm: float
    diameter_in: float

    @property
    def area_sqft(self):
        diameter_ft = self.diameter_in / 12
        return math.pi * (diameter_ft **2) / 4
    
    @property
    def velocity_fpm(self):
        return self.airflow_cfm / self.area_sqft

    @property
    def velocity_pressure_inwg(self):
        return (self.velocity_fpm / 4005) ** 2
    
    @property
    def loss_coefficient(self):
        return get_loss_coefficient(self.fitting_type)
    
    
@dataclass
class Path:
    name: str
    items: list