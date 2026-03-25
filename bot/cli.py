import argparse
import sys

from bot.logging_config import setup_logging
from bot.validators import (
    validate_symbol,
    validate_side,
    validate_order_type,
    validate_quantity,
    validate_price,
    validate_stop_price,
)
from bot.client import BinanceClient, TradingBotError
from bot.orders import (
    create_market_order,
    create_limit_order,
    create_stop_limit_order,
    format_order_response,
)

logger = None  # set in main()


def build_parser() -> argparse.ArgumentParser:
    """Build and return the CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog="trading_bot",
        description="Place orders on Binance Futures Testnet (USDT-M)",
    )
    parser.add_argument(
        "--symbol",
        required=True,
        help="Trading pair symbol (e.g. BTCUSDT)",
    )
    parser.add_argument(
        "--side",
        required=True,
        help="Order side: BUY or SELL",
    )
    parser.add_argument(
        "--type",
        required=True,
        dest="order_type",
        help="Order type: MARKET, LIMIT, or STOP_LIMIT",
    )
    parser.add_argument(
        "--quantity",
        required=True,
        type=float,
        help="Order quantity (e.g. 0.001)",
    )
    parser.add_argument(
        "--price",
        type=float,
        default=None,
        help="Limit price (required for LIMIT and STOP_LIMIT orders)",
    )
    parser.add_argument(
        "--stop-price",
        type=float,
        default=None,
        dest="stop_price",
        help="Stop price (required for STOP_LIMIT orders)",
    )
    return parser


def print_request_summary(
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: float | None,
    stop_price: float | None,
) -> None:
    """Print a formatted summary of the order request before submission."""
    print("\n─ Order Request Summary ─")
    print(f"  Symbol      : {symbol}")
    print(f"  Side        : {side}")
    print(f"  Type        : {order_type}")
    print(f"  Quantity    : {quantity}")
    if price is not None:
        print(f"  Price       : {price}")
    if stop_price is not None:
        print(f"  Stop Price  : {stop_price}")
    print("─\n")


def main() -> None:
    """Parse arguments, validate, and place the order."""
    global logger
    logger = setup_logging()

    parser = build_parser()
    args = parser.parse_args()


    try:
        symbol = validate_symbol(args.symbol)
        side = validate_side(args.side)
        order_type = validate_order_type(args.order_type)
        quantity = validate_quantity(args.quantity)
        price = validate_price(args.price, order_type)
        stop_price = validate_stop_price(args.stop_price, order_type)
    except ValueError as exc:
        logger.error("Validation error: %s", exc)
        print(f"\n❌ Validation error: {exc}")
        sys.exit(1)

    print_request_summary(symbol, side, order_type, quantity, price, stop_price)

    try:
        client = BinanceClient()

        if order_type == "MARKET":
            response = create_market_order(client, symbol, side, quantity)
        elif order_type == "LIMIT":
            response = create_limit_order(client, symbol, side, quantity, price)
        elif order_type == "STOP_LIMIT":
            response = create_stop_limit_order(
                client, symbol, side, quantity, price, stop_price
            )
        else:
            
            raise TradingBotError(f"Unsupported order type: {order_type}")

        print(format_order_response(response))
        logger.info("Order placed successfully (orderId=%s)", response.get("orderId"))
        print("✅ Order placed successfully!\n")

    except TradingBotError as exc:
        logger.error("Order failed: %s", exc)
        print(f"\n❌ Order failed: {exc}\n")
        sys.exit(1)

    except Exception as exc:
        logger.exception("Unexpected error: %s", exc)
        print(f"\n❌ Unexpected error: {exc}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
