import os
import pandas
import json
# from pipeline import preprocess, translate, generate_answer


def preprocess(df):
    """Preprocess dataframe
    
    Input: dataframe
    Output: preprocessed dataframe
    """

    for i in df:
        if i not in ['score_team', "player", 'roundscore_AB', 'roundscore_CD', 'ball_type', 'score_reason', 'lose_reason']:
            df = df.drop(columns=[i])

    for j, i in enumerate(df['score_team']):
        if i != 'AB' and i != 'CD':
            df = df.drop([j])

    df = df.reindex(columns=['score_team', "player", 'roundscore_AB',
                    'roundscore_CD', 'ball_type', 'score_reason', 'lose_reason'])

    df.rename(columns={'player': 'win_point_player'}, inplace=True)
    df.rename(columns={'score_reason': 'win_reason'}, inplace=True)
    df.rename(columns={'ball_type': 'ball_types'}, inplace=True)

    return df


def translate(input_df):
    """Translate from Chinese to English
    
    Input: dataframe
    Output: translated dataframe
    """

    ball_type_dictionary_path = "dictionary/ball_type_dictionary.json"
    with open(ball_type_dictionary_path, 'r', encoding="utf-8") as file:
        ball_type_dictionary = json.load(file)

    win_reason_dictionary_path = "dictionary/win_reason_dictionary.json"
    with open(win_reason_dictionary_path, 'r', encoding="utf-8") as file:
        win_reason_dictionary = json.load(file)

    lose_reason_dictionary_path = "dictionary/lose_reason_dictionary.json"
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

    # print("ouput_df:", ouput_df)

    return ouput_df


if __name__ == '__main__':
    game = "GOH_SOON_HUAT_LAI_SHEVON_JEMIE_YE_HONG_WEI_LEE_CHIA_HSIN_Asia_Championships_2023_Round_of_32"
    player_A = "GOH SOON HUAT"
    player_B = "LAI SHEVON JEMIE"
    player_C = "YE HONG WEI"
    player_D = "LEE CHIA HSIN"
    competition = "Asia Championships 2023 Round of 32"
    
    # QA_output = f"{competition}: {player_A}  & {player_B} v.s. {player_C} & {player_D}"
    CSV_output = f"{competition}: {player_A}  & {player_B} v.s. {player_C} & {player_D}"
    
    # Get list of filenames in the folder
    num_set = len(os.listdir(f"data/{game}/"))
    os.makedirs(f"CSV/{game}/", exist_ok=True)
    # os.makedirs(f"QA/{game}/", exist_ok=True)
    for set in range(1, num_set+1):
        filename = f"set{set}"
        
        print(f"> Read file {filename}...")
        data = pandas.read_csv(f"data/{game}/{filename}.csv")
        input_df = pandas.DataFrame(data)
        # print("input_df:", input_df)

        print(f"> Preprocess...")
        preprocessed_df = preprocess(input_df)
        # print("preprocessed_df:", preprocessed_df)
        
        print("> Translate...")
        translated_df = translate(preprocessed_df)
        # print("translated_df:", translated_df)
        
        translated_df_copy = translated_df.copy()
        translated_df_copy.replace(
            {'win_point_player': {"A": player_A, "B": player_B, "C": player_C, "D": player_D}}, inplace=True)
        
        translated_df_copy.to_csv(f"CSV/{game}/{filename}.csv", index=False)
        
        with open(f"CSV/{game}/{filename}.csv", "r") as f:
            CSV = f.read()
        
        CSV_output += f"\n\nSet {set}:\n{CSV}"
        
        print("> Generate answer...")
        # answers = generate_answer(translated_df, player_A, player_B)
        # print("answers:", answers)
        
        # QA_output += f"\n\nSet {set}:{answers}"

    # Output
    # print("Output...")
    # with open(f"QA/{game}/QA.txt", "w") as f:
    #     f.write(QA_output)
        
    with open(f"CSV/{game}/CSV.txt", "w") as f:
        f.write(CSV_output)
