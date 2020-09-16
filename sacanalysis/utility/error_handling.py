import pandas as pd
def xyTimeVelocityCheck(df:pd.DataFrame):
    xyCheck(df)    
    timeCheck(df)
    if "velocity" in df.columns:
        None
    else:
        raise Exception("Velocity is missing from df")    

def xyVelocityCheck(df:pd.DataFrame):
    xyCheck(df)    
    if "velocity" in df.columns:
        None
    else:
        raise Exception("Velocity is missing from df")    
        
def xyCheck(df:pd.DataFrame):
    if ("x" in df.columns) and ("y" in df.columns):
            None
    else:
        raise Exception("Either column x or y is missing from dataframe")
        
def timeCheck(df:pd.DataFrame):
    if "time" in df.columns:
            None
    else:
        raise Exception("Column time is missing from dataframe")
        
def sourceCheck(df:pd.DataFrame,verboose:int = 1):
    if "source" not in df.columns:
        if verboose == 1:
            print("No source column giving, assuming all data from same recording")
        df["source"] = ["same"] * len(df) 
        return df
    else:
        return df
        

if __name__ == "__main__":
    df_test = pd.DataFrame({"time":[1,2,3],
                            "x":[1,2,3],
                            "y":[1,2,3],
                            "velocity":[1,2,3]}) 
    xyVelocityCheck(df_test)
    df_test = sourceCheck(df_test,verboose=0)
