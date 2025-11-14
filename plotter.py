import matplotlib.pyplot as plt
import mplcursors
import parser
from datetime import datetime

def load_luminosity_data():
    """Load the cumulative luminosity data from CSV."""
    try:
        lumi_dict = {}
        with open('lumi.csv', 'r') as f:
            lines = f.readlines()[1:]  # Skip header
            for line in lines:
                parts = line.strip().split(',')
                date_str = parts[0]
                cumulative_recorded = float(parts[3])  # cumulative_recorded_fb column
                date = datetime.strptime(date_str, '%Y-%m-%d')
                lumi_dict[date.date()] = cumulative_recorded
        return lumi_dict
    except FileNotFoundError:
        print("Warning: lumi.csv not found. Plotting without luminosity data.")
        return None


def get_cumulative_lumi_at_date(date, lumi_dict):
    """Get cumulative luminosity at a specific date."""
    if lumi_dict is None:
        return None
    
    # Convert datetime to date if necessary
    if isinstance(date, datetime):
        date = date.date()
    
    # Find the cumulative luminosity up to this date
    valid_dates = [d for d in lumi_dict.keys() if d <= date]
    if valid_dates:
        latest_date = max(valid_dates)
        return lumi_dict[latest_date]
    return 0.0


def plot_currents_vs_date(data_dict, title="Pixel HV Leakage Currents", time_range=None):
    """Plot currents vs date."""
    if not data_dict:
        print(f"No data to plot for: {title}")
        return
    
    fig, ax = plt.subplots(figsize=(12, 7), layout='constrained')

    lines = []
    labels = []
    
    for module_name, date_current_tuples in data_dict.items():
        dates, currents = zip(*date_current_tuples)
        line, = ax.plot(dates, currents, marker='o', markersize=4, label=module_name)
        lines.append(line)
        labels.append(module_name)
    
    ax.set_ylabel("HV Leakage Current (μA)", fontsize=14)
    ax.set_xlabel("Date", fontsize=14)
    
    # Add time range info to title if specified
    if time_range:
        title = f"{title}\n({time_range[0]} to {time_range[1]})"
    
    ax.set_title(title, fontsize=16, fontweight='bold')
    
    # Only show legend if not too many modules
    if len(data_dict) <= 15:
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
    else:
        ax.text(0.02, 0.98, f'{len(data_dict)} modules plotted', 
                transform=ax.transAxes, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    # Add interactive hover
    cursor = mplcursors.cursor(lines, hover=True)
    cursor.connect("add", lambda sel: sel.annotation.set_text(
        f"{labels[lines.index(sel.artist)]}\n"
        f"Current: {sel.target[1]:.3f} μA"
    ))
    
    return fig


def plot_currents_vs_luminosity(data_dict, lumi_dict, title="Leakage Current vs Integrated Luminosity"):
    """Plot current vs cumulative recorded luminosity."""
    if not data_dict or lumi_dict is None:
        print(f"Cannot create luminosity correlation plot: missing data")
        return
    
    fig, ax = plt.subplots(figsize=(12, 7), layout='constrained')
    
    lines = []
    labels = []
    
    for module_name, date_current_tuples in data_dict.items():
        dates, currents = zip(*date_current_tuples)
        
        # Get cumulative luminosity for each measurement
        lumi_values = [get_cumulative_lumi_at_date(date, lumi_dict) for date in dates]
        
        # Filter out None values
        valid_data = [(l, c) for l, c in zip(lumi_values, currents) if l is not None]
        if valid_data:
            lumi_vals, curr_vals = zip(*valid_data)
            line, = ax.plot(lumi_vals, curr_vals, marker='o', markersize=4, label=module_name)
            lines.append(line)
            labels.append(module_name)
    
    ax.set_xlabel("Cumulative Recorded Integrated Luminosity (fb⁻¹)", fontsize=14)
    ax.set_ylabel("HV Leakage Current (μA)", fontsize=14)
    ax.set_title(title, fontsize=16, fontweight='bold')
    
    # Only show legend if not too many modules
    if len(data_dict) <= 15:
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
    else:
        ax.text(0.02, 0.98, f'{len(data_dict)} modules plotted', 
                transform=ax.transAxes, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
    
    # Add interactive hover
    cursor = mplcursors.cursor(lines, hover=True)
    cursor.connect("add", lambda sel: sel.annotation.set_text(
        f"{labels[lines.index(sel.artist)]}\n"
        f"Luminosity: {sel.target[0]:.2f} fb⁻¹\n"
        f"Current: {sel.target[1]:.3f} μA"
    ))
    
    return fig


def main():
    """Generate all configured plots."""
    all_plots = parser.get_all_plots()
    time_range = parser.get_time_range()
    lumi_dict = load_luminosity_data()
    
    if not all_plots:
        print("No plots configured in options.toml")
        return
    
    print(f"Generating {len(all_plots)} plot(s)...")
    if time_range:
        print(f"Time range: {time_range[0]} to {time_range[1]}")
    
    if lumi_dict is not None:
        print(f"Luminosity data loaded: {len(lumi_dict)} dates")
        max_lumi = max(lumi_dict.values())
        print(f"Cumulative luminosity range: 0 to {max_lumi:.2f} fb⁻¹")
    
    for plot_name, data_dict in all_plots.items():
        print(f"  - {plot_name}: {len(data_dict)} modules")
        
        # Plot 1: Current vs Date
        plot_currents_vs_date(data_dict, title=f"{plot_name} vs Date", time_range=time_range)
        plt.show()
        plt.close()
        
        # Plot 2: Current vs Integrated Luminosity
        if lumi_dict is not None:
            plot_currents_vs_luminosity(data_dict, lumi_dict, 
                                       title=f"{plot_name} vs Integrated Luminosity")
            plt.show()
            plt.close()
        else:
            print(f"  Skipping luminosity plot for {plot_name} (no luminosity data)")


if __name__ == "__main__":
    main()