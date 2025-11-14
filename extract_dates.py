from parser import _load_files, _format_date
from pathlib import Path

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

if __name__ == "__main__":
    get_stored_dates()