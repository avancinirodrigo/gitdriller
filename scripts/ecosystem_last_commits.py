from ecolyzer.ecosystem import EcosystemAnalyzer
from ecolyzer.system import System
from ecolyzer.repository import Repository, Person, Author, RepositoryMiner, GitPython
from ecolyzer.dataaccess import SQLAlchemyORM
from ecolyzer.ecosystem import Ecosystem

db_url = 'postgresql://postgres:postgres@localhost:5432/ecosystem_last_commits'
db = SQLAlchemyORM(db_url)
db.create_all(True)
session = db.create_session()

repo1 = Repository('repo/terrame')
sys1 = System('terrame', repo1)

session.add(repo1)
session.add(sys1)

miner = RepositoryMiner(repo1, sys1)
miner.add_ignore_dir_with('test')
miner.add_ignore_dir_with('example')	
miner.extract_last_commits(session, '2.0-RC-8')

repo2 = Repository('repo/ca')
sys2 = System('ca', repo2)
miner = RepositoryMiner(repo2, sys2)	
miner.extract_last_commits(session)

repo3 = Repository('repo/calibration')
sys3 = System('calibration', repo3)
miner = RepositoryMiner(repo3, sys3)	
miner.extract_last_commits(session)

repo4 = Repository('repo/logo')
sys4 = System('logo', repo4)
miner = RepositoryMiner(repo4, sys4)	
miner.extract_last_commits(session)

ecosystem = Ecosystem()

ecolyzer = EcosystemAnalyzer(ecosystem)
ecolyzer.make_relations(sys2, sys1, session)
ecolyzer.make_relations(sys3, sys1, session)
ecolyzer.make_relations(sys4, sys1, session)

session.close()