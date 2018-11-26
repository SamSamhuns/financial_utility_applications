# financial-utility-programs [![Build Status](https://travis-ci.com/SamSamhuns/financial-utility-programs.svg?branch=master)](https://travis-ci.com/SamSamhuns/financial-utility-programs)

Contains a list of software utilities and programs for financial calculations.
-   ## [Discounted Cash Flow](#dcf)
Discounted Cash Flow Calculator that generates a cash flow chart with NPV from a CSV file.
   <img src='https://raw.githubusercontent.com/SamSamhuns/financial-utility-programs/master/Discounted Cash Flow/cash_flow_fig.png' width='65%' height='30%'>

-   ## [Value_Realization_Model](#vrm)
Probability modeling of binary stock value expectations from sequence of buys or sells for a stock given a trading scenario for different proportions of informed and uninformed traders.
    <img src='https://raw.githubusercontent.com/SamSamhuns/financial-utility-programs/master/Value Realization Model/fig_output/high_low_prob_output.png' width='65%' height='30%'>
    
    
-   ## [Returns and Volatilities](#rav)
   Generate annualized summaries of returns and volatilities with the moving averages of different securities with the data downloaded as CSV from Yahoo Finance. </br>
    <img src='https://raw.githubusercontent.com/SamSamhuns/financial-utility-programs/master/Return and Volatilities/security_returns.png' width='65%' height='30%'>
   
## Prerequisites
Python 3.5.0 or later.

## Installing
Virtual environment packages with `virtualenv` or `anaconda` are recommended for both Windows and Linux/BSD based systems.

### Linux/BSD

After cloning the repository, install the required python packages using pip.
```git
git clone https://github.com/SamSamhuns/financial-utility-programs
pip install -r requirements.txt
```
### Windows

Download a copy of this <a href='https://github.com/SamSamhuns/financial-utility-programs'>github repository. </a>
Two options are available after this:

-   <a href='https://www.anaconda.com/download/#macos'>`Anaconda`</a> is recommended for Windows system.
Use the following command in the anaconda prompt to install modules from requirements.txt.
`conda install --yes --file requirements.txt`

-   Install <a href='https://www.python.org/downloads/'>`python`</a> and add it to your `PATH` system variable. Then install the <a  href='https://github.com/BurntSushi/nfldb/wiki/Python-&-pip-Windows-installation'>`pip`</a> package.                The `pip install -r requirements.txt` command now be used in the command prompt.

## Running the scripts

Individual instructions for running the utility scripts are also present inside each python file. 
The instructions are equivalent for both Windows and Linux/BSD systems given that python has been added to the PATH system variable in Windows systems.

In Unix, Linux and other BSD based systems, use the following command in the bash shell to ensure python file is exeutable.
```
chmod u+x python_script.py
```

### DCF
The CSV file name must entered as the first command line argument for the DCF calculation to work.
```
python3 main_DCF.py <yearly_discount_rate> <name_of_csv_file.csv>
```
A cash_flow_fig_png file will be generated that contains the cash flow diagram.

### VRM 
<p>
The Value Realization Model uses a simple model to predict the probability of a high value or a low value for a stock given the sequence of buys(asks being lifted) or sells(bids being hit).        
The script will prompt the user to enter a sequence of buy(s)/sell(s) like `bbssbs` or `BSBSBB`. And to enter the proportion of informed traders assumed to be present in the market.
</p>

Buy/sell sequences can also be entered through a text file containing these sequences as the first command line argument to the script_name.

```
python3 main_VRM.py <OPTIONAL-buy-sell-sequence.txt>
```

### RAV
<p>
The Returns and Volatilities model takes security returns data imported from the Yahoo Finance API or downloaded from Yahoo Finance as a CSV file. The returns can be download from Yahoo Finance or the `get_return_RAV.py` script can be used to directly download the return data in CSV. 
</p>
To download the CSV returns file using a script.

```
python get_returns_RAV.py <ticker_symbol>
```

To generate a summary of the returns and volatilities with their annualized calculations.

```
python main_RAV.py returns.csv
```

The returns.csv file must be in the same format downloaded from the <a href='https://finance.yahoo.com/quote/%5EGSPC/history?p=%5EGSPC'>Yahoo Finance historical prices section.</a></br>
CSV file format `Date, Open, High, Low, Close, Adj Close, Volume`


### Built With

-   [Python 3.6](https://www.python.org/downloads/release/python-360/) - The Programming tool used

### Versioning

Version tracked directly with Git

### Authors

-   **Samridha Shrestha**

### License

This project is licensed under the Apache 2.0 License - see the [License.md](License.md) file for details

### Acknowledgments

-   Python open source libraries
-   <a href='http://people.stern.nyu.edu/jhasbrou/'>Joel Hasbrouck</a>, NYU Stern Principles of Securities Trading, FINC-UB.0049, Spring 201. 

### Contributing [![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/dwyl/esta/issues)
