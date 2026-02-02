from datetime import date
from pathlib import Path
#import pandas as pd
#import sportsdataverse as sdv 
from shiny import reactive
from shiny.express import input, render, ui
from run_reports import main_shiny
from sportsdataverse.mbb import espn_mbb_teams
#import run_reports.main as main


ui.page_opts(title="MBB Run Reports", full_width=True)

#Year Input
with ui.card(full_screen=False, height="auto"):
        ui.card_header("Input Date (mm/dd/yy)")
        # Date input with custom format
        ui.input_date(
            "date", "", value=date.today(), format="mm/dd/yy",
            min = "2001-11-01", max = date.today()
        )

        @render.text
        def selected_date():
            return f"Selected date: {input.date()}"

with ui.card(full_screen=False, height="auto"):
    ui.card_header("Data Source")
    ui.input_checkbox("checkbox", "Use ESPN Data?", True) 

#TODO: hide team list until date is selected
#put team list in a reactive function that updates when date is selected
# then fetch team list for that season
# potentially add d1 and d2 options
# also error handling for no internet connection
team_list = ["Loading..."]
with ui.card(full_screen=False, height="auto"):
    ui.card_header("Select Team")

    ui.input_radio_buttons(
        id="radio", 
        label="Select Division:",
        choices = {50: "Division I", 51: "Division II/III"}, 
        selected="Division I"
    )

    @reactive.Effect
    def update_team_list(): 
        division = input.radio()
        print(f"Fetching team list for division: {division}")
        data = espn_mbb_teams(groups=division, return_as_pandas=True)
        team_list = data['team_display_name'].tolist()
        ui.update_select("select", choices=team_list)
    
    ui.input_select(
    "select",
    "Select an option below:",
    team_list,
    )

    @render.text
    def teamname():
        return f"{input.select()}"


    # TODO: change checkbox so they can upload their own
    # data set from CBB analytics in the form of a CSV
    # make sure its 2 different csv
    # add tooltip for whether to use espn or CBB dump
    # most commonly use ESPN for most up to date data

with ui.card(full_screen=False, height="auto"):
    ui.input_action_button("submit_button", "Generate Report", class_="btn-primary")
@render.text
@reactive.event(input.submit_button)
def report():
    try:
        result = main_shiny(
            team_name=input.select(),
            date=input.date(),
            uses_espn=input.checkbox()
        )
        return result
    except Exception as e:
        return f"Error generating report: {str(e)}"