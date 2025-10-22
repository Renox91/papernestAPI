"""
Constants
"""

API_URL = "https://api-adresse.data.gouv.fr/search/"
REVERSE_URL = "https://api-adresse.data.gouv.fr/reverse/"
CSV_NAME = "../csv/csv_processed.csv"

# Providers
MOBILE_OPERATORS = {
    20801: 'Orange',
    20810: 'SFR', 
    20815: 'Free',
    20820: 'Bouygues'
}

# Constantes pour les technologies mobiles
TECHNOLOGIES = {
    '2G': '2G',
    '3G': '3G', 
    '4G': '4G',
    '5G': '5G'
}

# Geographic filtering constants
GEOGRAPHIC_PREFILTER_RANGE = 0.2
