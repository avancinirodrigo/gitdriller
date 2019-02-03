from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import engine
from sqlalchemy_utils import database_exists, create_database, drop_database
#from sqlalchemy.schema import DropTable
#from sqlalchemy.ext.compiler import compiles

#@compiles(DropTable, "postgresql")
#def _compile_drop_table(element, compiler, **kwargs):
#	return compiler.visit_drop_table(element) + ' CASCADE'

class SQLAlchemyEngine:
	_instance = None

	def __new__(cls):
		if cls._instance is None:
			cls._instance = object.__new__(cls)

		return cls._instance

	def create_engine(self, url):
		self.engine = create_engine(url)
		self.session = sessionmaker(bind=self.engine)
		
	def create_all_tables(self):
		Base.metadata.create_all(self.engine)

	def create_all(self, url, overwrite):
		self.createdb(url, overwrite)
		self.create_engine(url)
		self.create_all_tables()		
		
	def create_session(self):
		return self.session()

	def createdb(self, url, overwrite):
		if database_exists(url):
			if overwrite:
				drop_database(url)
				create_database(url)
			else:
				url = engine.url.make_url(url)
				raise Exception('Database \'{}\' already exists.'.format(url.database))
		else:
			create_database(url)

	def existsdb(self, url):
		return database_exists(url)

	def dropdb(self, url):
		drop_database(url)

	def drop_all(self, url):
		Base.metadata.drop_all(self.engine)
		self.dropdb(url) 

Base = declarative_base()
