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

    return options, db_data


def _format_date(date_str):
    """Converts the date string to a datetime obj with useful methods."""
    return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')


def _is_in_time_range(date_obj, time_range):
    """Check if a datetime object falls within the specified time range."""
    if not time_range:
        return True
    
    start_date = _format_date(time_range[0])
    end_date = _format_date(time_range[1])
    
    return start_date <= date_obj <= end_date


def _parse_data_for_modules(db_data, module_names, time_range=None):
    """Parse data for a specific set of module names."""
    data_by_module = defaultdict(list)
    
    for entry in db_data[1:]:  # Skip header
        module_name = entry[0]
        if module_name in module_names:
            date = _format_date(entry[1])
            if _is_in_time_range(date, time_range):
                current = float(entry[2])
                data_by_module[module_name].append((date, current))
    
    return data_by_module


def _parse_data_by_filter(db_data, filter_string, time_range=None):
    """Parse data for modules containing a specific filter string."""
    data_by_module = defaultdict(list)
    
    for entry in db_data[1:]:  # Skip header
        module_name = entry[0]
        if filter_string in module_name:
            date = _format_date(entry[1])
            if _is_in_time_range(date, time_range):
                current = float(entry[2])
                data_by_module[module_name].append((date, current))
    
    return data_by_module


def _parse_data_by_position_filters(db_data, detector_prefix, position_filters, time_range=None):
    """
    Parse data for modules where each position's value is in the allowed list.
    Module format: BPix_BmI_SEC1_LAY14_LAY1_HV
    Positions:     [0]  [1]  [2]   [3]   [4]  [5]
    """
    data_by_module = defaultdict(list)
    
    for entry in db_data[1:]:  # Skip header
        module_name = entry[0]
        
        # Must start with detector prefix
        if not module_name.startswith(detector_prefix):
            continue
        
        # Split module name by underscore
        parts = module_name.split('_')
        
        # Check each position (parts[1] through parts[4])
        # parts[0] = 'BPix' or 'FPix'
        # parts[1] = pos_1 (BmI, BmO, BpI, BpO)
        # parts[2] = pos_2 (SEC1-8 or D1-3)
        # parts[3] = pos_3 (LAY14/LAY23 or ROG1-4)
        # parts[4] = pos_4 (LAY1-4 or RNG1-2)
        
        if len(parts) < 6:  # Make sure module has all parts
            continue
        
        matches = True
        
        # Check pos_1
        filters_pos1 = position_filters.get('pos_1', [])
        if filters_pos1 and parts[1] not in filters_pos1:
            matches = False
        
        # Check pos_2
        filters_pos2 = position_filters.get('pos_2', [])
        if filters_pos2 and parts[2] not in filters_pos2:
            matches = False
        
        # Check pos_3
        filters_pos3 = position_filters.get('pos_3', [])
        if filters_pos3 and parts[3] not in filters_pos3:
            matches = False
        
        # Check pos_4
        filters_pos4 = position_filters.get('pos_4', [])
        if filters_pos4 and parts[4] not in filters_pos4:
            matches = False
        
        if matches:
            date = _format_date(entry[1])
            if _is_in_time_range(date, time_range):
                current = float(entry[2])
                data_by_module[module_name].append((date, current))
    
    return data_by_module


def get_stored_dates():
    """
    Saves a .txt file of the dates stored in the csv, specifically to then go to brilcalc and get the integrated luminosity for these dates.
     
    There is some nuance to this, the current scan takes hours to finish so that data has different recorded times (hour, minute, seconds).
    but should have the same date (year, month, day). Therefore, it should be ok to take just the date (year, month, day) that the measurement is performed and neglect the time (hour, minute, second). 
    Differences in Int. Lum exposure on these time scales should have negligible effect on the leakage current due to radiation damage.
    
    Additionally, dates within 12 hours of each other are merged to the later date.
    """
    _, db_data = _load_files()
    
    # Extract all datetime objects
    all_dates = []
    for entry in db_data[1:]:  # Skip header
        date_str = entry[1]
        date_obj = _format_date(date_str)
        all_dates.append(date_obj)
    
    # Sort dates chronologically
    all_dates.sort()
    
    # Merge dates within 12 hours, keeping the later date
    merged_dates = []
    if all_dates:
        current_date = all_dates[0]
        
        for date in all_dates[1:]:
            time_diff = (date - current_date).total_seconds() / 3600  # Convert to hours
            
            if time_diff <= 12:
                # Within 12 hours, update to the later date
                current_date = date
            else:
                # More than 12 hours apart, save current and start new group
                merged_dates.append(current_date)
                current_date = date
        
        # Don't forget the last date
        merged_dates.append(current_date)
    
    # Convert to date-only format
    unique_dates = sorted(set(date.strftime('%Y-%m-%d') for date in merged_dates))
    
    # Write to file
    script_dir = Path(__file__).parent
    output_file = script_dir / "stored_dates.txt"
    
    with open(output_file, 'w') as f:
        for date in unique_dates:
            f.write(f"{date}\n")
    
    print(f"Saved {len(unique_dates)} unique dates to {output_file}")
    return output_file


def get_all_plots():
    """
    Returns a dictionary of plot configurations based on options.toml.
    Each key is a plot name, each value is the data dictionary for that plot.
    """
    options, db_data = _load_files()
    plots = {}
    
    # Get time range if specified
    time_range = options.get('time_range', None)
    
    # If run_all is True, create single plot with everything
    if options.get('run_all', False):
        data_by_module = defaultdict(list)
        for entry in db_data[1:]:
            module_name = entry[0]
            date = _format_date(entry[1])
            if _is_in_time_range(date, time_range):
                current = float(entry[2])
                data_by_module[module_name].append((date, current))
        plots['All Modules'] = data_by_module
        return plots
    
    # Plot specific modules
    if options.get('plot_specific_modules', False):
        modules = set(options.get('specific_modules', []))
        if modules:
            plots['Specific Modules'] = _parse_data_for_modules(db_data, modules, time_range)
    
    # Plot all BPix modules
    if options.get('plot_all_bpix', False):
        plots['All BPix'] = _parse_data_by_filter(db_data, 'BPix', time_range)
    
    # Plot all FPix modules
    if options.get('plot_all_fpix', False):
        plots['All FPix'] = _parse_data_by_filter(db_data, 'FPix', time_range)
    
    # Plot BPix by string filters
    if options.get('bpix_by_string_filters', False):
        bpix_filters = options.get('bpix_filters', {})
        if bpix_filters:
            filter_data = _parse_data_by_position_filters(db_data, 'BPix', bpix_filters, time_range)
            if filter_data:
                # Create descriptive name from filters
                filter_desc = []
                for pos in ['pos_1', 'pos_2', 'pos_3', 'pos_4']:
                    filters = bpix_filters.get(pos, [])
                    if filters:
                        filter_desc.append(f"{','.join(filters)}")
                filter_name = f"BPix: {' | '.join(filter_desc)}"
                plots[filter_name] = filter_data
    

    print(f"DEBUG: Checking FPix... fpix_by_string_filters = {options.get('fpix_by_string_filters')}")
    if options.get('fpix_by_string_filters', False):
        fpix_filters = options.get('fpix_filters', {})
        if fpix_filters:
            filter_data = _parse_data_by_position_filters(db_data, 'FPix', fpix_filters, time_range)
            if filter_data:
                # Create descriptive name from filters
                filter_desc = []
                for pos in ['pos_1', 'pos_2', 'pos_3', 'pos_4']:
                    filters = fpix_filters.get(pos, [])
                    if filters:
                        filter_desc.append(f"{','.join(filters)}")
                filter_name = f"FPix: {' | '.join(filter_desc)}"
                plots[filter_name] = filter_data
        
    
    return plots


def get_time_range():
    """Return the time range from options for display purposes."""
    options, _ = _load_files()
    return options.get('time_range', None)


def main():
    plots = get_all_plots()
    time_range = get_time_range()
    
    if time_range:
        print(f"Time range filter: {time_range[0]} to {time_range[1]}")
    
    for plot_name, data in plots.items():
        print(f"{plot_name}: {len(data)} modules")
    return

if __name__ == "__main__":
    main()