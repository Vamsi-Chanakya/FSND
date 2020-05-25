import os
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base


def db_fun():

    database_filename = "database.db"
    project_dir = os.path.dirname(os.path.abspath(''))
    database_path = "sqlite:///{}".format(os.path.join(project_dir, 'FlaskRecap', database_filename))
    print("database_path : " + database_path)

    engine = create_engine(database_path)


def main():

    db_fun()

    Base = declarative_base()

    class User(Base):
        __tablename__ = 'users'
        # Autoincrementing, unique primary key
        id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
        # String Title
        username = Column(String(80), unique=True)
        # the ingredients blob - this stores a lazy json blob
        # the required datatype is [{'color': string, 'name':string, 'parts':number}]
        password = Column(String(180), nullable=False)

        def __repr__(self):
            return self.username + ": " + self.password

    User.metadata.create_all(engine)

    User.__table__



if __name__ == "__main__":
    main()