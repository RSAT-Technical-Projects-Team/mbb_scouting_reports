""" Functions which generate "The Who" part of the mbb scouting report """
import pandas as pd

def generate_data():
    """dummy function"""
    return pd.read_csv("sample_data/D1_TeamFourFact.csv")

print(generate_data())
