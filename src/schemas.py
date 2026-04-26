from pydantic import BaseModel
from typing import Optional

class Transaction(BaseModel):
    TransactionID: int
    ProductCD: str
    card1: int
    card2: Optional[float] = None
    card3: Optional[float] = None
    card4: str
    addr1: float
    addr2: float
    TransactionAmt: float
    TransactionDT: float
    P_emaildomain: Optional[str] = None
    R_emaildomain: Optional[str] = None
    D1: Optional[float] = None
    D2: Optional[float] = None
    D3: Optional[float] = None
    D4: Optional[float] = None
    D5: Optional[float] = None
    D6: Optional[float] = None
    D7: Optional[float] = None
    D8: Optional[float] = None
    D9: Optional[float] = None
    D10: Optional[float] = None
    D11: Optional[float] = None
    D12: Optional[float] = None
    D13: Optional[float] = None
    D14: Optional[float] = None
    D15: Optional[float] = None
