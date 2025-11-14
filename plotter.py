import matplotlib.pyplot as plt
import parser

def plot_currents(data_dict, title="Pixel HV Leakage Currents", time_range=None):
    """Plot currents for a single set of modules."""
    if not data_dict:
        print(f"No data to plot for: {title}")
        return
    
    fig, ax = plt.subplots(figsize=(12, 7), layout='constrained')

    for module_name, date_current_tuples in data_dict.items():
        dates, currents = zip(*date_current_tuples)
        ax.plot(dates, currents, marker='o', markersize=4, label=module_name)
    
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
    plt.xticks(rotation=45, ha='right')
    
    return fig


def main():
    """Generate all configured plots."""
    all_plots = parser.get_all_plots()
    time_range = parser.get_time_range()
    
    if not all_plots:
        print("No plots configured in options.toml")
        return
    
    print(f"Generating {len(all_plots)} plot(s)...")
    if time_range:
        print(f"Time range: {time_range[0]} to {time_range[1]}")
    
    for plot_name, data_dict in all_plots.items():
        print(f"  - {plot_name}: {len(data_dict)} modules")
        plot_currents(data_dict, title=plot_name, time_range=time_range)
    
    plt.show()  # Show all plots at once


if __name__ == "__main__":
    main()