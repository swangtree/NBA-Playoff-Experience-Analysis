import csv

def create_finals_csvs():
    with open("./pre-1994/br_series_url.csv", "r", encoding="utf-8") as read_file:
        reader = list(csv.reader(read_file))
        for line in reader[1:]:
            if line[2] == "finals":
                with open("./pre-1994/finals_stats_paste/" + line[1] + ".csv", "w+", encoding="utf-8", newline="") as new_file:
                    writer = csv.writer(new_file)
                    # Writes year and teams
                    writer.writerow([line[0] + ": " + line[-4] + " vs. " + line[-3]])
                    print("File created: " + new_file.name)
                    
def reformat_finals_csvs(in_file, out_file):
    try:
        with open(in_file, "r", encoding="utf-8") as read_file:
            reader = csv.reader(read_file)
            with open(out_file, "w+", encoding="utf-8", newline="") as write_file:
                writer = csv.writer(write_file)
                writer.writerow(["Player ID","Player name","MP"])
                for line in reader:
                    print(line)
                    if len(line) > 0:
                        if line[0].isdigit():
                            print(line)
                            writer.writerow([line[-1],line[1],line[4]])
                            # print(out_file + str([line[-1],line[1],line[4]]))
        print("File complete: " + out_file)

    except Exception as error: 
        print(f"Error, infile: {in_file}, outfile: {out_file}", error)


if __name__ == "__main__":
    
    # Create empty finals csvs
    # create_finals_csvs()

    # Test reformat function
    # reformat_finals_csvs("./finals_stats_paste/" + "015.csv", "015.csv")

    # Reformat loop
    # for i in range(15, 451, 15):
    #     reformat_finals_csvs("./finals_stats_paste/" + f"000{i}.csv"[-7:], "./player_minutes/" + f"000{i}.csv"[-7:])

    # # file_data = input("Paste here:")
    # # print(file_data)

    # Create empty finals csvs for pre 1994
    # create_finals_csvs()

    # Reformat loop
    for i in range(15, 301):
        reformat_finals_csvs("./pre-1994/finals_stats_paste/" + f"000{i}.csv"[-7:], "./pre-1994/" + f"000{i}.csv"[-7:])
