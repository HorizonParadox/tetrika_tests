import requests
import csv
import time

API_URL = "https://ru.wikipedia.org/w/api.php"
CATEGORY = "Категория:Животные по алфавиту"
HEADERS = {
    "User-Agent": "AnimalCounterBot/1.0 (https://github.com/HorizonParadox)"
}


def get_category_members(letter):
    members = []
    cmcontinue = None
    while True:

        params = {
            "action": "query",
            "format": "json",
            "list": "categorymembers",
            "cmtitle": CATEGORY,
            "cmtype": "page",
            "cmlimit": "500",
            "cmsort": "sortkey",
            "cmstartsortkeyprefix": letter
        }

        if cmcontinue:
            params["cmcontinue"] = cmcontinue

        response = requests.get(API_URL, params=params, headers=HEADERS)
        data = response.json()

        for page in data["query"]["categorymembers"]:
            title = page["title"]

            if title.startswith(letter):
                members.append(title)
            else:
                return members

        if "continue" in data:
            cmcontinue = data["continue"]["cmcontinue"]
            time.sleep(0.5)
        else:
            break

    return members


def main():
    letter_counts = {}
    for code in range(ord('А'), ord('Я') + 1):
        letter = chr(code)
        members = get_category_members(letter)
        letter_counts[letter] = len(members)
        print(f"{letter}: {letter_counts[letter]}")

    with open("beasts.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        for letter, count in letter_counts.items():
            writer.writerow([letter, count])


if __name__ == "__main__":
    main()
