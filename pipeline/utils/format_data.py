from utils.format_iso_code import iso2_to_name, iso2_to_flag
from typing import TypedDict, Literal, Optional, Dict

Requirement = Literal[
    "visa_required",
    "visa_on_arrival",
    "e_visa",
    "eta",
    "visa_free",
    "no_admission",
]

class DestinationRule(TypedDict):
    requirement: Requirement
    max_stay_days: Optional[int]
    
class RawPassportRow(TypedDict):
    Passport: str
    Destination:str
    Requirement: str


# {"NGA": {"GHA": {...}}}
FormattedPassportData = Dict[str, Dict[str, DestinationRule]]


def normalise_rquirement(raw:str)-> Optional[DestinationRule]:
    """
    Turns a raw CSV value into a DestinationRule.
    Returns None for -1 (own country), so the caller can skip it.
    """
    value = raw.strip().lower()
    if value.isdigit():
        return {"requirement": "visa_free", "max_stay_days": int(value)}

    mapping: Dict[str, Requirement] = {
        "visa required": "visa_required",
        "visa on arrival": "visa_on_arrival",
        "e-visa": "e_visa",
        "eta": "eta",
        "visa free": "visa_free",
        "no admission": "no_admission",
    } 
    
    if value not in mapping:
        raise ValueError(f"Unknown requirement value: {raw!r}")

    return {"requirement": mapping[value], "max_stay_days": None}

def format_data(data:list[RawPassportRow]) -> FormattedPassportData:
    formatted_data: FormattedPassportData = {}
    for item  in  data:
        passport, destination, requirement = item.values()
        if requirement == '-1':
            continue
        formatted_data.setdefault(passport, {})[destination] = normalise_rquirement(requirement)
        print(iso2_to_name(passport), iso2_to_flag(destination) , iso2_to_name(destination), formatted_data[passport][destination])
    return formatted_data
        