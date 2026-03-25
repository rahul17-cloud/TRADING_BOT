import logging
from typing import Optional

from bot.client import BinanceClient

logger = logging.getLogger("trading_bot.orders")



def create_market_order(
    client: BinanceClient,
    symbol: str,
    side: str,
    quantity: float,
) -> dict:
    """Place a MARKET order on Binance Futures Testnet."""
    params = {
        "symbol": symbol,
        "side": side,
        "type": "MARKET",
        "quantity": quantity,
    }
    logger.info(
        "Placing MARKET %s order: %s %s", side, quantity, symbol
    )
    return client.place_order(**params)


def create_limit_order(
    client: BinanceClient,
    symbol: str,
    side: str,
    quantity: float,
    price: float,
) -> dict:
    """Place a LIMIT order (GTC) on Binance Futures Testnet."""
    params = {
        "symbol": symbol,
        "side": side,
        "type": "LIMIT",
        "quantity": quantity,
        "price": price,
        "timeInForce": "GTC",
    }
    logger.info(
        "Placing LIMIT %s order: %s %s @ %s", side, quantity, symbol, price
    )
    return client.place_order(**params)


def create_stop_limit_order(
    client: BinanceClient,
    symbol: str,
    side: str,
    quantity: float,
    price: float,
    stop_price: float,
) -> dict:
    """Place a STOP-LIMIT order (GTC) on Binance Futures Testnet.

    The order becomes a LIMIT order once the ``stop_price`` is reached.
    """
    params = {
        "symbol": symbol,
        "side": side,
        "type": "STOP",
        "quantity": quantity,
        "price": price,
        "stopPrice": stop_price,
        "timeInForce": "GTC",
    }
    logger.info(
        "Placing STOP_LIMIT %s order: %s %s @ %s (stop %s)",
        side, quantity, symbol, price, stop_price,
    )
    return client.place_order(**params)




def format_order_response(response: dict) -> str:
    """Return a human-readable summary of an order response."""
    lines = [
        "─ Order Response ─",
        f"  Order ID    : {response.get('orderId', 'N/A')}",
        f"  Symbol      : {response.get('symbol', 'N/A')}",
        f"  Side        : {response.get('side', 'N/A')}",
        f"  Type        : {response.get('type', 'N/A')}",
        f"  Status      : {response.get('status', 'N/A')}",
        f"  Quantity    : {response.get('origQty', 'N/A')}",
        f"  Executed Qty: {response.get('executedQty', 'N/A')}",
        f"  Price       : {response.get('price', 'N/A')}",
        f"  Avg Price   : {response.get('avgPrice', 'N/A')}",
        f"  Time        : {response.get('updateTime', 'N/A')}",
        "─",
    ]
    return "\n".join(lines)
