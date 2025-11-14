# Instructions

clone the repository to whatever working area you'd like, this project is all self contained in one folder.

There are only two dependencies for simplicity, `matplotlib` and `mplcursors`. This is also written for python 3. 

If you have conda or mamba installed then simply do:

`conda create -n hv_plot_env` (replacing `conda`with mamba if thats what you have installed.)

`conda activate hv_plot_env`

`conda install matplotlib`

`conda install mplcursors`

And after that is finished installing you can run the project with just:

`python3 plotter.py`



## Configuring which modules to plot

Open the `options.toml` file and at the top you'll see many options:

```
run_all = false

plot_specific_modules = false

plot_all_bpix = false
plot_all_fpix = false

...

specific_modules = [
    "BPix_BpI_SEC3_LAY14_LAY4_HV",
    "BPix_BmO_SEC4_LAY23_LAY3_HV",
    "FPix_BmO_D1_ROG2_RNG2_HV",
    "FPix_BmO_D1_ROG3_RNG1_HV",
    'BPix_BpI_SEC1_LAY14_LAY4_HV',
    'FPix_BmI_D3_ROG4_RNG1_HV',
    ]
```

I would suggest just using the specific modules, its the most straightforward and obvious way to use the tool although at the expense of being a bit tedious. You could save a few custom setups in a text file or markdown file or something and copy paste them into the options.toml file when needed (or put them in the toml and uncomment the one you want to use that time)

### Updating this tool when new data is available

I will do my best to keep the CSV up to date, feel free to tell me if it's missing the newest data point. As of now this is the most current CSV but anytime somebody pushes new data to the TOM database I will need to pull an updated version of the CSV and push here, not the best but considering new datapoints are pushed fairly infrequently to TOM I think this is ok for now.


