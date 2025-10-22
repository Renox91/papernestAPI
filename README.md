# Papernest API - Mobile Coverage Checker

## Overview
API to check mobile network coverage (2G, 3G, 4G) for any French address using real antenna data from French mobile operators.

## Features
- **Geocoding integration** with French government API (data.gouv.fr)
- **Mobile operator coverage lookup** for Orange, SFR, Free, and Bouygues
- **City code validation** to ensure accurate coverage data
- **Optimized processing** with geographic pre-filtering for fast response times
- **RESTful API** with JSON responses

## Installation

### Prerequisites
- Python 3.8+
- pip

### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Run the development server
python manage.py runserver
```

The API will be available at `http://localhost:8000/`

## API Endpoints

### 1. Coverage Check
```http
GET /coverage/?q={address}
```

**Parameters:**
- `q` (required): French address to check coverage for

**Example:**
```bash
curl "http://localhost:8000/coverage/?q=42+rue+papernest+75011+Paris"
```

**Response:**
```json
{
  "Orange": {"2G": true, "3G": true, "4G": false},
  "SFR": {"2G": true, "3G": false, "4G": false},
  "Free": {"2G": false, "3G": true, "4G": true},
  "Bouygues": {"2G": true, "3G": false, "4G": false},
}
```

**Response Format:**
- `true`: Technology available
- `false`: Technology not available

## How It Works

1. **Address Geocoding**: Converts the input address to GPS coordinates using the French government API
3. **Distance Calculation**: Uses geodesic distance to find the closest antenna for each operator
4. **City Validation**: Ensures antennas are in the same city as the target address
5. **Coverage Response**: Returns technology availability for each operator

## Data Sources

- **Antenna Data**: French mobile network antennas (2018 dataset)
- **Geocoding**: [API Adresse](https://api-adresse.data.gouv.fr/) - French government service
- **Coordinates**: Lambert 93 → WGS84 conversion for GPS compatibility

## Error Handling

The API returns appropriate HTTP status codes:

- `200`: Success
- `400`: Bad Request (missing address parameter)
- `404`: Address not found
- `503`: External service unavailable
- `500`: Internal server error