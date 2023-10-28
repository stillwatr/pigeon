import dataset
import datetime
import typing

from pigeon.models import TelegramObject

COLUMN_TYPES: dict = {
    bool: dataset.types.Boolean,
    int: dataset.types.BigInteger,
    float: dataset.types.Float,
    datetime.datetime: dataset.types.DateTime,
    dict: dataset.types.JSON,
}

# ==================================================================================================


class Database:
    """
    TODO
    """

    def __init__(self, db_root_dir: str, db_name: str) -> None:
        """
        TODO
        """
        self.db: dataset.Database = dataset.connect(
            url=f"sqlite:///{db_root_dir}/{db_name}.db",
            ensure_schema=False
        )

    def init_table(self, clazz: type[TelegramObject]) -> dataset.Table:
        """
        TODO
        """
        if not clazz:
            raise ValueError("No class given.")
        if not issubclass(clazz, TelegramObject):
            raise ValueError("The given class is not a subclass of 'TelegramObject'.")

        # Drop the table if it already exists.
        table_name: str = clazz.__name__
        if self.db.has_table(table_name):
            self.db[table_name].drop()

        table: dataset.Table = self.db.create_table(
            table_name,
            primary_id='id',
            primary_type=self.db.types.string
        )

        # Create a column for each "public" property (= each property not starting with "_").
        type_hints = typing.get_type_hints(clazz)
        public_props = {k: type_hints[k] for k in type_hints.keys() if not k.startswith("_")}
        for prop_name, prop_type in public_props.items():
            table.create_column(prop_name, COLUMN_TYPES.get(prop_type, dataset.types.Unicode))

        table.create_column("ts_created", dataset.types.DateTime, nullable=False)
        table.create_column("ts_modified", dataset.types.DateTime, nullable=False)

        # Create an index for each column.
        table.create_index(list(public_props.keys()))

        return table

    def get_many(self, clazz: type[TelegramObject], *_clauses, **kwargs) -> list[TelegramObject]:
        """
        TODO
        """
        if not clazz:
            raise ValueError("No class given.")
        if not issubclass(clazz, TelegramObject):
            raise ValueError("The given class is not a subclass of 'TelegramObject'.")

        # When no table for the given class exists, return an empty list.
        table_name: str = clazz.__name__
        if not self.db.has_table(table_name):
            return []
        table: dataset.Table = self.db[table_name]

        # Find the rows matching the specified clauses and arguments. Create an object for each.
        result = []
        for row in table.find(*_clauses, **kwargs):
            obj = clazz()
            for key in row:
                setattr(obj, key, row[key])
            result.append(obj)

        return result

    def get_one(self, clazz: type[TelegramObject], *_clauses, **kwargs) -> TelegramObject:
        """
        TODO
        """
        if not clazz:
            raise ValueError("No class given.")
        if not issubclass(clazz, TelegramObject):
            raise ValueError("The given class is not a subclass of 'TelegramObject'.")

        # When no table for the given class exists, return an empty list.
        table_name: str = clazz.__name__
        if not self.db.has_table(table_name):
            return
        table: dataset.Table = self.db[table_name]

        # Find the first row matching the specified clauses and arguments.
        row = table.find_one(*_clauses, **kwargs)
        if not row:
            return

        obj = clazz()
        for key in row:
            setattr(obj, key, row[key])

        return obj

    # ==============================================================================================

    def insert_one(self, clazz: type[TelegramObject], obj: TelegramObject) -> None:
        """
        TODO
        """
        if not clazz:
            raise ValueError("No class given.")
        if not issubclass(clazz, TelegramObject):
            raise ValueError("The given class is not a subclass of 'TelegramObject'.")
        if not obj:
            raise ValueError("No object given.")
        if not isinstance(obj, TelegramObject):
            raise ValueError("The given object is not an instance of 'TelegramObject'.")

        table_name: str = clazz.__name__
        if not self.db.has_table(table_name):
            raise ValueError("No table exists for the specified class.")

        row = vars(obj)
        ts_now = datetime.datetime.utcnow()
        row["ts_created"] = ts_now
        row["ts_modified"] = ts_now
        self.db[table_name].insert(row, ensure=False)

    def insert_many(self, clazz: type[TelegramObject], objs: list[TelegramObject]) -> None:
        """
        TODO
        """
        if not clazz:
            raise ValueError("No class given.")
        if not issubclass(clazz, TelegramObject):
            raise ValueError("The given class is not a subclass of 'TelegramObject'.")
        if not objs:
            raise ValueError("No objects given.")
        for obj in objs:
            if not isinstance(obj, TelegramObject):
                raise ValueError("One of the given objects is not an instance of 'TelegramObject'.")

        table_name: str = clazz.__name__
        if not self.db.has_table(table_name):
            raise ValueError("No table exists for the specified class.")

        ts_now = datetime.datetime.utcnow()

        rows = []
        for obj in objs:
            row = vars(obj)
            row["ts_created"] = ts_now
            row["ts_modified"] = ts_now
            rows.append(row)
        self.db[table_name].insert_many(rows, ensure=False)

    # ==============================================================================================

    def update_one(self, clazz: type[TelegramObject], obj: TelegramObject) -> None:
        """
        TODO
        """
        if not clazz:
            raise ValueError("No class given.")
        if not issubclass(clazz, TelegramObject):
            raise ValueError("The given class is not a subclass of 'TelegramObject'.")
        if not obj:
            raise ValueError("No object given.")
        if not isinstance(obj, TelegramObject):
            raise ValueError("The given object is not an instance of 'TelegramObject'.")

        table_name: str = clazz.__name__
        if not self.db.has_table(table_name):
            raise ValueError("No table exists for the specified class.")

        row = vars(obj)
        row["ts_modified"] = datetime.datetime.utcnow()
        self.db[table_name].update(row, keys=["id"], ensure=False)

    def update_many(self, clazz: type[TelegramObject], objs: list[TelegramObject]) -> None:
        """
        TODO
        """
        if not clazz:
            raise ValueError("No class given.")
        if not issubclass(clazz, TelegramObject):
            raise ValueError("The given class is not a subclass of 'TelegramObject'.")
        if not objs:
            raise ValueError("No objects given.")
        for obj in objs:
            if not isinstance(obj, TelegramObject):
                raise ValueError("One of the given objects is not an instance of 'TelegramObject'.")

        table_name: str = clazz.__name__
        if not self.db.has_table(table_name):
            raise ValueError("No table exists for the specified class.")

        ts_now = datetime.datetime.utcnow()

        rows = []
        for obj in objs:
            row = vars(obj)
            row["ts_modified"] = ts_now
            rows.append(row)
        self.db[table_name].update_many(rows, keys=["id"], ensure=False)

    # ==============================================================================================

    def upsert_one(self, clazz: type[TelegramObject], obj: TelegramObject) -> None:
        """
        TODO
        """
        if not clazz:
            raise ValueError("No class given.")
        if not issubclass(clazz, TelegramObject):
            raise ValueError("The given class is not a subclass of 'TelegramObject'.")
        if not obj:
            raise ValueError("No object given.")
        if not isinstance(obj, TelegramObject):
            raise ValueError("The given object is not an instance of 'TelegramObject'.")

        table_name: str = clazz.__name__
        if not self.db.has_table(table_name):
            raise ValueError("No table exists for the specified class.")

        ts_now = datetime.datetime.utcnow()

        row = vars(obj)
        if not self.contains(clazz, obj):
            row["ts_created"] = ts_now
        row["ts_modified"] = ts_now
        self.db[table_name].upsert(row, keys=["id"], ensure=False)

    def upsert_many(self, clazz: type[TelegramObject], objs: list[TelegramObject]) -> None:
        """
        TODO
        """
        if not clazz:
            raise ValueError("No class given.")
        if not issubclass(clazz, TelegramObject):
            raise ValueError("The given class is not a subclass of 'TelegramObject'.")
        if not objs:
            raise ValueError("No objects given.")
        for obj in objs:
            if not isinstance(obj, TelegramObject):
                raise ValueError("One of the given objects is not an instance of 'TelegramObject'.")

        table_name: str = clazz.__name__
        if not self.db.has_table(table_name):
            raise ValueError("No table exists for the specified class.")

        ts_now = datetime.datetime.utcnow()

        rows = []
        for obj in objs:
            row = vars(obj)
            if not self.contains(clazz, obj):
                row["ts_created"] = ts_now
            row["ts_modified"] = ts_now
            rows.append(row)
        self.db[table_name].upsert_many(rows, keys=["id"], ensure=False)

    # ==============================================================================================

    def delete_one(self, clazz: type[TelegramObject], *_clauses, **kwargs) -> bool:
        """
        TODO
        """
        if not clazz:
            raise ValueError("No class given.")
        if not issubclass(clazz, TelegramObject):
            raise ValueError("The given class is not a subclass of 'TelegramObject'.")

        table_name: str = clazz.__name__
        if not self.db.has_table(table_name):
            raise ValueError("No table exists for the specified class.")

        return self.db[table_name].delete(*_clauses, **kwargs)

    # ==============================================================================================

    def contains(self, clazz: type[TelegramObject], *_clauses, **kwargs) -> bool:
        """
        TODO
        """
        return self.get_one(clazz, *_clauses, **kwargs) is not None

    def count(self, clazz: type[TelegramObject], *_clauses, **kwargs) -> int:
        """
        TODO
        """
        if not clazz:
            raise ValueError("No class given.")
        if not issubclass(clazz, TelegramObject):
            raise ValueError("The given class is not a subclass of 'TelegramObject'.")

        # When no table for the given class exists, return an empty list.
        table_name: str = clazz.__name__
        if not self.db.has_table(table_name):
            return 0

        return self.db[table_name].count(*_clauses, **kwargs)


class DatabasePool:
    """
    TODO
    """

    def __init__(self, db_root_dir: str):
        """
        TODO
        """
        self.db_root_dir: str = db_root_dir
        self.db_cache: dict[str, Database] = {}

    def get_database(self, db_name: str, create_if_not_exists: bool = False) -> Database:
        """
        TODO
        """
        if db_name not in self.db_cache and create_if_not_exists:
            self.db_cache[db_name] = Database(self.db_root_dir, db_name)

        return self.db_cache[db_name]
