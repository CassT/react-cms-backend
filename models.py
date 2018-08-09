from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from settings import DATABASE_STRING
import hashlib


engine = create_engine(
    DATABASE_STRING,
    connect_args={'check_same_thread': False},
)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


#def hash_password(password):
#    return hashlib.sha512(password.encode('utf-8').hexdigest())


#class User(Base):
#    __tablename__ = 'users'
#    uid = Column(Integer, primary_key=True, autoincrement=True)
#    username = Column(String, primary_key=True)
#    password = Column(String)
#    display_name = Column(String)
#    is_administrator = Column(Integer)
#
#    def authenticate(self, username, password):
#        pass


#class Group(Base):
#    __tablename__ = 'groups'
#    group_id = Column(Integer, primary_key=True, autoincrement=True)
#    display_name = Column(String)


#class UserGroupAffiliation(Base):
#    __tablename__ = 'user_group_affiliations'
#    uid = Column(Integer, primary_key=True)
#    group_id = Column(Integer, primary_key=True)
#    is_owner = Column(Integer)


class Page(Base):
    __tablename__ = 'pages'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    parent = Column(Integer)
    slug = Column(String)
    content = Column(String)

    def as_dictionary(self):
        return {
            "id": self.id,
            "title": self.title,
            "parent": self.parent,
            "slug": self.slug,
            "content": self.content
        }

    def navigation_dictionary(self):
        return {
            "id": self.id,
            "title": self.title,
            "slug": self.slug,
            "parent": self.parent,
        }





#class PageHierarchy(Base):
#    __tablename__ = 'page_hierarchies'
#    parent = Column(Integer)
#    child = Column(Integer, primary_key=True)


#class UserPagePermission(Base):
#    __tablename__ = 'user_page_permissions'
#    uid = Column(Integer, primary_key=True)
#    page_id = Column(Integer, primary_key=True)
#    can_view = Column(Integer)
#    can_edit = Column(Integer)
#    can_add = Column(Integer)
#    can_delete = Column(Integer)


#class GroupPagePermission(Base):
#    __tablename__ = 'group_page_permissions'
#    group_id = Column(Integer, primary_key=True)
#    page_id = Column(Integer, primary_key=True)
#    can_view = Column(Integer)
#    can_edit = Column(Integer)
#    can_add = Column(Integer)
#    can_delete = Column(Integer)


def initialize_database():
    Base.metadata.create_all(engine)