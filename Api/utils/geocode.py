import requests
from Api.constants import API_URL, CSV_NAME, REVERSE_URL, MOBILE_OPERATORS
from .csv_utils import find_closest_antenna_per_operator

def get_city_code_from_coords(lon: float, lat: float, timeout=5.0):
    # reverse attend lat, lon (dans les params, pas dans l'ordre GeoJSON)
    r = requests.get(REVERSE_URL, params={"lat": lat, "lon": lon}, timeout=timeout)
    r.raise_for_status()
    data = r.json()
    features = data.get("features", [])
    if not features:
        return None
    props = features[0].get("properties", {}) or {}
    return props.get("citycode")

def check_providers_availability(lon,lat,citycode):
    antennas = find_closest_antenna_per_operator(lon, lat, CSV_NAME)
    filtered_antennas = {}
    
    for operator_code, antenna_data in antennas.items():
        citycode_data = get_city_code_from_coords(antenna_data['coordinates']['lon'], antenna_data['coordinates']['lat'])
        if citycode == citycode_data:
            filtered_antennas[operator_code] = antenna_data
    
    return filtered_antennas

def get_coverage(address):
    response = requests.get(API_URL, params={'q': address})
    data = response.json()
    
    # Extract the postcode from the address
    import re
    postcode_match = re.search(r'\b(\d{5})\b', address)
    target_postcode = postcode_match.group(1) if postcode_match else None

    for feature in data['features']:
        if target_postcode and feature['properties']['postcode'] == target_postcode:
            best_feature = feature
            break
    else:
        # If no match, take the first result
        print("No match, taking the first result")
        best_feature = data['features'][0]
    
    citycode = best_feature['properties']['citycode']
    coordinates = best_feature['geometry']['coordinates']
    lon, lat = coordinates[0], coordinates[1]
    
    # Get filtered antennas
    filtered_antennas = check_providers_availability(lon, lat, citycode)
    
    # Create result with all operators
    result = {}
    for operator_code, operator_name in MOBILE_OPERATORS.items():
        if operator_code in filtered_antennas:
            # Operator found, get technologies
            antenna = filtered_antennas[operator_code]
            result[operator_name] = antenna['technologies']
        else:
            # Operator not found
            result[operator_name] = None
    
    return result

