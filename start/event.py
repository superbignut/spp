# One of our goals with an event-driven trading system is to minimise duplication of code between the backtesting element and the live execution element. 
# 尽可能的减少回测框架和实盘交易的gap

# In order for this to work the Strategy object which generates the Signals, and the Portfolio object which provides Orders based on them, must utilise an 
# identical interface to a market feed for both historic and live running.
# 生成信号的Strategy object，和基于信号提供订单的Portfolio object需要使用回测和实盘的同一个接口


class Event:
    """
    Event is base class providing an interface for all subsequent (inherited) events, 
    that will trigger further events in the trading infrastructure.   
    """
    pass

class MarketEvent(Event):
    """
    Handles the event of receiving a new market update with corresponding bars.
    """
    
    def __init__(self) -> None:
        """
        Initialises the MarketEvent.
        """
        super().__init__()
        self.type = 'MARKET'
        
class SignalEvent(Event): # 处理从策略对象发送的信号，被投资组合对象接收
    """
    Handles the event of sending a Signal from a Strategy object. 
    This is received by a Portfolio object and acted upon.
    """
    
    def __init__(self, symbol, datetime, signal_type) -> None:
        """
        Initialises.
        Args:
            symbol (_type_): The ticker symbol
            datetime (_type_): The timestamp at which signal was generated
            signal_type (_type_): 'Long' or 'Short'
        """
        super().__init__()
        self.type = "SIGNAL"
        self.symbol = symbol
        self.datetime = datetime
        self.signal_type = signal_type
        
class OrderEvent(Event): # 将订单发送给执行系统
    """
    Handles the event of sending an Order to an execution system. 
    The order contains a symbol (e.g. GOOG), a type (market or limit),
    quantity and a direction.
    """
    
    def __init__(self, symbol, order_type, quantity, direction) -> None:
        """
        Initialises the order type, setting whether it is a Market order ('MKT') or Limit order ('LMT'), has
        a quantity (integral) and its direction ('BUY' or 'SELL').
        Args:
            symbol (_type_): The instrument to trade
            quantity (_type_): 'MKT' or 'LMT' for Market or Limit
            direction (_type_): 'BUY' or 'SELL' for long or short
        """
        super().__init__()
        self.type = 'ORDER'
        self.symbol = symbol 
        self.order_type = order_type
        self.quantity = quantity
        self.direction = direction
    
    def print_order(self):
        """
        Output the values within the Order
        """
        print("Order: Symbol={0:s}, Type:{0:s}, Quantity={0:s},Direction={0:s}".format(self.symbol,\
                self.order_type, self.quantity, self.direction))
        
class FillEvent(Event): # 已成交的订单信息
    """
    Encapsulates the notion of a Filled Order, as returned from a brokerage. 
    Stores the quantity of an instrument actually filled and at what price. 
    In addition, stores the commission of the trade from the brokerage.
    """

    def __init__(self, timeindex, symbol, exchange, quantity, 
                direction, fill_cost, commission = None) -> None:
        """
        Initialises the FillEvent object. Sets the symbol, exchange,
        quantity, direction, cost of fill and an optional commission.
        
        If commission is not provided, the Fill object will
        calculate it based on the trade size and Interactive
        Brokers fees.
        Args:
            timeindex (_type_): The bar-resolution when the order was filled.
            symbol (_type_): The instrument was filled.
            exchange (_type_): The exchange where the order was filled.
            quantity (_type_): The filled quantity.
            direction (_type_): The direction of fill ('BUY' or 'SELL') 
            fill_cost (_type_): The holdings value in dollars.
            commission (_type_, optional): _description_. Defaults to None.
        """
        super().__init__()
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
    
    def calculate_ib_commission(self):
        """
        Calculates the fees of trading based on an Interactive
        Brokers fee structure for API, in USD.

        This does not include exchange or ECN fees.

        Based on "US API Directed Orders":
        https://www.interactivebrokers.com/en/index.php?f=commission&p=stocks2
        """

        full_cost = 1.3
        if self.quantity <= 500:
            full_cost = max(1.3, 0.013 * self.quantity)
        else:
            full_cost = max(1.3, 0.008 * self.quantity)
        full_cost = min(full_cost, 0.5 / 100.0 * self.quantity * self.fill_cost)
        return full_cost
    