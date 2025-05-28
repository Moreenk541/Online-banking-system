
from cli import main_menu
from models import Base
from conn import engine


Base.metadata.create_all(engine)

if __name__ == "__main__":
    main_menu()








