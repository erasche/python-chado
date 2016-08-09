from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import mapper, sessionmaker

class Analysis(object):
    pass

class Organism(object):
    pass

class Dbxref(object):
    pass

class Cvterm(object):
    pass

class Db(object):
    pass

class Cv(object):
    pass

def ChadoAuth(parser):
    parser.add_argument('-h', '--dbhost', required=True, help='Database Host')
    parser.add_argument('-n', '--dbname', required=True, help='Database Name')
    parser.add_argument('-u', '--dbuser', help='Database Username')
    parser.add_argument('-p', '--dbpass', help='Database Password')
    parser.add_argument('--dbschema', help='Database Schema (default: public)', default="public")
    parser.add_argument("-d", "--debug", help="Print debug information", action="store_true")

class ChadoInstance(object):

    def __init__(self, dbhost, dbname, dbuser, dbpass, dbschema):
        self.dbhost = dbhost
        self.dbname = dbname
        self.dbuser = dbuser
        self.dbpass = dbpass
        self.dbschema = dbschema

        self.debug = debug

        self.jobs = JobsClient(self)

    def __str__(self):
        return '<ChadoInstance at %s>' % self.dbhost

    def connect(self):

        self._engine = create_engine('postgresql://%s:%s@%s/%s' % (self.dbuser, self.dbpass, self.dbhost, self.dbname), echo=self.debug)
        self._metadata = MetaData(engine)

        Session = sessionmaker(bind=engine)
        self.session = Session()

        self._test_db_access()

        self._reflect_tables()

    def _test_db_access(self):
        tables = self._engine.table_names()
        if ('analysis' not in tables or 'feature' not in tables):
            raise Exception("Could not find Chado tables in db %s" % (self._engine.url))

    def _reflect_tables(self):

        # Try to reflect tables
        analysis = Table('analysis', self._metadata, autoload=True)
        mapper(Analysis, analysis)
        organism = Table('organism', self._metadata, autoload=True)
        mapper(Organism, organism)
        dbxref = Table('dbxref', self._metadata, autoload=True)
        mapper(Dbxref, dbxref)
        cvterm = Table('cvterm', self._metadata, autoload=True)
        mapper(Cvterm, cvterm)
        db = Table('db', self._metadata, autoload=True)
        mapper(Db, db)
        cv = Table('cv', self._metadata, autoload=True)
        mapper(Cv, cv)