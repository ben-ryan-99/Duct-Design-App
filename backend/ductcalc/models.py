from dataclasses import dataclass
import math


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
    