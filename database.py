from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String
)

from sqlalchemy.orm import (
    declarative_base,
    sessionmaker
)

engine = create_engine(
    "sqlite:///netshield.db"
)

Base = declarative_base()

class Alert(Base):

    __tablename__ = "alerts"

    id = Column(
        Integer,
        primary_key=True
    )

    time = Column(String)

    alert_type = Column(String)

    source_ip = Column(String)

    severity = Column(String)

    details = Column(String)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)