import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

# Assuming you have a DataFrame named 'data' with 'time' and 'field_to_plot' columns
# Replace 'time' and 'field_to_plot' with your actual column names

# Example dataset creation (replace this with your dataset)


fpath_ref = '../dataset/no_delay_drop/latest_run.csv'
fpath_cmp = '../dataset/drop_50/latest_run.csv'

data_ref = pd.read_csv(fpath_ref)
data_cmp = pd.read_csv(fpath_cmp)

experiment = fpath_cmp.split('/')[-2]


# Subtracting start time for data_ref
start_t_ref = data_ref['%time'][0]
data_ref['%time'] -= start_t_ref

# Subtracting start time for data_cmp
start_t_cmp = data_cmp['%time'][0]
data_cmp['%time'] -= start_t_cmp

print('normal completion time ',data_ref['%time'].iloc[-1]/1e9)
print('50ms delay completion time ',data_cmp['%time'].iloc[-1]/1e9)

# Plotting data_ref
sns.lineplot(x='%time', y='field.pos0', data=data_ref.iloc[5000:6000], label='normal_operation')

# Overlaying plot for data_cmp
sns.lineplot(x='%time', y='field.pos0', data=data_cmp.iloc[5000:6000], label=experiment)


# # Plotting data_ref
# sns.lineplot(x='%time', y='field.pos0', data=data_ref, label='normal_operation')

# # Overlaying plot for data_cmp
# sns.lineplot(x='%time', y='field.pos0', data=data_cmp, label=experiment)



# Set plot title and labels
plt.title('Comparison of Packet Loss Induced Execution with Normal Execution')
plt.xlabel('Time')
plt.ylabel('End Effector Position 0')

# Show legend
plt.legend()

plt.savefig(f'./results/{experiment}.png')

# Display the plot
plt.show()