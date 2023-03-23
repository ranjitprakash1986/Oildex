# Oildex

> Author: Ranjit Sundaramurthi
>
> Project completed in accordance with DSCI 532 for the UBC MDS Program 2022-23

### Usage

The objective of this dashboard is to enable an executive or any investor interested in Schlumberger (SLB) to get an immediate overview of the Oil market within a specific selected year range. It also enables to compare the Oil prices with the SLB and the S&P 500 stock prices. Please see this detailed [proposal](docs/proposal.md) for more information on the motivation and description of the data.  

The Dashboard page presents the user with widgets to select the year range of interest between 1986 - 2022 at the top. The selected year range filters the lineplots which reveal the trends in Oil price movement with changes in the drilling activity represented by Rig Count. The next line plot compares the trend of Oil price with SLB stock price. Due to the varying scales of prices, a third plot shows the normalized prices of Oil, SLB stock, S&P500 stock index. This enables the user to see the changes in trend on an even scale.

The bottom half of the Dashboard shows a stacked barplot with the Rig Counts. These can be visualized by different regions of interest. Please note that the regions selected only affect the stacked barplot and  do not affect the lineplots.

The latest version of the dashboard is deployed on Render [here](https://oildex-dash.onrender.com)

### Running locally

<!-- #region -->
Please follow the following instruction to run the Dashboard locally
Clone the repository using

```bash
git clone https://github.com/ranjitprakash1986/Oildex
```
<!-- #endregion -->

<!-- #region -->
Add the dependencies using the following

```bash
pip install -r src/requirements.txt`
```
<!-- #endregion -->

<!-- #region -->
Ensure you are in the `src/` folder. Then run the Dashboard from the terminal using the following:

```bash
python app.py
```
<!-- #endregion -->

### References

The data for this Dashboard is pulled from four sources

* [Oil Price]("https://www.eia.gov/dnav/pet/PET_PRI_SPT_S1_D.htm")
* [S&P 500 Price]("https://ca.investing.com/indices/us-spx-500-historical-data")
* [SLB Price]("https://ca.investing.com/equities/schlumberger-ltd-historical-data")
* [Rig Count]("https://rigcount.bakerhughes.com/intl-rig-count")

The code for cleaning and coercing the data for the visualization can be found [here](https://github.com/ranjitprakash1986/Oildex/blob/main/src/code.ipynb)

The software and associated documentation files are licensed under the MIT License. You may find a copy of the license at [LICENSE](https://github.com/ranjitprakash1986/Oildex/blob/main/LICENSE).

```python

```
