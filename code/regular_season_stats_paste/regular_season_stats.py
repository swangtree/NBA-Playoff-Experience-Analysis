import csv

def create_regular_season_paste_file(year):
    with open(year + ".txt", "w+", encoding="utf-8") as f:
        f.write(year)

def reformat_to_csv(year):
    return_dict = {}
    with open("./" + year + ".txt", "r+", encoding="utf-8") as in_file:
        with open("./csvs/" + year + ".csv", "w+", encoding="utf-8", newline="") as out_file:
            writer = csv.writer(out_file)
            writer.writerow(["Year", "Points scored", "Points allowed"])
            next(in_file)

            for line in in_file:
                if line.replace(" ", "") != "\n" and line.replace(" ", "") != "\n":
                    if line.split()[-1][-1].isdigit():

                        # In format [Team, Points scored, Points allowed]
                        line_list = [" ".join(line.split()[:-7]).replace("*", "")] + line.split()[-3:-1]
                        writer.writerow(line_list)
                        return_dict[year + "-" + line_list[0]] = line_list[1:]

    # In format [Points score, Points allowed]
    return return_dict

if __name__ == "__main__":
    
    # # Create files for seasons 1994-2023
    # for year in range(1994, 2024):
    #     create_regular_season_paste_file(str(year))

    regular_season_dict = {}
    for year in range(1994, 2024):
        regular_season_dict.update(reformat_to_csv(str(year)))
    
    print(regular_season_dict)