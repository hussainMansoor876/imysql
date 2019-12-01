from dataclasses import dataclass
import functools
import pymysql


@dataclass
class MySQL:
    """
    Connecting your MySQL database with CRUD operation.
    :param host (str): hostname
    :param user (str): user
    :param password (str): password
    :param db (str): database name
    :param port (int): port number, default is 3306
    :param charset (str): character set, default is `utf8mb4`
    :param autocommit (bool): enables realt-time execution, default is True
    :param cursorclass (type): default is DictCursor class object
    """
    host: str
    user: str
    password: str
    db: str
    port: int = 3306
    charset: str = 'utf8mb4'
    autocommit: bool = True
    cursorclass: type = pymysql.cursors.DictCursor

    def __post_init__(self):
        """
        Initializing connection.
        :returns (null): no returning value
        """
        self.connection = pymysql.connect(**self.__dict__)
        self.cursor = self.connection.cursor()
        # delete sql and args from object's dict to begin another transaction
        [self.__dict__.pop(item, ...) for item in ['sql', 'args']]

    def errorhandler(self):
        """
        Error handling for each method operations.
        :returns (type): error with statement
        """
        @functools.wraps(self)
        def wrapper(*args, **kwargs):
            try:
                return self(*args, **kwargs)
            except Exception as e:
                return f'error: {e}'
        return wrapper

    @errorhandler
    def fetchone(self):
        """
        SELECT a row.
        :returns (dict): selected single row
        """
        self.cursor.execute(self.sql, self.args)
        return self.cursor.fetchone()

    @errorhandler
    def fetchall(self):
        """
        SELECT more than one row.
        :returns (list): list of dictionaries of selected rows
        """
        self.cursor.execute(self.sql, self.args)
        return self.cursor.fetchall()

    @errorhandler
    def commit(self):
        """
        CREATE INSERT UPDATE DELETE row/s.
        :returns (str): 'success'
        """
        self.cursor.execute(self.sql, self.args)
        self.connection.commit()
        return 'success'

    def __del__(self):
        """
        Closing connection.
        :returns (null): no returning value
        """
        self.connection.close()
