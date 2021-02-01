import time
import pymongo, random, string


def update():
    client = pymongo.MongoClient(appname='Updater')

    print('update: Sleeping so we can check the txn id')

    time.sleep(60)

    print('update: Performing updates')

    while True:
        with client.start_session() as session:
            session.start_transaction(read_concern=pymongo.read_concern.ReadConcern('snapshot'))

            lswa_db = client.lswa_db
            lswa = lswa_db.lswa

            for i in range(1, 10000):
                val = random.choice(string.printable) * 1000 * 1000

                # Update the existing value for that _id.
                doc = {
                    '_id': i,
                    'contents': val,
                }

                result = lswa.replace_one({'_id': i}, doc)
                assert result.matched_count == 1
                # print('update: Updated {}'.format(i))

            session.commit_transaction()

    print('update: Finished updates')
