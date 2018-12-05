from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Column, Integer, String, Float, ForeignKey




Base = declarative_base()

class Function(Base):
	__tablename__ = '__function__'
	arn = Column(String, primary_key=True)
	name = Column(String)
	runtime = Column(String)
	memory = Column(Integer)

class Execution(Base):
	__tablename__ = 'execution'
	id = Column(Integer, primary_key=True)
	total_time = Column(Integer)
	security_insepect_time = Column(Integer)
	cpu_presentage = Column(Float)
	used_memory = Column(Integer)
	finnish_state = Column(Integer)
	application = Column(String)
	function = Column('func_id', String, ForeignKey("__function__.arn"), nullable=False)



