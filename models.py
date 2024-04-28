from sqlalchemy import Integer, String, Column, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    surname = Column(String)
    name = Column(String)
    age = Column(Integer)
    position = Column(String)
    speciality = Column(String)
    address = Column(String)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    modified_date = Column(DateTime)

    def __repr__(self):
        return f"<Colonist> {self.id} {self.surname} {self.name}"


class Jobs(Base):
    __tablename__ = 'jobs'
    id = Column(Integer, primary_key=True)
    team_leader = Column(Integer, ForeignKey('users.id'))
    job = Column(String)
    work_size = Column(Integer)
    collaborators = Column(String)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    is_finished = Column(Boolean)
    user = relationship('User')

    def __repr__(self):
        return f"<Job> {self.job}"


class Department(Base):
    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    chief = Column(Integer, ForeignKey('users.id'))
    members = Column(String)
    email = Column(String)