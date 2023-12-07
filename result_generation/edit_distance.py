import editdistance
import pandas as pd

# Assuming you have a DataFrame named 'data' with 'time' and 'field_to_plot' columns
# Replace 'time' and 'field_to_plot' with your actual column names

# Example dataset creation (replace this with your dataset)


fpath_ref = '../dataset/no_delay_drop/latest_run.csv'

fpath_cmps = ['../dataset/drop_10/latest_run.csv',
              '../dataset/drop_50/latest_run.csv',
              '../dataset/drop_75/latest_run.csv',
              '../dataset/delay_rand_10/latest_run.csv',
              '../dataset/delay_rand_50/latest_run.csv',
              '../dataset/delay_seq_25/latest_run.csv',
              ]

data_ref = pd.read_csv(fpath_ref)

result_cols = ["experiment",'normalized_editdistance']

results = []
for fpath_cmp in fpath_cmps:
    
    data_cmp = pd.read_csv(fpath_cmp)


    arr1 = data_ref['field.pos0']
    arr2 = data_cmp['field.pos0']

    max_distance = len(arr1) + len(arr2)

    normalized_edit_distance = (editdistance.eval(arr1, arr2)/max_distance)

    print("*****************\n")

    print("Current comparison: ",fpath_cmp.split('/')[-2])
    print(normalized_edit_distance )
    
    results.append([fpath_cmp.split('/')[-2],normalized_edit_distance])
    print("\n*****************")
    
    
print("writing to results.csv")

df = pd.DataFrame(results, columns=result_cols)
df.to_csv("./results/results.csv",index=False)