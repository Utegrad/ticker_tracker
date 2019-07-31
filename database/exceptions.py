""" Custom exceptions for working with the database. """


class InvalidDecimalRecordDataException(Exception):
    def __init__(self):
        self.message = "Data from record found invalid for use with database"
