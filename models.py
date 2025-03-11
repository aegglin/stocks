from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, mapped_column, relationship, sessionmaker

Base = declarative_base()

class StockSymbol(Base):
    __tablename__ = 'stock_symbol'

    stock_symbol_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    stock_symbol = mapped_column(String(4), unique=True, nullable=False)
    long_name = mapped_column(String(50), nullable=False)
    short_name = mapped_column(String(50), nullable=False)

    # Class to be related, name of matching SQLAlchemy column in other table
    # Plural to indicate that a stock symbol can have multiple stock prices (many to one)
    stock_prices = relationship('StockPrice', back_populates='stock_symbol_id')

    def __repr__(self):
        return f"StockSymbol(StockSymbolId={self.stock_symbol_id!r}, StockSymbol={self.stock_symbol!r}, SymbolLongName={self.long_name!r}, SymbolShortName={self.short_name!r})"
    

class StockPrice(Base):
    __tablename__ = 'stock_price'

    stock_price_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    stock_symbol_id = mapped_column(Integer, ForeignKey('stock_symbol.stock_symbol_id'))
    stock_price = mapped_column(Float, nullable=False)

    # Class to be related, name of matching SQLAlchemy column in other table
    # Singular to indicate that a stock price has one stock symbol (one to many)
    stock_symbol = relationship('StockSymbol', back_populates='stock_symbol_id')

    def __repr__(self):
        return f"StockPrice(StockPriceId={self.stock_price_id!r}, StockSymbolId={self.stock_symbol_id!r}), StockPrice={self.stock_price!r}"