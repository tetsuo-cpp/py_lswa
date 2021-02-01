import pymongo, random, string


def load():
    client = pymongo.MongoClient(appname='Loader')

    # Get a handle on the LSWA collection.
    lswa_db = client.lswa_db
    lswa = lswa_db.lswa

    print('load: Generating values')

    # Generate 1MB values.
    values = list()
    for i in range(1, 10000):
        # print('load: Generated {}'.format(i))
        val = random.choice(string.printable) * 1000 * 1000
        values.append(val)

        # Making strings like 'aaaaaa...' isn't ideal because it compresses too well.
        # This would be better but it's slow. Figure out a nice way to do this.
        # val = ''.join(random.choice(string.printable) for i in range(1000 * 1000))

    print('load: Loading values')

    # Insert 1000 docs.
    counter = 1
    for val in values:
        doc = {
            '_id': counter,
            'contents': val,
        }
        counter += 1
        lswa.insert_one(doc)

    print('load: Finished loading')
