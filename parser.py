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
    
    # Plot by individual filters
    if options.get('plot_by_filters', False):
        filters = options.get('filters', {})
        for filter_name, enabled in filters.items():
            if enabled:
                filter_data = _parse_data_by_filter(db_data, filter_name, time_range)
                if filter_data:  # Only add if there's data
                    plots[f'Filter: {filter_name}'] = filter_data
    
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