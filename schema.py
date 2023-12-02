from typing import List, Optional
from pydantic import BaseModel
import datetime


class Profile(BaseModel):
    name: str
    email: str
    phone: str
    linkedin: Optional[str]
    site: Optional[str]


class Education(BaseModel):
    institution: str
    location: str
    degree: str
    gpa: float
    honors: Optional[str]
    start_date: datetime.date
    end_date: Optional[datetime.date] = None


class Job(BaseModel):
    title: str
    employer: str
    location: str
    start_date: datetime.date
    end_date: Optional[datetime.date] = None
    description: List[str]


class Leadership(BaseModel):
    title: str
    entity: str
    location: str
    start_date: datetime.date
    end_date: datetime.date
    description: List[str]


class Award(BaseModel):
    title: str
    dates: List[datetime.date]
    awarder: str
    summary: str


class Project(BaseModel):
    title: str
    date: datetime.date
    description: str
    link: Optional[str]


class Resume(BaseModel):
    profile: Profile
    languages: Optional[List[str]] = None
    tools: Optional[List[str]] = None
    work: Optional[List[Job]] = None
    education: Optional[List[Education]] = None
    leadership: Optional[List[Leadership]] = None
    projects: Optional[List[Project]] = None
    awards: Optional[List[Award]] = None
