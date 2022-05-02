
from table_data import csv_to_data, json_to_tables, discretize_data


def predict_policy(test_data):

    x = csv_to_data("E:/Weather_AnomalyDetection/src/data/train.csv", [ (6, 7), #age, len.at.res
                                        (11, 11), #premiums
                                        (15, 17) #adults, children,tenure
                                        ])
    y = csv_to_data("E:/Weather_AnomalyDetection/src/data/train.csv", [ (5,5), #age, len.at.res
                                        (8, 10), #premiums
                                        (18,18) #adults, children,tenure
                                        ])

    col_names = x[0] + y[0]
    x.pop(0)
    y.pop(0)

    tgg = json_to_tables("E:/Weather_AnomalyDetection/src/data/train.json")
    #tgg.process_all()

    #print([x.entries for x in tgg.tables])
    print(tgg.__dict__)
    #print(x)

    discrete_processed_data = []
    for i in range(10):
        print(x[i])
        dis_test = discretize_data(x[i], tgg)
        #print(x[i])
        
        print(dis_test + y[i])
        dis_test = dis_test + y[i]

        discrete_processed_data.append(dis_test)
    print(discrete_processed_data)

    for i in range(0,len(discrete_processed_data)):
        tmp_data = discrete_processed_data[i]
            
