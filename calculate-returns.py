# Python script to calculate the pension fund for mutual funds
import pandas as pd

# Import the dataframe from excel file
df_pension = pd.read_excel('./data/16-Apr-2021.xls', header=None)

# Calculate the rows in third column where the value is NaN
missing_list = list(df_pension.index[df_pension[df_pension.columns[3]].isna()])

# Split dataframes using the missing_list
def split_dfs(input_df, indice_list):
    dfs_list = []
    for (ind_num, index_val) in enumerate(indice_list):
        if ind_num == 0:
            dfs_list.append(input_df[0:index_val])
        elif ind_num == len(indice_list)-1:
            dfs_list.append(input_df[indice_list[ind_num-1]+1:index_val])
            dfs_list.append(input_df[index_val+1:])
        else:
            dfs_list.append(input_df[indice_list[ind_num-1]+1:index_val])
    return dfs_list


def clean_table_names(input_df):
    input_df = input_df.reset_index(drop=True)
    # Extract scheme name and remove unnecessary columns
    scheme_name = input_df[2][0].strip()
    input_df = input_df.iloc[:, 3:]
    # Clean the first row - remove space characters
    first_row = input_df.iloc[0]
    first_row = [x.replace('\n', '') for x in first_row]
    # Change the column names to the first row
    # and remove the first row
    input_df.columns = first_row
    input_df = input_df.iloc[1:]
    return scheme_name, input_df

# Calculate the returns using values of NAV
def calculate_returns_formula(input_df):
    # New columns for the dataframe
    input_df['Returns 1 Year value'] = input_df['NAV'] - input_df['NAV'] * (1 - input_df['Returns 1 Year'])
    input_df['Returns 3 Years value'] = input_df['NAV'] - input_df['NAV'] * (1 - input_df['Returns 3 Years'])
    input_df['Returns 5 Years value'] = input_df['NAV'] - input_df['NAV'] * (1 - input_df['Returns 5 Years'])
    input_df['Returns 7 Years value'] = input_df['NAV'] - input_df['NAV'] * (1 - input_df['Returns 7 Years'])
    input_df['Returns 10 Years value'] = input_df['NAV'] - input_df['NAV'] * (1 - input_df['Returns 10 Years'])
    return input_df

# Split the dataframes using the split_dfs function
dfs_list = split_dfs(df_pension, missing_list)
# Clean the table for each dataframe
dfs_list = [clean_table_names(each_df) for each_df in dfs_list]
# Consider which columns to choose in desired_col_names
desired_col_names = []
dfs_dict = {scheme_name: calculate_returns_formula(cleaned_df) for (scheme_name, cleaned_df) in dfs_list}

# # Pick only the desired columns
# def get_required_col(input_df, desired_col_names):
#     return input_df[[desired_col_names]]


# TODO Plot the values
