"""
event.py - Base class for an Event object
"""

class Event(object):
    """
    Event is base class providing an interface for all subsequent
    (inherited) events that will trigger further events in the
    trading infrastructure.
    """
    pass


class MarketEvent(Event):
    """
    MarketEvent handles the event of receiving a new market update with
    corresponding bars.
    """
    def __init__(self):
        """
        Initializes the MarketEvent
        """
        self.type = "MARKET"

class SignalEvent(Event):
    """
    SignalEvent handles the event of sending a Signal from a Strategy object.
    This is received by a Portfolio object and acted upon.
    """
    def __init__(self,
                 strategy_id: int,
                 symbol: str,
                 datetime, signal_type, strength):
        """
        Initialize the SignalEvent.

        Parameters:
        strategy_id - The unique identifier for the strategy that
                      generated the signal.
        symbol - The ticker symbol, e.g. 'GOOG'
        datetime - The timestamp at which the signal was generated.
        signal_type - 'LONG' and 'SHORT'
        strength - An adjustment factor "suggestion" used to scale
                   quantity at the portfolio level. Useful for pairs strategies.
        """
        self.type = "SIGNAL"
        self.strategy_id = strategy_id
        self.symbol = symbol
        self.datetime = datetime
        self.signal_type = signal_type
        self.strength = strength

class OrderEvent(Event):
    """
    OrderEvent handles the event of sending an Order to an execution system.
    The order contains a symbol (e.g. GOOG), a type (market or limit),
    quantity and a direction.
    """
    def __init__(self, symbol, order_type, quantity, direction):
        """
        Initialize the order type, setting whether it is a Market order ('MKT')
        or Limit order ('LMT'), has a quantity (integer) and its direction
        ('BUY' or 'SELL').

        Parameters:
        symbol - The instrument to trade.
        order_type - 'MKT' or 'LMT' for Market order or Limit order
        quantity - Non-negative integer for quantity.
        direction - 'BUY' or 'SELL' for long or short.
        """
        self.type = 'ORDER'
        self.symbol = symbol
        self.order_type = order_type
        self.quantity = quantity
        self.direction = direction

    def print_order(self):
        """
        Outputs the values within the Order.
        """
        print(
            "Order: Symbol={:}, Type={:}, Quantity={:}, Direction={:}".format(self.symbol,
                                                                              self.order_type,
                                                                              self.quantity,
                                                                              self.direction)
        )


class FillEvent(Event):
    """
    FillEvent encapsulates the notion of a Filled Order, as returned
    from a brokerage. Stores the quantity of an instrument actually
    filled and at what price. In addition, store the commission of the
    trade from the brokerage.
    """
    def __init__(self, timeindex, symbol, exchange, quantity, direction
                 fill_cost, commission=None):
        """
        Initializes the FillEvent object. Sets the symbol, exchange, quantity,
        direction, cost of fill and an optional commission.

        If commission if not provided, the Fill object will calculate it based
        on the trade size and Interactive Brokers fees.

        Parameters:
        timeindex - The bar-resolution when the order was filled.
        symbol - The instrument which was filled.
        exchange - The exchange where the order was filled.
        quantity - The filled quantity.
        direction - The direction of fill ('BUY' or 'SELL')
        fill_cost - The holdings value in dollars.
        commission - An optinal commision sent from the brokerage.
        """
        self.type = 'FILL'
        self.timeindex = timeindex
        self.symbol = symbol
        self.exchange = exchange
        self.quantity = quantity
        self.direction = direction
        self.fill_cost = fill_cost

        # Calculate commission
        if commission is None:
            self.commission = self.calculate_ib_commission()
        else:
            self.commission = commission

    def calculate_ib_commision(self):
        """
        Calculates the fess of trading based on an Interactive Brokers
        fee structure for API, in USD.

        This does not include exchange or ECN fees.
        """
        full_cost = 1.3
        if self.quantity <= 500:
            full_cost = max(1.3, 0.013*self.quantity)
        else:
            full_cost = max(1.3, 0.008*self.quantity)
        return full_cost