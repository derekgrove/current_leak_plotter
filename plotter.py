import matplotlib.pyplot as plt
import parser

def plot_currents(data_dict):

    fig, ax = plt.subplots(figsize=(10, 6), layout='constrained')

    for module_name, date_current_tuples in data_dict.items():
        dates, currents = zip(*date_current_tuples)
        ax.plot(dates, currents, marker='o', label=module_name)  # 'o' adds circular points
    
    ax.set_ylabel("HV Leakage Current (μA?)", fontsize=20)
    ax.set_xlabel("Date", fontsize=20)
    #ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    

    ax.grid(True, alpha=0.5, linestyle='--', linewidth=0.5)

    plt.xticks(rotation=45, ha='right')
    plt.show()


def main():
    #print("starting main... ")
    plot_currents(parser._parse_data())
    return

if __name__ == "__main__":
    main()