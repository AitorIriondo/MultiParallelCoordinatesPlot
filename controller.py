import pandas as pd

class Controller:
    df = []
    elementNames = []
    elementMin = []
    elementMax = []
    normValues = []
    normalized_df = []
    def __init__(self, df):
        self.df = df
        self.elementNames = self.df.columns.to_numpy()

        self.elementMin = self.df.min().to_numpy()

        self.elementMax = self.df.max().to_numpy()

        self.normalized_df = (self.df - self.df.min()) / (self.df.max() - self.df.min())