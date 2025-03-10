from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, mapped_column, relationship, sessionmaker

Base = declarative_base()

class StockSymbol(Base):
    __tablename__ = 'stock_symbol'

    stock_symbol_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    stock_symbol = mapped_column(String(4), unique=True, nullable=False)

    def __repr__(self):
        return f"StockSymbol(StockSymbolId={self.stock_symbol_id!r}, StockSymbol={self.stock_symbol!r})"
    

class StockPrices(Base):
    __tablename__ = 'stock_price'

    stock_price_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    stock_symbol_id = mapped_column(Integer, ForeignKey('stock_symbol.stock_symbol_id'))
    stock_price = mapped_column(Float, nullable=False)

    stock_symbol = relationship("stock_symbol")

    def __repr__(self):
        return f"StockPrice(StockPriceId={self.stock_price_id!r}, StockSymbolId={self.stock_symbol_id!r}), StockPrice={self.StockPrice!r}"