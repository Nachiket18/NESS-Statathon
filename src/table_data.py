"""
@author: Rany Kamel (UltraArceus3)

Other Contributors:
"""
#import anomaly_detection as anom_detect
import json
import string


class Table:
    """
    A class to compare data points (as floats) to ranges, and return what range it is within.

    entries: dict - A dictionary of ranges that the data will be compared to. Formatted as:
                    key: (lower bound, upper bound)
                    When a data point is within a specific range, the key of the matching range is returned.
                    When one of the bounds is None, the range encompasses all numbers within that direction.
                    e.g.: (None, 20) = All numbers less than or equal to 20 (or from -infinity to 20).
    """

    def __init__(self, entries: dict, keys: list = []):
        self.entries = entries  # Allows for entries to be pre-inputted to table w/o using add_entry
        self.keys = keys

    def add_entry(
        self, id, lower_range=None, upper_range=None
    ):  # Adds a range to the table
        """
        Adds a new range to the Table class.

        id - What will be returned when a data point is within range
        lower_range - The lowest bound in the range. When None, it extends to -infinity.
        upper_range - The highest bound in the range. When None, it extends to infinity.
        """
        self.entries[id] = [lower_range, upper_range]

    def check_data(
        self, data: float
    ):  # Data - The number you want to check, compare to table ranges
        """
        Checks a data point if it is within one of the stored ranges and returns the key of said range.
        """
        data = float(data)
        for i in range(len(self.entries)):  # Checks each range until it finds the matching one

            val = list(self.entries.values())[i]  # val[0] - Lower Range, val[1] - Upper Range

            if (val[0] is None or data >= val[0]) and (
                val[1] is None or data <= val[1]):  
                # If data is greater than lower and less than upper
                # (None is when range goes to -inf or inf)

                return list(self.entries.keys())[i]  # Return corresponding range id
        return [None]

    def is_processed(self) -> bool:
        """
        Checks if the data has been processed (if the keys had been separated from the dictionary).
        """
        return len(self.keys) > 0

    def process_table(self) -> None:
        """
        Separates the keys from the table, moving them into self.keys as a list and leaving
        self.entries with 0, 1, 2, ... len(self.entries)-1 as the dictionary keys.
        """
        if self.is_processed():
            # print(self.keys)
            return

        self.__dict__.update(process_table(self).__dict__)
        # Takes the __dict__ of the table generated in process_table, and overrides
        # its __dict__ with the new table's, effectively changing it to the new table.


class TableGroup:
    """
    A class to compare a list of data points to a list of corresponding tables simultaneously.

    tables: list - List of Table classes. A list of data points will be compared to a table on the same index.
    """

    def __init__(self, tables: list):
        self.tables = tables  # Pre-input tables

    def create_table(self, entries: dict):
        """
        Creates a new Table class.

        entries: dict - A dictionary of ranges that the data will be compared to. (read Table class docstring for more info.)
                        It is used to create a new Table class.
        """
        self.tables.append(Table(entries))  # Creates new table w/ inputted entries

    def check_datas(
        self, datas: list
    ):  # Checks mutliple data points w/ multiple tables
        """
        Checks a list of data points with its corresponding table at the same index and
        returns a list of keys of ranges that each data point matched.

        Length of data and length of tables MUST match
        as each data point must have a corresponding table.
        """
        if len(datas) != len(
            self.tables
        ):  # Data index must match table index, i.e. lens must equal
            raise Exception(
                "Number of data ({}) don't match number of tables ({})!".format(
                    len(datas), len(self.tables)
                )
            )

        dat_ret = []
        for i in range(len(self.tables)):
            dat_ret.append(
                self.tables[i].check_data(datas[i])
            )  # Checks table check_data w/ corresponding data entry

        return dat_ret

    def process_all(self) -> None:
        for i in self.tables:
            assert isinstance(i, Table)
            i.process_table()


def csv_to_data(file_path: str, data_range: list):  # data_range - from what to what
    """
    A function to convert comma-separated value (CSV) files to a list of numerical data.

    file_path: str - Path to CSV file
    data_range: list - Range of data in CSV to be extracted and converted.
                       Formatted as either: 
                            -  (lower bound, upper bound) 
                                    [for single bound range]
                            -  ((lower bound 1, upper bound 1),
                                (lower bound 2, upper bound 2),
                                ...) 
                                    [for multiple, separate bound ranges]
    """

    with open(file_path, "r") as f:
        def _get_data(d_r: int, file: string) -> list:
            return file.split(",")[(d_r[0] - 1) : d_r[1]]

        data = []

        for i in f.readlines():
            if type(data_range[0]) is list or type(data_range[0]) is tuple:
                dat_row = []

                for d_r in data_range:
                    dat_row += _get_data(d_r, i)
                data.append(dat_row)
                #data = [x for dat_list in data for x in dat_list]

            else:
                data.append(_get_data(data_range, i))

            
            # Temperature[3] - App. Temperature[4] - Humidty[5] - Wind Speed[6] - Wind Bearing[7]
            # Visibility[8] - Loud Cover[9] - Pressure[10]

    return data


def json_to_tables(file_path: str, return_tablegroup=True) -> TableGroup | Table | list:
    """
    A function to convert JSON files of tables to Table classes.

    file_path: str - Path to JSON file
    return_tablegroup: bool = True - When the number of tables is greater than 1, should the tables
                                     be packed into a TableGroup class? (True by default)
    """
    with open(file_path, "r") as f:  # Opens JSON file
        json_data = json.load(f)  # Converts JSON data to Dictionary
        table_data = list(json_data.values())  # Gets Table Data

        tables = []
        for i in table_data:
            tables.append(Table(i))  # Converts Table Data to Table Classes

        if return_tablegroup:
            return TableGroup(tables) if len(tables) > 1 else tables[0]
            # Returns TableGroup if there are more than one table, else just a Table gets returned
        else:
            return tables


def discretize_data(data: list, tables: TableGroup):
    return tables.check_datas(data)


def process_table(table: Table) -> Table:
    def _replace_key(dict, old_key, new_key) -> None:
        dict[new_key] = dict[old_key]
        del dict[old_key]

    table_entries = table.entries.copy()
    table_keys = list(table_entries.keys())
    keys = []

    for i in range(len(table_entries)):
        keys.append(table_keys[i])
        _replace_key(table_entries, keys[i], i)

    new_table = Table(table_entries, keys)

    return new_table


if __name__ == "__main__":

    #x = csv_to_data("src/data/weatherHistory.csv", (4, 11))
    #x = csv_to_data("data/train.csv", (5, 17))
    x = csv_to_data("data/train.csv", [ (6, 7), #age, len.at.res
                                        (11, 11), #premiums
                                        (15, 16) #adults, children
                                        ])
    col_names = x[0]
    x.pop(0)

    tgg = json_to_tables("data/train.json")
    tgg.process_all()

    print([x.entries for x in tgg.tables])

    #print(x)

    for i in range(10):
        dis_test = discretize_data(x[i], tgg)
        print(x[i])
        
        print(dis_test)
        print("\n")
