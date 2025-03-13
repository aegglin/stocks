from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, mapped_column, relationship, sessionmaker

Base = declarative_base()

class StockSymbol(Base):
    __table_args__ = {'schema': 'Dim'}
    __tablename__ = 'StockSymbols'

    StockSymbolId = mapped_column(Integer, primary_key=True, autoincrement=True)
    Symbol = mapped_column(String(5), unique=True, nullable=False)
    LongName = mapped_column(String(50), nullable=False)
    ShortName = mapped_column(String(50), nullable=False)

    # Class to be related, name of matching SQLAlchemy column in other table
    # Plural to indicate that a stock symbol can have multiple stock prices (many to one)
    # stock_prices = relationship('StockPrice', back_populates='stock_symbol_id')
    # stock_prices = relationship('stock_price')

    def __repr__(self):
        return f"StockSymbol(StockSymbolId={self.StockSymbolId!r}, StockSymbol={self.Symbol!r}, SymbolLongName={self.LongName!r}, SymbolShortName={self.ShortName!r})"
    

class StockPrice(Base):
    __table_args__ = {'schema': 'Fact'}
    __tablename__ = 'stock_price'

    stock_price_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    date_id = mapped_column(Integer, ForeignKey('dates.date_id'))
    stock_symbol_id = mapped_column(Integer, ForeignKey('stock_symbol.stock_symbol_id'))
    stock_price = mapped_column(Float, nullable=False)

    # Class to be related, name of matching SQLAlchemy column in other table
    # Singular to indicate that a stock price has one stock symbol (one to many)
    stock_symbol = relationship('StockSymbol', back_populates='stock_symbol_id')
    # stock_symbol = relationship('stock_symbol')
    dates = relationship('dates')

    def __repr__(self):
        return f"StockPrice(StockPriceId={self.stock_price_id!r}, StockSymbolId={self.stock_symbol_id!r}), StockPrice={self.stock_price!r}"


class Date(Base):
    __table_args__ = {'schema': 'Dim'}
    __tablename__ = 'dates'

    date_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    date = mapped_column(DateTime, nullable=False)
    year = mapped_column(Integer, nullable=False)
    month = mapped_column(Integer, nullable=False)
    day = mapped_column(Integer, nullable=False)

    def __repr__(self):
        return f"Date(DateId={self.date_id!r}, Date={self.date}, Year={self.year}, Month={self.month}, Day={self.Day})"