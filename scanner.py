import random
import pymongo


def scan():
    client = pymongo.MongoClient(appname='Scanner')

    print('scan: Performing long-running scan')

    with client.start_session(causal_consistency=True) as session:
        with session.start_transaction(read_concern=pymongo.read_concern.ReadConcern('snapshot')):
            lswa_db = session.client.lswa_db
            lswa = session.client.lswa_db.lswa

            # Make it a multi-update transaction just to be sure...
            doc1 = {
                '_id': 1,
                'contents': 'a',
            }
            doc2 = {
                '_id': 2,
                'contents': 'a',
            }
            result = lswa.replace_one({'_id': 1}, doc1)
            assert result.matched_count == 1
            result = lswa.replace_one({'_id': 2}, doc2)
            assert result.matched_count == 1

            counter = 0
            while True:
                id_val = random.randint(1, 10000)
                doc = lswa.find_one({'_id': id_val})
                counter += 1
                if counter % 1000 == 0:
                    print(counter)
                # for val in lswa.find():
                #     # print('scan: Iterated {}'.format(val['contents'][0]))
                #     pass

        # session.commit_transaction()

    print('scan: Finished scanning')
