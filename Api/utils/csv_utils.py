import csv
import os
from django.conf import settings
import geopy.distance
from ..constants import MOBILE_OPERATORS

def distance_between_long_lat(lon1, lat1, lon2, lat2):
    return geopy.distance.geodesic((lat1, lon1), (lat2, lon2)).km

def find_closest_antenna_per_operator(target_lon, target_lat, csv_name, max_distance_km=10):
    csv_file_path = os.path.join(settings.BASE_DIR, 'csv', csv_name)
    
    # Dictionary to store closest antenna for each operator
    closest_antennas = {}
    
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=';')
            for row in reader:
                try:
                    # Get coordinates from CSV
                    lon = float(row['lon'].strip())
                    lat = float(row['lat'].strip())
                    # Calculate distance
                    distance = distance_between_long_lat(lon, lat, target_lon, target_lat)
                    # Skip if too far
                    if distance > max_distance_km:
                        continue
                    
                    # Get operator code
                    operator_code = int(row['Operateur'])
                    
                    # Check if this is the closest antenna for this operator
                    if operator_code not in closest_antennas or distance < closest_antennas[operator_code]['distance_km']:
                        
                        closest_antennas[operator_code] = {
                            'operator_code': operator_code,
                            'operator_name': MOBILE_OPERATORS.get(operator_code, 'Unknown'),
                            'coordinates': {'lat': lat, 'lon': lon},
                            'distance_km': round(distance, 3),
                            'technologies': {
                                '2G': bool(int(row['2G'])),
                                '3G': bool(int(row['3G'])),
                                '4G': bool(int(row['4G']))
                            }
                        }
                    
                except (ValueError, KeyError):
                    continue
            return closest_antennas
            
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return {}
