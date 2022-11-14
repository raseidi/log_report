def get_variants(df):
    variants = df.groupby(['case_id'])['activity'].apply(list) # transform groupby into list
    variants = variants.apply(lambda x: ','.join(map(str, x))) # transfor list into a unique string
    return sorted(set(variants))

def get_activities(df):
    return sorted(df["activities"].unique())