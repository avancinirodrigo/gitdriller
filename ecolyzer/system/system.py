from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from ecolyzer.dataaccess import Base

class System(Base):
	"""System"""
	__tablename__ = 'system'

	id = Column(Integer, primary_key=True)
	name = Column(String, nullable=False, unique=True)
	repo_id = Column(Integer, ForeignKey('repository.id'))
	repository = relationship('Repository', backref=backref('system', 
							uselist=False, cascade='all,delete'))

	def __init__(self, name, repository):
		self.name = name
		self.repository = repository
