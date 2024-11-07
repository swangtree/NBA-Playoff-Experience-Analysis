import re
import requests
from bs4 import BeautifulSoup, Comment
import csv
import time
import os

def scrape_points(url, year_series, series_ID, path_points_for):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        tables = soup.find_all("table", {"class": "teams"})
        if tables == None:
            print("Error, no table: " + url)
            return None
            
        scores = []
        winners = []
        for table in tables:
            score_row = []
            
            for row in table.find_all("td"):
                score_row.append(row.text)

            scores.append([score_row[0][5], score_row[1], 0, score_row[2]])
            scores.append([score_row[0][5], score_row[4], 1, score_row[5]])
            
            # Add to list of winners
            if int(score_row[2]) > int(score_row[5]):
                winners.append(score_row[1])
            else:
                winners.append(score_row[4])
        
        winner = max(set(winners), key=winners.count)
        loser = min(set(winners), key=winners.count)
        winner_players = []
        loser_players = []
        is_winner = True
        
        for caption in soup.find_all("caption"):
            table = caption.find_parent()
            rows = table.find_all("tr")

            # print(rows)
            for row in rows[1:]:
                cols = row.find_all("td")
                
                if cols:  # Check if cols exist
                    player_link = cols[0].find("a")
                    # print("\n player link")
                    # print(player_link)
                    if player_link:  # Check if player_link exists
                        player_url = player_link.get("href")
                        player_id = player_url.split("/")[-1].split(".")[0]
                        player_name = player_link.text
                        minutes_played = cols[4].text.strip()

                        if is_winner:
                            winner_players.append([player_id, player_name, minutes_played])
                        else:
                            loser_players.append([player_id, player_name, minutes_played])
                        
            is_winner = False

        winner_players.sort(key=lambda x: int(x[2]), reverse=True)
        winner_player_IDs = [id for id, name, minutes in winner_players]
        loser_players.sort(key=lambda x: int(x[2]), reverse=True)
        loser_player_IDs = [id for id, name, minutes in loser_players]
        # print("Winning Players: ", winner_players, winner_player_IDs)
        # print("Losing Players: ", loser_players, winner_player_IDs)
        # print(scores)

        # Write to points for file
        with open(path_points_for, "a+", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            for box_score in scores:
                if box_score[1] == winner:
                    # In format [year-series, series_ID, game#, team, points, home, starter IDs, rest IDs, opponent starter IDs, opponent rest IDs]
                    writer.writerow([year_series, series_ID, box_score[0], box_score[1], box_score[3], box_score[2], " ".join(winner_player_IDs[:5]), " ".join(winner_player_IDs[5:]), " ".join(loser_player_IDs[:5]), " ".join(loser_player_IDs[5:]), loser])
                else:
                    writer.writerow([year_series, series_ID, box_score[0], box_score[1], box_score[3], box_score[2], " ".join(loser_player_IDs[:5]), " ".join(loser_player_IDs[5:]), " ".join(winner_player_IDs[:5]), " ".join(winner_player_IDs[5:]), winner])
        print("Scraped: " + url)

    except Exception as error:
        print("Error: " + url)
        print(error)

if __name__ == "__main__":
    # scrape_points("https://www.basketball-reference.com/playoffs/2023-nba-eastern-conference-first-round-heat-vs-bucks.html","2023-1", "001", "001.csv")
    
    # Clear file
    with open("./data_analysis/scores_unformatted2.csv", "w") as f:
        f.write('')

    # Scraping points
    with open("br_series_url.csv","r", encoding="utf-8") as in_file:
        url_file = csv.reader(in_file)
        next(url_file)

        for row in url_file:
            scrape_points("https://www.basketball-reference.com" + row[3], row[0] + "-" + str((int(row[1]) - 1)%15 + 1), row[1], "./data_analysis/scores_unformatted2.csv")
            scrape_points("https://www.basketball-reference.com" + row[4], row[0] + "-" + str((int(row[1]) - 1)%15 + 1), row[1], "./data_analysis/scores_unformatted2.csv")
            time.sleep(8)
