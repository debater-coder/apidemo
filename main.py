import requests

from interfaces.openai import Chat
from interfaces.swapi import cache_available, fetch_people, json_from_path, contact

print("Star Wars recruiting system\n")

if not cache_available():
    print("People database not available - downloading...")
try:
    people = fetch_people()
except requests.exceptions.RequestException:
    print("Failed to download people database - exiting...")
    exit()

min_vehicle = int(input("What is the minimum amount of vehicles driven required? (0 if you don't care) "))
min_starships = int(input("What is the minimum amount of starships flown required? (0 if you don't care) "))

people = list(
    filter(lambda person: len(person["starships"]) >= min_starships and len(person["vehicles"]) >= min_vehicle, people)
)

print("\nSuggested pilots:")
print(f"{len(people)} people meet your requirements")
print('-' * 80)

for index, person in enumerate(people):
    try:
        if len(person["species"]):
            species = json_from_path(person["species"][0])["name"]
        else:
            species = "Unknown"
    except requests.exceptions.RequestException:
        species = "Species data not available"
    print(f"[{index + 1}] {person['name']} | Contact: {contact(person)} | Species: {species}")
    print("Experience:")
    try:
        vehicles = [json_from_path(uri) for uri in person['vehicles']]
        starships = [json_from_path(uri) for uri in person['starships']]
        print(f"\tVehicles: {', '.join([vehicle['name'] for vehicle in vehicles])}")
        print(f"\tStarships: {', '.join([starship['name'] for starship in starships])}")
    except requests.exceptions.RequestException:
        print("\tExperience data not available")
    print('-' * 80)

prompt = "Enter the number of the candidate to proceed with to phone interview or type ABORT to cancel: "

while True:
    while not ((option := input(prompt)).isdigit() and 0 < (option := int(option)) <= len(people)):
        if option == "ABORT":
            exit()
    person = people[option - 1]
    if input(f"Are you sure you want to continue with a phone interview with {person['name']}? (y/n) ")[0].lower() == 'y':
        break

job = input("Enter job description: ")
print(f"\nCalling {person['name']}...")

chat = Chat("http://localhost:1234/", f"You are {person['name']} and are in a phone interview for a job of '{job}'. "
                                      f"You are from the Star Wars universe. Stay in character and answer all "
                                      f"questions as the character would. Keep your responses short, succinct and "
                                      f"professional. Do not ramble on about stories unless asked to.")

print(f"You are in a phone call with {person['name']}. All messages hereafter will be sent over the phone.")

try:
    while msg := input("> "):
        print(chat.send_message(msg))
except requests.exceptions.RequestException:
    print(f"{person['name']} hung up.")

