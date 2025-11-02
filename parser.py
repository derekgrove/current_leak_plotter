import tomllib
import csv
from pathlib import Path
from datetime import datetime
from collections import defaultdict

def _load_files():
    script_dir = Path(__file__).parent

    options_toml = script_dir / "options.toml"
    db_csv = script_dir / "pixel_db_results.csv"
    
    with open(options_toml, 'rb') as f:
        options = tomllib.load(f)

    with open(db_csv, 'r') as f:
        reader = csv.reader(f)
        db_data = list(reader)

    # debug:
    # print(options)
    # print(db_currents)

    return options, db_data


def _parse_data():

    options, db_data = _load_files()

    if options['plot_specific_modules']:
        modules = set(options['specific_modules'])
        db_data = [entry for entry in db_data if entry[0] in modules]
        
    
    # Create dictionary with module names as keys
    data_by_module = defaultdict(list)
    
    for entry in db_data[1:]:  # Skip header if present
        module_name = entry[0]
        date = format_date(entry[1])
        current = float(entry[2])
        
        # Append tuple of (date, current)
        data_by_module[module_name].append((date, current))
    
    return data_by_module

def format_date(date_str):

    """
    converts the date string to a datetime obj with useful methods
    examples:

    print(date_obj)  # 2025-05-29 09:11:36
    print(date_obj.year)   # 2025
    print(date_obj.month)  # 5
    print(date_obj.day)    # 29
    print(date_obj.hour)   # 9
    """

    return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')

def filtered_selection():
    return


def main():
    #print("starting main... ")
    _parse_data()
    return

if __name__ == "__main__":
    main()