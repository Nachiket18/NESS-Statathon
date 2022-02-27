'''

'''
import anomaly_detection as anom_detect
import json


class Table:
    '''
    A class to compare data points (as floats) to ranges, and return what range it is within.

    entries: dict - A dictionary of ranges that the data will be compared to. Formatted as:
                    key: (lower bound, upper bound)
                    When a data point is within a specific range, the key of the matching range is returned.
                    When one of the bounds is None, the range encompasses all numbers within that direction.
                    e.g.: (None, 20) = All numbers less than or equal to 20 (or from -infinity to 20).
    '''


    def __init__(self, entries: dict):
        self.entries = entries #Allows for entries to be pre-inputted to table w/o using add_entry

    def add_entry(self, id, lower_range = None, upper_range = None): #Adds a range to the table
        '''
        Adds a new range to the Table class.

        id - What will be returned when a data point is within range
        lower_range - The lowest bound in the range. When None, it extends to -infinity.
        upper_range - The highest bound in the range. When None, it extends to infinity.
        '''
        self.entries[id] = [lower_range, upper_range]
    
    def check_data(self, data: float): #Data - The number you want to check, compare to table ranges
        '''
        Checks a data point if it is within one of the stored ranges and returns the key of said range.
        '''
        data = float(data)
        for i in range(len(self.entries)):  #Checks each range until it finds the matching one
            val = list(self.entries.values())[i] # val[0] - Lower Range, val[1] - Upper Range
            if (val[0] is None or data >= val[0]) and \
               (val[1] is None or data <= val[1]): #If data is greater than lower and less than upper
               # (None is when range goes to -inf or inf)

               return list(self.entries.keys())[i] #Return corresponding range id

class TableGroup:

    def __init__(self, tables: list):
        self.tables = tables #Pre-input tables

    def create_table(self, entries):
        self.tables.append(Table(entries)) #Creates new table w/ inputted entries

    def check_datas(self, datas: list): #Checks mutliple data points w/ multiple tables
        if len(datas) != len(self.tables): #Data index must match table index, i.e. lens must equal
            raise Exception("Number of data ({}) don't match number of tables ({})!"\
                .format(len(datas), len(self.tables)))

        dat_ret = []
        for i in range(len(self.tables)):
            dat_ret.append(self.tables[i].check_data(datas[i])) #Checks table check_data w/ corresponding data entry

        return dat_ret


def csv_to_data(file_path: str, data_range: list): #data_range - from what to what
    '''
    A function to convert comma-separated value (CSV) files to a list of numerical data.

    file_path: str - Path to CSV file
    data_range: list - Range of data in CSV to be extracted and converted. 
                       Formatted as: (lower bound, upper bound)
    '''


    with open(file_path, "r") as f:

        data = []

        for i in f.readlines():
            data.append(i.split(",")[(data_range[0] - 1):data_range[1]])
            # Temperature[3] - App. Temperature[4] - Humidty[5] - Wind Speed[6] - Wind Bearing[7] 
            # Visibility[8] - Loud Cover[9] - Pressure[10]

    return data


def json_to_tables(file_path: str) -> TableGroup | Table:

    with open(file_path, "r") as f: #Opens JSON file
        json_data = json.load(f) #Converts JSON data to Dictionary
        table_data = list(json_data.values()) #Gets Table Data

        tables = []
        for i in table_data:
            tables.append(Table(i)) #Converts Table Data to Table Classes
        
        return TableGroup(tables) if len(tables) > 1 else tables[0]
        #Returns TableGroup if there are more than one table, else just a Table gets returned

def discretize_data(data: list, tables: TableGroup):
    return tables.check_datas(data)


if __name__ == "__main__":
    help("table_data")

    exit()

    x = csv_to_data("src/data/weatherHistory.csv", (4, 11))
    x.pop(0)

    tgg = json_to_tables("src/data/tables_test.json")


    horiz_ds = []
    for i in range(1000):
        data = x[i][0:3]
        dis_dat = discretize_data(x[i][0:3], tgg)
        
        print(data, dis_dat)

        horiz_ds.append(anom_detect.horizontalDataset(i, dis_dat))

        tM = anom_detect.transactionMapping()

        o = tM.createTransactionTree(dataset = horiz_ds, length=len(horiz_ds))
        print(tM)
        print(o)