
# third-party
import pandas as pd


def get_individual_occurrences(df_series, sep):
    '''  Expand occurrences of elements in a column by splitting them by 'sep'. Return a dataframe
    where each column corresponds to the unique elements from the split and the corresponding rows
    have a 1 if the element occurs in that index.

    Parameters
    ---------- 
    df: pd.Series
        Dataframe column with elements to be split by 'sep'. 

    Returns
    -------
    : pd.DataFrame
        Dataframe where each column corresponds to the unique elements from the split 
        and the corresponding rows have a 1 if the element occurs in that index.
    '''

    df_sep = df_series.str.split(sep, expand=True).stack()
    list_rows = []

    for index in range(0, df_sep.index.levshape[0]):
        ind_dict = dict.fromkeys(df_sep.unique())
        for inp in df_sep[index]:
            ind_dict[inp] = 1

        list_rows += [ind_dict]

    df = pd.DataFrame(list_rows)
    df.fillna(0, inplace=True)

    return df
