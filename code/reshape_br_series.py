"""
Using the bs_series.csv, output another csv file changing the date format, 
"""
import requests
from bs4 import BeautifulSoup
import csv
import time
import os

month_calendar = {
    "Apr" : "4",
    "May" : "5",
    "Jun" : "6",
    "Jul" : "7",
    "Aug" : "8",
    "Sep" : "9",
    "Oct" : "10",
}

def reshape_to_url():
    with open("./br_series.csv", "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        with open("./br_series_url.csv", "w+", encoding="utf-8", newline="") as out_file:
            writer = csv.writer(out_file)
            writer.writerow(["Year", "Game ID" , "Series", "URL1", "URL2", "Team1", "Team2", "Start Date", "End Date"])
            num = 1

            for row in reader:
                if row[0] == "Yr":
                    continue

                year = row[0]
                series = row[2].lower().replace("conf", "conference")
                start_date = month_calendar[row[3].split()[0]] + "/" + row[3].split()[1] + "/" + year[-2:]
                end_date = month_calendar[row[3].split()[3]] + "/" + row[3].split()[4] + "/" + year[-2:]
                team1 = row[-2].split()[0]
                team2 = row[-1].split()[0]
                url1 = "/playoffs/" + "-".join([year, "nba", series.replace(" ", "-"), row[5].split()[-2], "vs", row[8].split()[-2]]).lower() + ".html"
                print(url1)
                url2 = "/playoffs/" + "-".join([year, "nba", series.replace(" ", "-"), row[8].split()[-2], "vs", row[5].split()[-2]]).lower() + ".html"
                game_id = f"000{num}"[-3:]
                print([year, game_id, series, url1, url2, team1, team2, start_date, end_date])
                num += 1
                writer.writerow([year, game_id, series, url1, url2, team1, team2, start_date, end_date])

                print(row)

def old_reshape_to_url():
    with open("./pre-1994/old_br_series.csv", "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        with open("./pre-1994/br_series_url.csv", "w+", encoding="utf-8", newline="") as out_file:
            writer = csv.writer(out_file)
            writer.writerow(["Year", "Game ID" , "Series", "URL1", "URL2", "Team1", "Team2", "Start Date", "End Date"])
            num = 1
            next(reader)

            for row in reader:
                print(row)

                year = row[0]
                series = row[2].lower().replace("conf", "conference")
                start_date = "N/A"
                end_date = "N/A"
                team1 = "N/A"
                team2 = "N/A"
                url1 = "/playoffs/" + "-".join([year, "nba", series.replace(" ", "-"), row[5].split()[-2], "vs", row[8].split()[-2]]).lower() + ".html"
                print(url1)
                url2 = "/playoffs/" + "-".join([year, "nba", series.replace(" ", "-"), row[8].split()[-2], "vs", row[5].split()[-2]]).lower() + ".html"
                game_id = f"000{num}"[-3:]
                print([year, game_id, series, url1, url2, team1, team2, start_date, end_date])
                num += 1
                writer.writerow([year, game_id, series, url1, url2, team1, team2, start_date, end_date])

                print(row)

def scrape_players(url, team1, team2, out_file):

    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    player_data = []

    for caption in soup.find_all("caption"):
        table = caption.find_parent()
        print(caption)
        rows = table.find_all("tr")
        if table == None:
            print("Error: " + out_file[-7:] + team1 + ", " + team2)
            return None
        
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

def main():
    # old_reshape_to_url()
    
    # Scraping player minutes part 1
    with open("./pre-1994/br_series_url.csv","r", encoding="utf-8") as in_file:
        url_file = csv.reader(in_file)
        next(url_file)

        print(1)
        for row in url_file:
            print(2)
            scrape_players("https://www.basketball-reference.com" + row[3], row[-4], row[-3], "./pre-1994/" + row[1] + ".csv")
            scrape_players("https://www.basketball-reference.com" + row[4], row[-4], row[-3], "./pre-1994/" + row[1] + ".csv")
            time.sleep(8)

if __name__ == "__main__":
    main()
