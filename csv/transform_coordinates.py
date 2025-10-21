import csv
import sys
import os
from pyproj import Transformer

def lamber93_to_gps(x, y):
    # Create transformer from Lambert 93 (EPSG:2154) to WGS84 (EPSG:4326)
    transformer = Transformer.from_crs("EPSG:2154", "EPSG:4326", always_xy=True)
    long, lat = transformer.transform(x, y)
    return long, lat

def transform_csv(input_file, output_file):
    if not os.path.exists(input_file):
        print(f"Error: File {input_file} does not exist.")
        return False
    
    try:
        with open(input_file, 'r', encoding='utf-8') as infile, \
             open(output_file, 'w', encoding='utf-8', newline='') as outfile:
            
            reader = csv.DictReader(infile, delimiter=';')
            
            # Create new headers by replacing x,y with lon,lat
            fieldnames = []
            for field in reader.fieldnames:
                if field == 'x':
                    fieldnames.append('lon')
                elif field == 'y':
                    fieldnames.append('lat')
                else:
                    fieldnames.append(field)
            
            writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter=';')
            writer.writeheader()
            
            processed_rows = 0
            skipped_rows = 0
            
            for row in reader:
                try:
                    # Get x and y coordinates
                    x_val = row['x'].strip()
                    y_val = row['y'].strip()
                    
                    # Skip rows with invalid values
                    if x_val in ['#N/A', '', 'N/A', 'NULL'] or y_val in ['#N/A', '', 'N/A', 'NULL']:
                        skipped_rows += 1
                        continue
                    
                    # Convert to float to handle decimals
                    x_float = float(x_val)
                    y_float = float(y_val)
                    
                    # Transform coordinates
                    lon, lat = lamber93_to_gps(x_float, y_float)
                    
                    # Create new row with lon,lat instead of x,y
                    new_row = {}
                    for key, value in row.items():
                        if key == 'x':
                            new_row['lon'] = round(lon, 6)  # Round to 6 decimal places
                        elif key == 'y':
                            new_row['lat'] = round(lat, 6)  # Round to 6 decimal places
                        else:
                            new_row[key] = value
                    
                    writer.writerow(new_row)
                    processed_rows += 1
                    
                    # Show progress every 10000 rows
                    if processed_rows % 10000 == 0:
                        print(f"Processed rows: {processed_rows}")
                
                except (ValueError, KeyError) as e:
                    skipped_rows += 1
                    continue
            
            print(f"\nTransformation completed!")
            print(f"Processed rows: {processed_rows}")
            print(f"Skipped rows: {skipped_rows}")
            print(f"Output file: {output_file}")
            
            return True
            
    except Exception as e:
        print(f"Error during transformation: {e}")
        return False

def main():
    if len(sys.argv) != 3:
        print("Usage: python transform_coordinates.py input.csv output.csv")
        print("Example: python transform_coordinates.py sites_mobiles.csv sites_mobiles_gps.csv")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    print(f"Transforming {input_file} to {output_file}")
    print("Conversion Lambert 93 -> GPS (WGS84)")
    print("-" * 50)
    
    success = transform_csv(input_file, output_file)
    
    if success:
        print("\n✅ Transformation successful!")
    else:
        print("\n❌ Error during transformation")
        sys.exit(1)

if __name__ == "__main__":
    main()
