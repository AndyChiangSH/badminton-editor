import pandas
import json


if __name__ == "__main__":
    input_path = "experiment/questions_prompt/data/play_english.csv"
    input_df = pandas.read_csv(input_path)
    print("input_df:", input_df)
    print("len(input_df):", len(input_df))
