from sqlmodel import Field, Session, SQLModel, create_engine, select


class Threat(SQLModel, table=True):
    
    id: int | None = Field(default=None, primary_key=True)
    indicator: str | None = None
    type: str | None = None
    confidence: int | None = None
    cve: str | None = None
    attack_pattern: str | None = None
    timestamp: str | None = None


sqlite_file_name = "cti.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

def create_db_and_tables():  
    SQLModel.metadata.create_all(engine)

def create_threats(id_id, indicator_ind):
    threat1 = Threat(id=id_id, indicator=indicator_ind)
    
    with Session(engine) as session:
        session.add(threat1)

        session.commit()

def select_threats():
    with Session(engine) as session:
        statement = select(Threat).where(Threat.type == "domain")
        results = session.exec(statement)
        for threat in results:

            print(threat)



def main():
    create_db_and_tables()
    create_threats()
    select_threats()

if __name__ == "__main__":
    select_threats()
