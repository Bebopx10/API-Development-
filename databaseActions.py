from pathlib import Path
import sqlite3
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Person:
    id: int
    name: str
    sex: str
    year: str
    numberOfDocuments: int

class DatabaseActions:
    CONFIG_PATH = Path("config.cfg")
    with open(CONFIG_PATH, "r") as config_file:
        lines = config_file.readlines()
        db_name = lines[0].strip().split("=")[1].strip()
        names_folder = lines[1].strip().split("=")[1].strip()
    DB_PATH = db_name
    NAMES_PATH = names_folder

    def get_conn():
        conn = sqlite3.connect(DatabaseActions.DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    
def init_db():
    with DatabaseActions.get_conn() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS people (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            sex TEXT NOT NULL,
            year TEXT NOT NULL,
            numberOfDocuments INTEGER
                CHECK(length(Name) <= 15),
            CHECK(length(Sex) == 1),
            CHECK(length(Year) <= 4),
            CHECK(NumberOfOccurrences >= 0),
        )
        """)
        conn.commit()

def create_person(person: Person):
    with DatabaseActions.get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO people (Name, Sex, year, numberOfOccurences) VALUES (?, ?, ?, ?)",
            (person.name, person.sex, person.year, person.numberOfOccurences)
        )
        conn.commit()
        return cur.lastrowid
    
def get_person_by_id(person_pk: int) -> Optional[Person]:
    with DatabaseActions.get_conn() as conn:
        row = conn.execute("SELECT * FROM people WHERE id = ?", (person_pk,)).fetchone()
        return Person(**row) if row else None
    
def get_person_by_name(name: str) -> Optional[Person]:
    with DatabaseActions.get_conn() as conn:
        row = conn.execute("SELECT * FROM people WHERE name = ?", (name,)).fetchone()
        return Person(**row) if row else None
    
def list_years_by_person_name(name: str) -> List[str]:
    with DatabaseActions.get_conn() as conn:
        rows = conn.execute("SELECT year FROM people WHERE name = ?", (name,)).fetchall()
        return [row["year"] for row in rows]
    
def list_persons() -> List[Person]:
    with DatabaseActions.get_conn() as conn:
        rows = conn.execute("SELECT * FROM people").fetchall()
        return [Person(**row) for row in rows]
    
def update_person(person: Person) -> bool:
    if person.id is None:
        raise ValueError("update_person requires person.id to be set")
    with DatabaseActions.get_conn() as conn:
        cur = conn.execute(
            """UPDATE people
            SET name = ?, sex = ?, year = ?, numberOfDocuments = ?
            WHERE id = ?
            """,
            (person.name, person.sex, person.year, person.numberOfDocuments, person.id)
        )
        conn.commit()
        return cur.rowcount == 1
    
def delete_person(person: Person) -> bool:
    if person.id is None:
        raise ValueError("delete_person requires person.id to be set")
    with DatabaseActions.get_conn() as conn:
        cur = conn.execute("DELETE FROM people WHERE id = ?", (person.id,))
        conn.commit()
        return cur.rowcount == 1
    
def generate_database():
    if DatabaseActions.DB_PATH.exists():
        DatabaseActions.DB_PATH.unlink()

        DatabaseActions.init_db()

for file_path in DatabaseActions.NAMES_PATH.glob("*.txt"):
    year = file_path.stem
    year = year[3:]
    print(f"Processing year: {year})")
    with file_path.open("r, encoding='utf-8") as f:
        for line in f:
            parts = line.strip().split(",")
            if len(parts) != 3:
                continue
            name, sex, count_str = parts
            try:
                count = int(count_str)
            except ValueError:
                continue
            person = person(
                Id=None
                Name=name,
                Sex=sex,
                Year=year,
                NumberOfOccurences=count
            )
            DatabaseActions.create_person(person)
print("Database population complete.")