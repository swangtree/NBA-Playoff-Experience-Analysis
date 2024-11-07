import csv
import os

def main():
    
    # Year loop to make player minutes dictionary
    player_minutes_dict = {}
    output_years = [i for i in range(1994, 2024)]

    # Open score file and output regression file
    with open("./data_analysis/scores_unformatted2.csv", "r", encoding="utf=8", newline="") as scores_unformatted:
        with open("./data_analysis/scores_formatted2.csv", "w+", encoding="utf-8", newline="") as score_file:

            writer = csv.writer(score_file)
            writer.writerow(["score", "series_ID", "starters_playoff_exp_dif", "bench_playoff_exp_dif", "at_home", "team", "reg_season_points", "opp_reg_season_pa", "year", "starters_playoff_exp_quartile", "total_playoff_exp_quartile"])
            scores_list = list(csv.reader(scores_unformatted))

            # Add pre 1994 playoff minutes here
            player_minutes_dict = pre_1994_minutes("./pre-1994/")

            # Lists to find quartiles
            starters_exp_list = []
            total_exp_list = []

            for year in range(1994, 2024):
                
                game_id_start = (2023 - year) * 15 + 1
                game_id_end = (2024 - year) * 15 + 1

                for id in range(game_id_start, game_id_end):
                    if year in output_years:

                        for score_row in scores_list:
                            if score_row[0][:4] == str(year):
                                # Doesn't work right now with finals
                                if int(score_row[1]) == id and id % 15 != 0:
                                    starters_exp_list.extend([check_minutes(score_row[6], player_minutes_dict) - check_minutes(score_row[8], player_minutes_dict), check_minutes(score_row[8], player_minutes_dict) - check_minutes(score_row[6], player_minutes_dict)])
                                    total_exp_list.extend([check_minutes(score_row[6], player_minutes_dict) - check_minutes(score_row[8], player_minutes_dict) + check_minutes(score_row[7], player_minutes_dict) - check_minutes(score_row[9], player_minutes_dict), check_minutes(score_row[8], player_minutes_dict) - check_minutes(score_row[6], player_minutes_dict) +  check_minutes(score_row[9], player_minutes_dict) - check_minutes(score_row[7], player_minutes_dict)])
                            

                    # Update player mins after series
                    with open("./player_minutes/" + f"000{id}"[-3:] + ".csv", "r+", encoding="utf-8") as player_mins_file:
                        reader = csv.reader(player_mins_file)
                        for row in list(reader)[1:]:
                            if row[0] not in player_minutes_dict:
                                player_minutes_dict[row[0]] = int(row[2])
                            else: 
                                player_minutes_dict[row[0]] += int(row[2])

            starters_exp_list.sort()
            total_exp_list.sort()

            # Troubleshoot
            # print(starters_exp_list, len(starters_exp_list))

            # Troubleshoot
            # print(len(total_exp_list), len(starters_exp_list))
            print(len(starters_exp_list))
            # print(series_IDs)
            # print([i for i in range(1,451) if i not in series_IDs])
            
            starters_q1 = (starters_exp_list[(len(starters_exp_list) - 1) // 4] + starters_exp_list[(len(starters_exp_list)) // 4]) // 2
            starters_q3 = -starters_q1

            total_q1 = (total_exp_list[(len(total_exp_list) - 1) // 4] + total_exp_list[(len(total_exp_list)) // 4]) // 2
            total_q3 = -total_q1

            print("Check player minutes of Lebron: ", player_minutes_dict["jamesle01"])

            player_minutes_dict = pre_1994_minutes("./pre-1994/")
            for year in range(1994, 2024):
                
                game_id_start = (2023 - year) * 15 + 1
                game_id_end = (2024 - year) * 15 + 1

                for id in range(game_id_start, game_id_end):
                    id_count = 0
                    if year in output_years:

                        for score_row in scores_list:
                            if score_row[0][:4] == str(year):

                                # Doesn't work right now with finals
                                if int(score_row[1]) == id and id % 15 != 0:
                                    id_count += 1

                                    # Starter and Total exp quartiles assigment
                                    if check_minutes(score_row[6], player_minutes_dict) - check_minutes(score_row[8], player_minutes_dict) < starters_q1:
                                        starter_cat = 1
                                    elif check_minutes(score_row[6], player_minutes_dict) - check_minutes(score_row[8], player_minutes_dict) < 0:
                                        starter_cat = 2
                                    elif check_minutes(score_row[6], player_minutes_dict) - check_minutes(score_row[8], player_minutes_dict) < starters_q3:
                                        starter_cat = 3
                                    else:
                                        starter_cat = 4

                                    if check_minutes(score_row[6], player_minutes_dict) - check_minutes(score_row[8], player_minutes_dict) + check_minutes(score_row[7], player_minutes_dict) - check_minutes(score_row[9], player_minutes_dict) < total_q1:
                                        total_cat = 1
                                    elif check_minutes(score_row[6], player_minutes_dict) - check_minutes(score_row[8], player_minutes_dict) + check_minutes(score_row[7], player_minutes_dict) - check_minutes(score_row[9], player_minutes_dict) < 0:
                                        total_cat = 2
                                    elif check_minutes(score_row[6], player_minutes_dict) - check_minutes(score_row[8], player_minutes_dict) + check_minutes(score_row[7], player_minutes_dict) - check_minutes(score_row[9], player_minutes_dict) < total_q3:
                                        total_cat = 3
                                    else:
                                        total_cat = 4

                                    # Add the row in form [score, series_ID, starters_playoff_exp_differential, bench_playoff_exp_differential, at_home, Team, reg_season_points, opp_reg_season_points_allowed]
                                    writer.writerow([score_row[4], score_row[1], check_minutes(score_row[6], player_minutes_dict) - check_minutes(score_row[8], player_minutes_dict), check_minutes(score_row[7], player_minutes_dict) - check_minutes(score_row[9], player_minutes_dict), score_row[5], score_row[3], regular_season(year, score_row[3]), regular_season(year, score_row[-1], True), year, starter_cat, total_cat])
                    if id_count % 2 != 0: print(id)
                    # Update player mins after series
                    with open("./player_minutes/" + f"000{id}"[-3:] + ".csv", "r+", encoding="utf-8") as player_mins_file:
                        reader = csv.reader(player_mins_file)
                        for row in list(reader)[1:]:
                            if row[0] not in player_minutes_dict:
                                player_minutes_dict[row[0]] = int(row[2])
                            else: 
                                player_minutes_dict[row[0]] += int(row[2])

    print("Check player minutes of Lebron: ", player_minutes_dict["jamesle01"])
    print("Check player minutes of Olajuwon: ", player_minutes_dict["olajuha01"])
    print("Check player minutes of Baron Davis: ", player_minutes_dict["davisba01"])


def check_minutes(players_string, player_mins_dict):
    return_minutes = 0
    players_list = players_string.split()

    for player in players_list:
        if player in player_mins_dict:
            return_minutes += player_mins_dict[player]

    return return_minutes

def pre_1994_minutes(folder_path):

    player_minutes_dict = {}
    for id in range (1, 1000):
        if os.path.isfile(folder_path + f"000{id}"[-3:] + ".csv"):
            with open(folder_path + f"000{id}"[-3:] + ".csv", "r+", encoding="utf-8") as player_mins_file:
                        reader = csv.reader(player_mins_file)

                        for row in list(reader)[1:]:
                            if row[0] not in player_minutes_dict:
                                player_minutes_dict[row[0]] = int("0" + row[2])
                            else: 
                                player_minutes_dict[row[0]] += int("0" + row[2])

    return player_minutes_dict

def regular_season(year, team, is_opp = False):
    if is_opp:
        with open("./regular_season_stats_paste/" + str(year) + ".txt", "r+", encoding="utf-8") as f:
            for line in list(f):
                if len(line.split()) > 1:
                    if " ".join(line.split()[:-7]).replace("*", "") == team:
                        return line.split()[-2]
                    
    else:
        with open("./regular_season_stats_paste/" + str(year) + ".txt", "r+", encoding="utf-8") as f:
            for line in list(f):
                if len(line.split()) > 1:
                    if " ".join(line.split()[:-7]).replace("*", "") == team:
                        return line.split()[-3]

if __name__ == "__main__":
    main()