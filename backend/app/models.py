from sqlalchemy import Column, Integer, String

from app.database import Base


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    severity = Column(String)
    mitre_technique = Column(String)
    technique_name = Column(String)
    tactic = Column(String)
    description = Column(String)
    recommended_action = Column(String)