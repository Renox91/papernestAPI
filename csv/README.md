# CSV Coordinates Transformation

This script transforms Lambert 93 coordinates to GPS coordinates (WGS84)
in a CSV file.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python transform_coordinates.py input.csv output.csv
```

### Example

```bash
python transform_coordinates.py "2018_01_Sites_mobiles_2G_3G_4G_France_metropolitaine_L93.csv" "sites_mobiles_gps.csv"
```

## What the script does

1. **Reads the CSV file** with `;` delimiter
2. **Replaces columns** `x` and `y` with `lon` and `lat`
3. **Converts coordinates** Lambert 93 → GPS (WGS84)
4. **Ignores rows** with `#N/A` or invalid values
5. **Rounds coordinates** to 6 decimal places
6. **Shows progress** every 10,000 rows

## Result

- **Before**: `Operateur;x;y;2G;3G;4G`
- **After**: `Operateur;lon;lat;2G;3G;4G`

Lambert 93 coordinates are transformed into GPS coordinates that you can use with geocoding APIs.