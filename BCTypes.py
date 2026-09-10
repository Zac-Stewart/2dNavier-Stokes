from enum import Enum

class BCType(Enum): #not using ENUMs
    NONE = 0     
    NO_SLIP = 1
    FREE_SLIP = 2
    INFLOW = 3
    OUTFLOW = 4
    