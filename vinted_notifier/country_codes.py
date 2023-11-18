from typing import Literal

class CountryCodes:
    
    FR = "FR"
    IT = "IT"
    # add other country later

    
    @classmethod
    def getAllCountryCodesAsLiteral(cls):
        country_codes = []
        for attr in dir(cls):
            if not callable(getattr(cls, attr)) and not attr.startswith("__"):
                country_codes.append(getattr(cls, attr))
        return country_codes
        