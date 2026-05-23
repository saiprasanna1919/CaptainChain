from pydantic import BaseModel


class Player(BaseModel):
    id: str
    name: str
    country: str
    image: str = ""
    batting_style: str = ""
    role: str = ""
    teams: list[str] = []


class Relationship(BaseModel):
    captain: str
    player: str
    team: str
    tournament: str
    season: str
    year: int
    captain_role: str = ""
    notes: str = ""


class PathResult(BaseModel):
    path: list[str]
    relationships: list[Relationship]
    degrees: int


class HiddenFact(BaseModel):
    fact: str
    players: list[str]
    context: str
