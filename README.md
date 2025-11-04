# Instructions

clone the repository to whatever working area you'd like, this project is all self contained in one folder.

There is only one dependency for simplicity, `matplotlib`. This is also written for python 3. 

If you have conda or mamba installed then simply do:

`conda create -n hv_plot_env` (replacing `conda`with mamba if thats what you have installed.)

`conda activate hv_plot_env`

`conda install matplotlib`

And after that is finished installing you can run the project with just:

`python3 plotter.py`



## Configuring which modules to plot

Open the `options.toml` file and at the top you'll see:

```
specific_modules = [
    "BPix_BpI_SEC3_LAY14_LAY4_HV",
    "BPix_BmO_SEC4_LAY23_LAY3_HV",
    "FPix_BmO_D1_ROG2_RNG2_HV",
    "FPix_BmO_D1_ROG3_RNG1_HV",
    'BPix_BpI_SEC1_LAY14_LAY4_HV',
    'FPix_BmI_D3_ROG4_RNG1_HV',
    ]
```

just place in here the specific modules you'd like to be plotted. Too many modules will overwhelm the plotter so be weary not to do too many.

In the future there will be options for convenience but I figured I should post this working version ASAP so others can use it as needed. 

### Updating this tool when new data is available

I will do my best to keep the CSV up to date, feel free to tell me if its missing the newest data point. As of now this is the most current CSV but anytime somebody pushes new data to the TOM database I will need to pull an updated version of the CSV and push here, not the best but considering new datapoints are pushed fairly infrequently to TOM I think this is ok for now.

