import pandas as pd
import re

def read_df(file):
    return pd.read_pickle(file)

#def get_mapped_columns(df, mapping):
#    """
#    Retrieves all QBlade columns from the DataFrame that are in the mapping.
#    
#    Args:
#        df (pd.DataFrame): The QBlade DataFrame.
#        mapping (dict): QBlade to OpenFAST column mapping.
#    
#    Returns:
#        pd.DataFrame: DataFrame with only the mapped columns, renamed to OpenFAST names.
#    """
#    # Filter and rename only the columns present in the DataFrame
#    # selected_columns = {k: v for k, v in mapping.items() if k in df.columns}
#    # print(selected_columns)
#    
#    selected_columns = {}
#    for col, v in df.columns:#.get_level_values(0):
#        for pattern, replacement in mapping.items():
#            if re.search(pattern, col):  # Check if column matches regex pattern
#                new_name = re.sub(pattern, replacement, col)  # Replace using regex
#                selected_columns[col] = new_name
#    
#    if not selected_columns:
#        raise KeyError("No matching columns found in the DataFrame.")
#        
#    # Return DataFrame with selected columns renamed to OpenFAST names
#    return df[selected_columns.keys()].rename(columns=selected_columns)

def get_mapped_columns(df, mapping, drop_unmapped=True, verbose=False):
    """
    Applies QBlade to OpenFAST variable name mapping to DataFrame columns.
    Supports both flat and multi-index DataFrames.

    Args:
        df (pd.DataFrame): Input DataFrame.
        mapping (dict): Mapping from QBlade to OpenFAST variable names.
        drop_unmapped (bool): If True, returns only mapped columns. Else, retains all.
        verbose (bool): If True, prints mapping summary.

    Returns:
        pd.DataFrame: Mapped DataFrame.
    """
    matched = []
    unmatched = list(df.columns)

    if isinstance(df.columns, pd.MultiIndex):
        mapped_columns = []
        for col in df.columns:
            original_name = col[0]
            new_name = original_name
            for pattern, repl in mapping.items():
                if re.search(pattern, original_name):
                    new_name = re.sub(pattern, repl, original_name)
                    matched.append(original_name)
                    if original_name in unmatched:
                        unmatched.remove(original_name)
                    break
            mapped_columns.append((new_name, col[1]))
        df.columns = pd.MultiIndex.from_tuples(mapped_columns)

    else:
        rename_dict = {}
        for col in df.columns:
            for pattern, repl in mapping.items():
                if re.search(pattern, col):
                    new_name = re.sub(pattern, repl, col)
                    rename_dict[col] = new_name
                    matched.append(col)
                    if col in unmatched:
                        unmatched.remove(col)
                    break
        if not rename_dict:
            raise KeyError("No matching columns found in the DataFrame.")
        df = df.rename(columns=rename_dict)
        if drop_unmapped:
            df = df[list(rename_dict.values())]

    if verbose:
        print_mapping_summary(matched, unmatched)

    return df

def print_mapping_summary(matched, unmatched):
    """
    Prints summary of matched and unmatched columns for debug purposes.
    """
    print("✔ Matched columns:")
    for col in matched:
        print(f"  - {col}")
    if unmatched:
        print("\n⚠ Unmatched columns:")
        for col in unmatched:
            print(f"  - {col}")

def load_and_map_stats(ss_paths, mapping, drop_unmapped=True, verbose=False):

    stats_raw, stats_mapped = {}, {}

    for i, path in enumerate(ss_paths):
        df = read_df(path)
        stats_raw[i] = df
        stats_mapped[i] = get_mapped_columns(df, mapping, drop_unmapped, verbose)
        
    return stats_raw, stats_mapped

def load_and_map_timeseries(ts_paths, mapping, drop_unmapped=True, verbose=False):

    ts_raw, ts_mapped = {}, {}

    for i, path in enumerate(ts_paths):
        df = read_df(path)
        ts_raw[i] = df
        ts_mapped[i] = get_mapped_columns(df, mapping, drop_unmapped, verbose)
        
    return ts_raw, ts_mapped