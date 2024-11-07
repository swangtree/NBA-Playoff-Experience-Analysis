import requests
from bs4 import BeautifulSoup
import csv

def scrape_players(url, team1, team2, out_file):

    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    if not soup.find_all(string="404 error"):
        print("URL: " + url)
        with open("finals.txt", "w+", encoding="utf-8") as f:
            f.write((soup.prettify()))

        table = soup.find("table", id=team1)
        print(table)
        if table == None:
            print("Error: " + out_file[-7:] + team1 + ", " + team2)
            return None
        
        rows = table.find_all("tr")
        print(rows)

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

        # with open(out_file, "w+", newline="", encoding="utf-8") as f:
        #     writer = csv.writer(f)
        #     writer.writerow(["Player ID", "Player name", "MP"])
        #     writer.writerows(player_data)

def main():
    scrape_players("https://www.basketball-reference.com/playoffs/2001-nba-finals-76ers-vs-lakers.html", "LAL", "PHI", "./test.csv")

if __name__ == "__main__":
    main()