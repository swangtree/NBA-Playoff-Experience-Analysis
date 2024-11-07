import requests
from bs4 import BeautifulSoup, Comment
import csv
import time
import os

def scrape_players(url, team1, team2, out_file):

    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    if not soup.find_all(string="404 error"):
        print("URL: " + url)
        table = soup.find("table", {"class": "sortable stats_table"}, id=team1)
        if table == None:
            print("Error: " + out_file[-7:] + team1 + ", " + team2)
            return None
        
        rows = table.find_all("tr")

        # print(rows)
        player_data = []

        for row in rows[1:]:
            cols = row.find_all("td")
            
            if cols:  # Check if cols exist
                player_link = cols[0].find("a")
                # print("\n player link")
                # print(player_link)
                if player_link:  # Check if player_link exists
                    url = player_link.get("href")
                    player_id = url.split("/")[-1].split(".")[0]
                    player_name = player_link.text
                    
                    minutes_played = cols[4].text.strip()
                    player_data.append([player_id, player_name, minutes_played])

        table = soup.find("table", id=team2)

        rows = table.find_all("tr")

        # print(rows)
        for row in rows[1:]:
            cols = row.find_all("td")
            
            if cols:  # Check if cols exist
                player_link = cols[0].find("a")
                # print("\n player link")
                # print(player_link)
                if player_link:  # Check if player_link exists
                    url = player_link.get("href")
                    player_id = url.split("/")[-1].split(".")[0]
                    player_name = player_link.text
                    minutes_played = cols[4].text.strip()
                    player_data.append([player_id, player_name, minutes_played])

        with open(out_file, "w+", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Player ID", "Player name", "MP"])
            writer.writerows(player_data)

def check_player_minutes(url_list_path, player_minutes_path, series_count):
    return_list = []
    missing_list = []
    with open(url_list_path, "r", encoding="utf-8") as f1:
        url_list = list(csv.reader(f1))

        for i in range(1, series_count + 1):
            if not os.path.isfile(player_minutes_path + "/" + f"000{i}.csv"[-7:]):
                print(player_minutes_path + "/" + f"000{i}.csv"[-7:])
                return_list.append(url_list[i])
                missing_list.append(i)
    
    return missing_list, return_list

def tally_file(file_path, index_list):
    return_dict = {}
    with open(file_path, "r", encoding="utf-8") as f:
        reader = list(csv.reader(f))[1:]

        for index in index_list:
            for line in reader:
                if line[index] in return_dict:
                    return_dict[line[index]] += 1
                else:
                    return_dict[line[index]] = 1
        
        return return_dict

def main():

    # Scraping player minutes part 1
    with open("br_series_url.csv","r", encoding="utf-8") as in_file:
        url_file = csv.reader(in_file)
        next(url_file)

        for row in url_file:
            scrape_players("https://www.basketball-reference.com" + row[3], row[-4], row[-3], "./player_minutes/" + row[1] + ".csv")
            scrape_players("https://www.basketball-reference.com" + row[4], row[-4], row[-3], "./player_minutes/" + row[1] + ".csv")
            time.sleep(8)

    # # Checking missed series
    # missing_list, missing_url_list = check_player_minutes("./br_series_url.csv", "./player_minutes", 450)
    # with open("./missing_br_series_url.csv", "w+", encoding="utf-8", newline="") as f:
    #     writer = csv.writer(f)
    #     writer.writerow(["Year", "Game ID" , "Series", "URL1", "URL2", "Team1", "Team2", "Start Date", "End Date"])
    #     for line in missing_url_list:
    #         writer.writerow(line)

    # # Tallying missed series statistics

    # print(missing_list)
    # print(tally_file("./missing_br_series_url.csv", [2, -3, -4]))
    # print(tally_file("./br_series_url.csv", [2, -3, -4]))

    # # Fix missed series URLs
    # # Fix Trail Blazers URLs
    # with open("./missing_br_series_url.csv", "r", encoding="utf-8") as f:
    #     reader = csv.reader(f)
    #     old_url_list = list(reader)

    # with open("./fixed_br_series_url.csv", "w+", encoding="utf-8", newline="") as f:
    #     writer = csv.writer(f)
    #     for line in old_url_list:
    #         for i in range(len(line)):
    #             line[i] = line[i].replace("blazers","trail-blazers")
    #         writer.writerow(line)

    # # Scraping part 2
    # with open("fixed_br_series_url.csv","r", encoding="utf-8") as in_file:
    #     url_file = csv.reader(in_file)
    #     next(url_file)
        
    #     for row in url_file:
    #         if int(row[1]) <= 345 or int(row[1]) >= 3360:
    #              continue
            
    #         # Tries both URLs, one will work
    #         scrape_players("https://www.basketball-reference.com" + row[3], row[-4], row[-3], "./player_minutes/" + row[1] + ".csv")
    #         scrape_players("https://www.basketball-reference.com" + row[4], row[-4], row[-3], "./player_minutes/" + row[1] + ".csv")
    #         time.sleep(8)

    # # Check Trail Blazers
    # missing_list, missing_url_list = check_player_minutes("./br_series_url.csv", "./player_minutes", 450)
    # with open("./missing_br_series_url.csv", "w+", encoding="utf-8", newline="") as f:
    #     writer = csv.writer(f)
    #     writer.writerow(["Year", "Game ID" , "Series", "URL1", "URL2", "Team1", "Team2", "Start Date", "End Date"])
    #     for line in missing_url_list:
    #         writer.writerow(line)

    # # Tallying missed series statistics

    # print(missing_list)
    # print(tally_file("./missing_br_series_url.csv", [2, -3, -4]))
    # print(tally_file("./br_series_url.csv", [2, -3, -4]))

    # Checking missing series second time
    # missing_list, missing_url_list = check_player_minutes("./br_series_url.csv", "./player_minutes", 450)
    # with open("./missing_br_series_url.csv", "w+", encoding="utf-8", newline="") as f:
    #     writer = csv.writer(f)
    #     writer.writerow(["Year", "Game ID" , "Series", "URL1", "URL2", "Team1", "Team2", "Start Date", "End Date"])
    #     for line in missing_url_list:
    #         writer.writerow(line)

    # # Tallying missed series statistics
    # print(missing_list)
    # print(tally_file("./missing_br_series_url.csv", [2, -3, -4]))
    # print(tally_file("./br_series_url.csv", [2, -3, -4]))

    # Scraping player minutes part 3
    with open("br_series_url.csv","r", encoding="utf-8") as in_file:
        url_file = csv.reader(in_file)
        next(url_file)

        for row in url_file:
            if int(row[1]) <= 351 or int(row[1]) >= 3360:
                continue
            scrape_players("https://www.basketball-reference.com" + row[3], row[-4], row[-3], "./player_minutes/" + row[1] + ".csv")
            scrape_players("https://www.basketball-reference.com" + row[4], row[-4], row[-3], "./player_minutes/" + row[1] + ".csv")
            time.sleep(8)

if __name__ == "__main__":
    main()