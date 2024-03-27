import requests

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
    print(f"[{index + 1}] {person['name']} | Contact: {contact(person)}")
    print("Experience:")
    try:
        vehicles = [json_from_path(uri) for uri in person['vehicles']]
        starships = [json_from_path(uri) for uri in person['starships']]
        print(f"\tVehicles: {', '.join([vehicle['name'] for vehicle in vehicles])}")
        print(f"\tStarships: {', '.join([starship['name'] for starship in starships])}")
    except:
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

print(f"\nCalling {person['name']}...")