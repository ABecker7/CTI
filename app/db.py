from sqlmodel import Field, Session, SQLModel, create_engine, select


class Threat(SQLModel, table=True):
    ioc_type: str | None = Field(default=None, primary_key=True)
    value: str | None = None
    source: str | None = None
    confidence: int | None = None
    cve: str | None = None
    attack_pattern: str | None = None
    timestamp: str | None = None


sqlite_file_name = "cti.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

def create_db_and_tables():  
    SQLModel.metadata.create_all(engine)

def create_threats():
    threat1 = Threat(ioc_type="ip", value="100.100.100.100",source="test")
    threat2 = Threat(ioc_type="domain", value="evil.com",source="eviltest")
    
    with Session(engine) as session:
        session.add(threat1)
        session.add(threat2)

        session.commit()

def select_threats():
    with Session(engine) as session:
        statement = select(Threat).where(Threat.ioc_type == "domain")
        results = session.exec(statement)
        for threat in results:

            print(threat)



def main():
    create_db_and_tables()
    create_threats()
    select_threats()

if __name__ == "__main__":
    main()
