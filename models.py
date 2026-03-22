# models.py
#
# A Metaclass runs when Python DEFINES your class (not when you create an instance).
# We use it to:
#   1. Read the class's type annotations (name: str, age: int)
#   2. Automatically create a matching SQLite table
#
# When you write:
#   class User(BaseModel):
#       name: str
#       age: int
#
# Python calls ModelMeta.__new__() at class-definition time.
# We read __annotations__ = {"name": str, "age": int} and build the SQL.

import sqlite3

DB_FILE = "database.db"

# Map Python types to SQLite column types
PYTHON_TO_SQL = {
    "str":   "TEXT",
    "int":   "INTEGER",
    "float": "REAL",
    "bool":  "INTEGER",   # SQLite has no bool, use 0/1
}


class ModelMeta(type):
    """
    Metaclass for BaseModel.
    Runs when a subclass of BaseModel is defined.
    Reads type annotations and creates the SQLite table automatically.
    """

    def __new__(mcs, class_name, bases, attrs):
        # Build the class normally first
        cls = super().__new__(mcs, class_name, bases, attrs)

        # Skip BaseModel itself — only process subclasses
        if class_name == "BaseModel":
            return cls

        # __annotations__ holds the type hints: {"name": str, "age": int}
        # This is where Python stores "name: str" — NOT in regular attrs
        annotations = attrs.get("__annotations__", {})

        cls._fields     = annotations             # store for later use
        cls._table_name = class_name.lower()      # User -> "user"

        # Create the SQLite table now
        cls._create_table()
        return cls

    def _create_table(cls):
        """Generate and run CREATE TABLE IF NOT EXISTS ..."""
        columns = ["id INTEGER PRIMARY KEY AUTOINCREMENT"]

        for field_name, field_type in cls._fields.items():
            # field_type is the actual type object (str, int, etc.)
            type_name = field_type.__name__ if hasattr(field_type, "__name__") else str(field_type)
            sql_type  = PYTHON_TO_SQL.get(type_name, "TEXT")
            columns.append(f"{field_name} {sql_type}")

        sql = (
            f"CREATE TABLE IF NOT EXISTS {cls._table_name} "
            f"({', '.join(columns)})"
        )

        conn = sqlite3.connect(DB_FILE)
        conn.execute(sql)
        conn.commit()
        conn.close()
        print(f"  [ORM] Table '{cls._table_name}' is ready. Columns: {list(cls._fields.keys())}")


class BaseModel(metaclass=ModelMeta):
    """
    Base class for all models.
    Subclass it and add type-annotated fields:

        class User(BaseModel):
            name: str
            age: int

    Then:
        u = User(name="Alice", age=30)
        u.save()    # INSERT INTO user (name, age) VALUES (?, ?)
        print(u.id) # auto-assigned by SQLite
    """

    # These will be overridden in subclasses by the metaclass
    _fields     = {}
    _table_name = ""

    def __init__(self, **kwargs):
        self.id = kwargs.get("id", None)
        for field_name in self._fields:
            setattr(self, field_name, kwargs.get(field_name))

    def save(self):
        """
        Save this object to the database.
        INSERT if id is None, UPDATE if id already exists.
        """
        conn   = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        field_names = list(self._fields.keys())
        values      = [getattr(self, f, None) for f in field_names]

        if self.id is None:
            # Build: INSERT INTO user (name, age) VALUES (?, ?)
            columns      = ", ".join(field_names)
            placeholders = ", ".join(["?"] * len(field_names))
            sql          = f"INSERT INTO {self._table_name} ({columns}) VALUES ({placeholders})"

            cursor.execute(sql, values)
            self.id = cursor.lastrowid   # SQLite gives us back the new id
            print(f"  [ORM] Inserted into '{self._table_name}' — id={self.id}")
        else:
            # Build: UPDATE user SET name=?, age=? WHERE id=?
            set_clause = ", ".join([f"{f} = ?" for f in field_names])
            sql        = f"UPDATE {self._table_name} SET {set_clause} WHERE id = ?"

            cursor.execute(sql, values + [self.id])
            print(f"  [ORM] Updated '{self._table_name}' — id={self.id}")

        conn.commit()
        conn.close()
        return self   # return self so you can chain: u = User(...).save()

    @classmethod
    def all(cls):
        """Fetch all rows from this table and return a list of model instances."""
        conn   = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {cls._table_name}")
        rows = cursor.fetchall()
        conn.close()

        # Build column name list: id + our fields
        column_names = ["id"] + list(cls._fields.keys())
        result       = []
        for row in rows:
            obj = cls(**dict(zip(column_names, row)))
            result.append(obj)
        return result

    def __repr__(self):
        fields_str = ", ".join(
            f"{f}={getattr(self, f, None)!r}" for f in self._fields
        )
        return f"<{self.__class__.__name__} id={self.id} {fields_str}>"
