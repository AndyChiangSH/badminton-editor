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
        if i not in ['score_team', 'roundscore_AB', 'roundscore_CD', "fault_player", 'ball_type', "score_reason"]:
            df = df.drop(columns=[i])

    df = df.reindex(columns=['score_team', 'roundscore_AB','roundscore_CD', "fault_player", 'ball_type', "score_reason"])
    
    print(df.shape)
    
    for i, value in enumerate(df['ball_type']):
        if value != '死球':
            pre_ball_type = value
            df = df.drop([i])
        else:
            print("pre_ball_type:", pre_ball_type)
            df['ball_type'][i] = pre_ball_type
    
    # new_df = pandas.DataFrame(columns=['score_team', 'roundscore_AB','roundscore_CD', "fault_player", 'ball_type', "score_reason"])
    # for i in range(len(df)):
    #     if df.iloc[i, 0] == "AB" or df.iloc[i, 0] == "CD":
    #         new_row = df.iloc[i]
    #         new_row["ball_type"] = df.iloc[i-1, 4]
    #         new_df += new_row
    
    # df.rename(columns={'player': 'win_point_player'}, inplace=True)
    # df.rename(columns={'ball_type': 'ball_types'}, inplace=True)
    # df.rename(columns={'score_reason': 'win_reason'}, inplace=True)

    return df


if __name__ == '__main__':
    game = "PUAVARANUKROH_TAERATTANACHAI_YE_LEE_YONEX_SUNRISE_India_Open_2024_Semifinals"
    player_A = "Dechapol Puavaranukroh"
    player_B = "Sapsiree Taerattanachai"
    player_C = "葉宏蔚"
    player_D = "李佳馨"
    competition = "India Open 2024 Semifinals"
    
    # QA_output = f"{competition}: {player_A}  & {player_B} v.s. {player_C} & {player_D}"
    # CSV_output = f"{competition}: {player_A}  & {player_B} v.s. {player_C} & {player_D}"
    
    # Get list of filenames in the folder
    num_set = len(os.listdir(f"data/{game}/"))
    os.makedirs(f"post/{game}/", exist_ok=True)
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
        
        # print("> Translate...")
        # translated_df = translate(preprocessed_df)
        # print("translated_df:", translated_df)
        
        # translated_df_copy = translated_df.copy()
        # translated_df_copy.replace(
        #     {'win_point_player': {"A": player_A, "B": player_B, "C": player_C, "D": player_D}}, inplace=True)
        
        preprocessed_df.to_csv(f"post/{game}/{filename}.csv", index=False)
        
        # with open(f"CSV/{game}/{filename}.csv", "r") as f:
        #     CSV = f.read()
        
        # CSV_output += f"\n\nSet {set}:\n{CSV}"
        
        # print("> Generate answer...")
        # answers = generate_answer(translated_df, player_A, player_B)
        # print("answers:", answers)
        
        # QA_output += f"\n\nSet {set}:{answers}"

    # Output
    # print("Output...")
    # with open(f"QA/{game}/QA.txt", "w") as f:
    #     f.write(QA_output)
        
    # with open(f"CSV/{game}/CSV.txt", "w") as f:
    #     f.write(CSV_output)
