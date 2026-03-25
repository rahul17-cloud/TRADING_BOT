import logging
import os

from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException
from dotenv import load_dotenv

logger = logging.getLogger("trading_bot.client")

TESTNET_BASE_URL = "https://testnet.binancefuture.com"


class TradingBotError(Exception):
    """Custom exception for trading bot errors."""
    pass


class BinanceClient:
    """Wrapper around the python-binance Client for Futures Testnet."""

    def __init__(self) -> None:
        load_dotenv()

        api_key = os.getenv("BINANCE_API_KEY")
        api_secret = os.getenv("BINANCE_API_SECRET")

        if not api_key or not api_secret:
            raise TradingBotError(
                "BINANCE_API_KEY and BINANCE_API_SECRET must be set in a .env "
                "file or environment variables."
            )

        self._client = Client(
            api_key,
            api_secret,
            testnet=True,
        )
        self._client.FUTURES_URL = TESTNET_BASE_URL + "/fapi"

        logger.info("Binance Futures Testnet client initialised.")

    def place_order(self, **params) -> dict:
        """Place a futures order and return the API response dict.

        Parameters are forwarded verbatim to ``client.futures_create_order``.
        Raises ``TradingBotError`` on any API or network failure.
        """
        logger.debug("Order request params: %s", params)

        try:
            response = self._client.futures_create_order(**params)
            logger.debug("Order response: %s", response)
            return response

        except BinanceAPIException as exc:
            logger.error(
                "Binance API error [%s]: %s", exc.status_code, exc.message
            )
            raise TradingBotError(
                f"Binance API error ({exc.status_code}): {exc.message}"
            ) from exc

        except BinanceRequestException as exc:
            logger.error("Binance request error: %s", exc)
            raise TradingBotError(
                f"Binance request error: {exc}"
            ) from exc

        except Exception as exc:
            logger.error("Unexpected error placing order: %s", exc)
            raise TradingBotError(
                f"Unexpected error: {exc}"
            ) from exc
