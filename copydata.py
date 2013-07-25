from mongokit import Connection, Document

# MongoLab configuration
MONGO_USERNAME = 'bueno'
MONGO_PASSWORD = 'Cry9Gas'
MONGO_DBNAME = 'thisweekscomics'
MONGO_HOST = 'ds031877.mongolab.com'
MONGO_PORT = 31877
LAB_URI = 'mongodb://%s:%s@%s:%s/%s' % (MONGO_USERNAME, MONGO_PASSWORD,
                                          MONGO_HOST, MONGO_PORT, MONGO_DBNAME)

# M_URI = 'mongodb://heroku:93f17e34f76c9902ad0b574509c98040@linus.mongohq.com:10002/app15098233'

lab = Connection(LAB_URI)
lab = lab[MONGO_DBNAME]

cbackup = list(lab.comics.find())
lab.comic_backup.insert(cbackup)

# mdb = Connection(M_URI)
# mdb = mdb['app15098233']

# allComics = list(mdb.comicDB.find())

# lab.comics.insert(allComics)

