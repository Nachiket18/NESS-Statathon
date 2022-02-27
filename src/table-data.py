import anomaly_detection as anom_detect


class Table:

    def __init__(self, entries: dict):
        self.entries = entries #Allows for entries to be pre-imported to table w/o using add_entry

    def add_entry(self, id, lower_range = None, upper_range = None): #Adds a range to the table
        self.entries[id] = [lower_range, upper_range]
    
    def check_data(self, data): #Data - The number you want to check, compare to table ranges
        data = float(data)
        for i in range(len(self.entries)):  #Checks each range until it finds the matching one
            val = list(self.entries.values())[i] # val[0] - Lower Range, val[1] - Upper Range
            if (val[0] is None or data >= val[0]) and \
               (val[1] is None or data <= val[1]): #If data is greater than lower and less than upper
               # (None is when range goes to -inf or inf)

               return list(self.entries.keys())[i] #Return corresponding range id

def csv_to_data(file_path: str):
    
    with open(file_path, "r") as f:

        data = []

        for i in f.readlines():
            data.append(i.split(",")[3:11])
            # Temperature[3] - App. Temperature[4] - Humidty[5] - Wind Speed[6] - Wind Bearing[7] 
            # Visibility[8] - Loud Cover[9] - Pressure[10]

    return data


def de_ser_data(data: list, tables: list):
    pass

if __name__ == "__main__":
    x = csv_to_data("src/weatherHistory.csv")
    x.pop(0)
    test_table = {
        "Low": [None, 20],
        "Normal": [20, 30],
        "High": [30, None]
        }
    t = Table(test_table)

    for i in range(len(x)):
        print(x[i][0], t.check_data(x[i][0]))

    #de_ser_data(x,test_table)
