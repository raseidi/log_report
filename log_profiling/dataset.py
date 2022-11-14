import yaml
from typing import Any, Optional
import pandas as pd
from config import Settings
from log_profiling.descriptions.process_mining import get_variants


class Dataset:
    def __init__(self, df: pd.DataFrame = None, cfg: Settings = None) -> None:
        if cfg is None:
            with open("dataset_config.yaml") as f:
                data = yaml.safe_load(f)
                cfg = Settings(**data)

        self.cfg = cfg
        self.df = self.__initialize_df(df, self.cfg)

        self._variants = None
        self._activities = None


    def __str__(self) -> str:
        return f"Dataset {self.name}"

    def __getitem__(self, name):
        if name in self.df.columns:
            return self.df[name]
        else:
            raise KeyError(name)

    def __len__(self):
        return len(self.df)

    @property
    def name(self):
        return self.cfg.name

    @property
    def columns(self):
        return self.df.columns