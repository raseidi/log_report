import pandas as pd


def describe_dataset(df):
    """
    Returns an overview of the provided dataset
    """
    return {
        "columns" "case_id": "case_id",
        "activity": "activity",
        "timestamp": "timestamp",
        "variables": {
            "categorical": [
                "org:resource",
            ],
            "numerical": [
                "org:resource_2",
            ],
            "timestamp": [
                "other_time_column",
            ],
        },
        "dataset": {
            "n_cases": df["case_id"].nunique(),
            "n_activities": df["activity"].nunique(),
            "n_events": len(df),
        },
        "trace_info": {
            "length": {
                "min": df.groupby(["case:concept:name"]).size().min(),
                "max": df.groupby(["case:concept:name"]).size().max(),
                "mean": df.groupby(["case:concept:name"]).size().mean(),
                "std": df.groupby(["case:concept:name"]).size().std(),
                "median": df.groupby(["case:concept:name"]).size().median(),
            },
        }
    }
