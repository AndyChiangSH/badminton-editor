import pandas
import json

id = 3

if __name__ == "__main__":
    input_path = f"questions_prompt/data/game{id}.csv"
    input_df = pandas.read_csv(input_path)
    print("input_df:", input_df)
    
    ball_type_dictionary_path = "questions_prompt/data/ball_type_dictionary.json"
    with open(ball_type_dictionary_path, 'r', encoding="utf-8") as file:
        ball_type_dictionary = json.load(file)
        
    win_reason_dictionary_path = "questions_prompt/data/win_reason_dictionary.json"
    with open(win_reason_dictionary_path, 'r', encoding="utf-8") as file:
        win_reason_dictionary = json.load(file)
        
    lose_reason_dictionary_path = "questions_prompt/data/lose_reason_dictionary.json"
    with open(lose_reason_dictionary_path, 'r', encoding="utf-8") as file:
        lose_reason_dictionary = json.load(file)
    
    ouput_df = input_df

    for index in input_df.index:
        try:
            ouput_df["ball_types"][index] = ball_type_dictionary[input_df["ball_types"][index]]
        except:
            ouput_df["ball_types"][index] = "unknown"
            
        try:
            ouput_df["win_reason"][index] = win_reason_dictionary[input_df["win_reason"][index]]
        except:
            ouput_df["win_reason"][index] = "unknown"
  
        try:
            ouput_df["lose_reason"][index] = lose_reason_dictionary[input_df["lose_reason"][index]]
        except:
            ouput_df["lose_reason"][index] = "unknown"

    print("ouput_df:", ouput_df)

    output_path = f"questions_prompt/data/game{id}_english.csv"
    ouput_df.to_csv(output_path)
