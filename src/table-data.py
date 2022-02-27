import anomaly_detection as anom_detect
import json


class Table:

    def __init__(self, entries: dict):
        self.entries = entries #Allows for entries to be pre-inputted to table w/o using add_entry

    def add_entry(self, id, lower_range = None, upper_range = None): #Adds a range to the table
        self.entries[id] = [lower_range, upper_range]
    
    def check_data(self, data: float): #Data - The number you want to check, compare to table ranges
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
    x = csv_to_data("src/data/weatherHistory.csv", (4, 11))
    x.pop(0)

    tgg = json_to_tables("src/data/tables_test.json")

    test_table = { #Temp.
        "Low": [None, 20],
        "Normal": [20, 30],
        "High": [30, None]
        }
    test_table2 = { #Approx. Temp.
        "Low": [None, 20],
        "Normal": [20, 30],
        "High": [30, None]
        }
    test_table3 = { #Humidity
        "Lo-Hu": [0.0, 0.3],
        "Normal": [0.3, 0.7],
        "Damp": [0.7, 1]
        }

    t1 = Table(test_table)
    t2 = Table(test_table2)
    t3 = Table(test_table3)

    tg = TableGroup([t1, t2, t3])

    #for i in range(len(x)):
    #    print(x[i][0], t.check_data(x[i][0]))

    for i in range(len(x)):
        print(x[i][0:3], discretize_data(x[i][0:3], tgg))
        #tg.check_datas(x[i][0:3])
    #de_ser_data(x,test_table)
