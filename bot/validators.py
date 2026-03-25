from typing import Optional

VALID_SIDES = ("BUY", "SELL")
VALID_ORDER_TYPES = ("MARKET", "LIMIT", "STOP_LIMIT")


def validate_symbol(symbol: str) -> str:
    """Validate and normalise a trading-pair symbol (e.g. BTCUSDT)."""
    symbol = symbol.strip().upper()
    if not symbol:
        raise ValueError("Symbol must not be empty.")
    if not symbol.isalpha():
        raise ValueError(
            f"Symbol must contain only letters (got '{symbol}')."
        )
    return symbol


def validate_side(side: str) -> str:
    """Validate order side (BUY / SELL)."""
    side = side.strip().upper()
    if side not in VALID_SIDES:
        raise ValueError(
            f"Side must be one of {VALID_SIDES} (got '{side}')."
        )
    return side


def validate_order_type(order_type: str) -> str:
    """Validate order type (MARKET / LIMIT / STOP_LIMIT)."""
    order_type = order_type.strip().upper()
    if order_type not in VALID_ORDER_TYPES:
        raise ValueError(
            f"Order type must be one of {VALID_ORDER_TYPES} (got '{order_type}')."
        )
    return order_type


def validate_quantity(quantity: float) -> float:
    """Validate that quantity is a positive number."""
    if quantity <= 0:
        raise ValueError(
            f"Quantity must be a positive number (got {quantity})."
        )
    return quantity


def validate_price(price: Optional[float], order_type: str) -> Optional[float]:
    """Validate price — required and positive for LIMIT / STOP_LIMIT orders."""
    if order_type in ("LIMIT", "STOP_LIMIT"):
        if price is None:
            raise ValueError(
                f"Price is required for {order_type} orders."
            )
        if price <= 0:
            raise ValueError(
                f"Price must be a positive number (got {price})."
            )
    return price


def validate_stop_price(
    stop_price: Optional[float], order_type: str
) -> Optional[float]:
    """Validate stop price — required and positive for STOP_LIMIT orders."""
    if order_type == "STOP_LIMIT":
        if stop_price is None:
            raise ValueError("Stop price is required for STOP_LIMIT orders.")
        if stop_price <= 0:
            raise ValueError(
                f"Stop price must be a positive number (got {stop_price})."
            )
    return stop_price
