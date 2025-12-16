## Automating Scouting Reports for Rice Men's Basketball

This is an internal tool developed by the Rice Sport Analytics Team Technical Projects (RSATTP) team which looks to automate the generation of pre-match scouting reports for Rice MBB.

To download the libraries needed to run the program, simply run the following command in your terminal:

```         
pip install -r requirements.txt
```

### Usage

To generate a scouting report, run `run_reports.py`. From there, you will be prompted to enter three things: 

1. Opponent Name
2. Date
3. Whether to use ESPN or CBB Analytics Data.

For (3), using ESPN data relies on scraping data from the internet and calculating statistics, inputting them into the program. More traditionally, using CBB Analytics data requires downloading CSV files from CBB Analytics and inputting them into the `sample_data` directory. Currently, there is 2024 data as a sample.

### Future Work

1.  Building frontend shiny app for easier use 
    - This also helps deal with error handling with invalid inputs
2. Testing
3. Ensuring that CBBAnalytics and ESPN data give similar results

### Other Important Notes

- Due to issues with the sportsdataverse library, running this program will require you to downgrade your XGBoost version to a version prior to 3.1. For this reason, we recommend creating a virtual environment to run this program in.

- For the ESPN data, we define transitions (and therefore transition eFG and rates) as anything occuring within 8 seconds of a change of possession, this follows the definition used by [Instat](https://instatglossary.hudl.com/basketball/events/play-types/transitions/) Additionally, we define Rim Shots as any shot considered a "Dunk", "Layup" or "Putback" by ESPN's play by play data, and midranges as any shot worth two points not in those categories. For those reasons, these categories may differ from the CBBAnalytics implementation.

- For the CBBAnalytics implementation, since we do not have rim, midrange, or transition data, these missing values are simply filled in with -1 (or -100%)

- Finally, to run the program, you need access to RSATTP's internal gmail which is used to physically edit the google sheets, please contact the project maintainer for access if you are a member of RSAT.

### Development

This work was built by RSATTP during the Fall 2025 semester, with contributions from the following individuals:

- [Lou Zhou](https://lou-zhou.github.io/) *Project Maintainer, Please Contact lz80@rice.edu for questions*
- [David Coronado](https://www.linkedin.com/in/david-coronado-189642289) 
- [Russell Chen](https://www.linkedin.com/in/russell-chenn) 
- [Jude Thomas](https://www.linkedin.com/in/jude-thomas-336970316/) 


