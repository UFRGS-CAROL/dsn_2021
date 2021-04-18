#!/usr/bin/python3
import pandas as pd
import numpy as np

micros_float = ["FADD", "FMUL", "FFMA", "FSIN", "FEXP"]
micros_int = ["IADD", "IMUL", "IMAD"]
inputs_float = ["small", "common", "big"]
inputs_int = ["small", "mid", "large"]
error_sites = ["execution_units", "pipeline", "scheduler"]


data_path = "./data"

defined_nan_and_inf = [np.nan, np.inf, -np.inf]

final_list = list()
for precision in ["int", "float"]:
    for error_site in error_sites:
        error_site_df = pd.read_csv(f"{data_path}/raw_data_{error_site}.csv")
        inf_and_nan_exec = error_site_df.isin(defined_nan_and_inf).any(1)

        # Select the non nan and inf
        error_site_df.loc[inf_and_nan_exec, 'valid'] = 0
        error_site_df.loc[~inf_and_nan_exec, 'valid'] = 1

        percentage_of_invalids = 1 - error_site_df[
            error_site_df.precision == precision].valid.sum() / error_site_df[
            error_site_df.precision == precision].valid.shape[0]

        print(f"{precision} - {error_site} percentage of inf/nan", percentage_of_invalids)
        micros = micros_float if precision == "float" else micros_int
        for micro in micros:
            for input_type in inputs_float:
                selected_df = error_site_df[
                    (error_site_df.precision == precision) &
                    (error_site_df.micro == micro) &
                    (error_site_df.input_size == input_type) &
                    (error_site_df.valid == 1)
                    ]

                final_list.append(
                    {
                        "precision": precision,
                        "error_site": error_site,
                        "micro": micro,
                        "input_type": input_type,
                        "min_relative_error": selected_df.relative_diff.min(),
                        "max_relative_error": selected_df.relative_diff.max(),
                        "median_relative_error": selected_df.relative_diff.median()
                    }
                )


final_df = pd.DataFrame(final_list)
