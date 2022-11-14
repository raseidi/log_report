import os
import yaml
import pandas as pd
from typing import Any, Dict, Optional, Union
from config import Settings
from appdirs import user_cache_dir
from log_profiling.descriptions.process_mining import get_variants

class LogProfiling:
    def __init__(
        self,
        df: Optional[pd.DataFrame] = None,
        settings: Union[str, Settings] = None,
        cache: bool = False
    ) -> None:
        
        self.config = self.__initialize_settings(settings)
        self.df = self.__initialize_df(df, self.config)

        if cache:
            if self.config.cache_path in (None, "default"):
                self.config.cache_path = "log_profiling/descriptors.csv"
            self.__cache = self.load_cache(self.config.cache_path)
        
        self._variants = None
        self._activities = None
        self._report = None

    @staticmethod
    def __initialize_settings(settings: Settings = None):
        if settings is None:
            settings = "dataset_config.yaml"
        
        if isinstance(settings, Settings):
            pass
        elif isinstance(settings, str):
            with open(settings) as f:
                data = yaml.safe_load(f)
                settings = Settings(**data)
        else:
            raise TypeError(f"Expected settings to be [str, Settings] type, but {type(settings)} was found.")

        return settings

    @staticmethod
    def __initialize_df(
        df: Optional[pd.DataFrame] = None, cfg: Settings = None
    ) -> pd.DataFrame:
        if df is None:
            df = pd.read_csv(cfg.path)
        df = df.rename(
            columns={
                cfg.features.case_id: "case_id",
                cfg.features.activity: "activity",
                cfg.features.time: "timestamp",
            }
        )
        df["timestamp"] = pd.to_datetime(
            df["timestamp"], infer_datetime_format=True, utc=True
        ).dt.tz_localize(None)
        return df

    @staticmethod # ToDo: persist by decorating functions
    def load_cache(path):
        # using a db might be better?
        if os.path.exists(path):
            cache = pd.read_csv(path)
        else:
            cache = pd.DataFrame()
        return cache

    @property
    def variants(self):
        if self._variants is None:
            self._variants = get_variants(self.df)
        return self._variants
    
    @property
    def activities(self):
        if self._activities is None:
            self._activities = self.df["activity"].unique()
        return self._activities

    def __str__(self) -> str:
        return f"Profiling {self.config.name}"

    def text_report(self, activities=False, variants=False):
        if self.report is None:
            self.report = self._text_report()
        
        
        print(self)
        print("number of cases\t\t", self.df["case_id"].nunique())
        print("number of activities\t\t", len(self.activities))
        print("number of variants\t\t", len(self.variants))
        
        if activities:
            print("unique activities", self.activities)
        if variants:
            print("unique variants", self.variants)
        print("number of events (dataset len)\t\t", len(self.df))

        print("shortest case length\t\t", self.df.groupby(["case_id"]).size().min())
        print("longest case length\t\t", self.df.groupby(["case_id"]).size().max())
        print("average case length\t\t", self.df.groupby(["case_id"]).size().mean())
        print("std case length\t\t", self.df.groupby(["case_id"]).size().std())
        print("median case length\t\t", self.df.groupby(["case_id"]).size().median())
