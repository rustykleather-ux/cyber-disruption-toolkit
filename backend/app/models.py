from sqlalchemy import Column, Integer, String

from app.database import Base


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    severity = Column(String)
    risk_score = Column(Integer)
    mitre_technique = Column(String)
    host = Column(String)
    user = Column(String)
    source_ip = Column(String)
    technique_name = Column(String)
    tactic = Column(String)
    description = Column(String)
    recommended_action = Column(String)