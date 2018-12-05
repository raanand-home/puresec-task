import connexion
from entities import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = connexion.App(__name__, specification_dir='swagger/')


engine = create_engine('sqlite:///a.db', echo=False)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)


if __name__ == '__main__':
    app.add_api('api.yaml')
    app.run(port=5001)
