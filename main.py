import json
import os.path
import random
import requests


def contact(person):
    name = person["name"].lower().split()

    random.seed(person["name"])  # so that the same name -> same email
    provider = random.choice(["@hotmail.com", "@gmail.com", "@outlook.com"])
    number = random.randint(1, 99)
    if len(name) == 1:
        firstname = name[0]
        return f"{firstname}{number}{provider}"
    elif len(name) == 2:
        firstname, lastname = name
        if random.randint(0, 1):
            return f"{lastname[0]}{firstname}{number}{provider}"
        return f"{firstname}{lastname}{number}{provider}"

    return f"{''.join(name)}{number}{provider}"


def json_from_path(uri):
    return requests.get(uri).json()


def cache_available():
    return os.path.exists("cache.json")


def fetch_people(uri="https://swapi.dev/api/people/"):
    if cache_available():
        with open("cache.json") as cache:
            return json.load(cache)

    data = json_from_path(uri)  # we are using custom cache
    people = data['results']

    if data.get('next'):
        people += fetch_people(data['next'])

    with open("cache.json", 'w') as cache:
        json.dump(people, cache)

    return people


print("Star Wars recruiting system\n")

if not cache_available():
    print("People database not available - downloading...")
try:
    people = fetch_people()
except:
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