import pycountry
from constants.countries import EXTRA_COUNTRIES

def iso2_to_name(iso2_code:str) -> str:
    country = pycountry.countries.get(alpha_2=iso2_code)
    if iso2_code in EXTRA_COUNTRIES:
            return EXTRA_COUNTRIES[iso2_code]
    if country is None:
        raise ValueError(f"Unknown ISO2 code: {iso2_code!r}")
    return country.name

def iso2_to_flag(iso2_code:str) -> str:
    return "".join(chr(0x1F1E6 + ord(letter) - ord("A")) for letter in iso2_code)

    