import sqlite3


class TriangleDatabase:

    def __init__(self, db_path=":memory:"):
        self.conn = sqlite3.connect(db_path)
        self._init_table()

    def _init_table(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS triangles (
                side_a REAL,
                side_b REAL,
                side_c REAL,
                triangle_type TEXT,
                error_message TEXT,
                PRIMARY KEY (side_a, side_b, side_c)
            )
        """)
        self.conn.commit()

    def add(self, a: float, b: float, c: float, tri_type: str, error_msg: str = "") -> None:
        self.conn.execute(
            "INSERT OR REPLACE INTO triangles (side_a, side_b, side_c, triangle_type, error_message) "
            "VALUES (?, ?, ?, ?, ?)",
            (float(a), float(b), float(c), tri_type, error_msg)
        )
        self.conn.commit()

    def get(self, a: float, b: float, c: float):
        cur = self.conn.execute(
            "SELECT triangle_type, error_message FROM triangles "
            "WHERE side_a=? AND side_b=? AND side_c=?",
            (float(a), float(b), float(c))
        )
        return cur.fetchone()

    def delete(self, a: float, b: float, c: float) -> None:
        self.conn.execute(
            "DELETE FROM triangles WHERE side_a=? AND side_b=? AND side_c=?",
            (float(a), float(b), float(c))
        )
        self.conn.commit()

    def close(self):
        self.conn.close()