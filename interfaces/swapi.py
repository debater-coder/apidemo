
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

