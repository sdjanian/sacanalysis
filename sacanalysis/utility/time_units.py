def getTimeinSec(time_unit: str) -> int:    
    time_dict = {"micro":1000000,
                 "milli":1000,
                 "second:":1}    
    try:
        return time_dict[time_unit]
    except:
        raise Exception("only valid inputs are: micro, milli, second")
    
    
    
    
    