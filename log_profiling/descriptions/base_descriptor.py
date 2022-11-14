from log_profiling.descriptions.process_mining import get_activities, get_variants


class BaseDescriptor:
    def __init__(self, df) -> None:
        pass

class PMDescriptor(BaseDescriptor):
    def __init__(self, df) -> None:
        super().__init__(df)                
        self.variants = get_variants(df)
        self.activities = get_activities(df)

class GeneralDescriptor(BaseDescriptor):
    def __init__(self, df) -> None:
        super().__init__(df)
        