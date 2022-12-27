# File Name: db.py

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('mysql://root:Dragon1573_gm4wsl2@localhost/study?charset=utf8')
Base = declarative_base(engine)


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True, nullable=False)
    email = Column(String(64), unique=True)

    def __repr__(self):
        return '<User: {}>'.format(self.name)


class Course(Base):
    __tablename__ = 'course'
    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))
    user = relationship('User',
            backref=backref('course', cascade='all, delete-orphan'))

    def __repr__(self):
        return '<Course: {}>'.format(self.name)


class Lab(Base):
    __tablename__ = 'lab'
    id = Column(Integer, ForeignKey('course.id'), primary_key=True)
    name = Column(String(128))
    course = relationship('Course', backref=backref('lab', uselist=False))

    def __repr__(self):
        return '<Lab: {}>'.format(self.name)


Rela = Table('rela', Base.metadata,
        Column('tag_id', Integer, ForeignKey('tag.id'), primary_key=True),
        Column('course_id', Integer, ForeignKey('course.id'), primary_key=True)
)


class Tag(Base):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True)
    course = relationship('Course', secondary=Rela, backref='tag')

    def __repr__(self):
        return '<Tag: {}>'.format(self.name)


if __name__ == '__main__':
    Base.metadata.create_all()
