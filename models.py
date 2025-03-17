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

    # Class name to be related, name of matching SQLAlchemy column in other table, back_populates is the name of the relationship in the other class
    stock_prices = relationship('StockPrice', back_populates='stock_symbol')

    def __repr__(self):
        return f"StockSymbol(StockSymbolId={self.StockSymbolId!r}, StockSymbol={self.Symbol!r}, SymbolLongName={self.LongName!r}, SymbolShortName={self.ShortName!r})"


class StockPrice(Base):
    __table_args__ = {'schema': 'Fact'}
    __tablename__ = 'StockPrices'

    StockPriceId = mapped_column(Integer, primary_key=True, autoincrement=True)
    DateId = mapped_column(Integer, ForeignKey('Dim.Dates.Date'))

    # Foreign key refers to the tablename, not the class. Must have the schema in the relationship
    StockSymbolId = mapped_column(Integer, ForeignKey('Dim.StockSymbols.StockSymbolId'))
    StockPrice = mapped_column(Float, nullable=False)

    # Class name to be related, name of matching SQLAlchemy column in other table, back_populates is the name of the relationship
    stock_symbol = relationship('StockSymbol', back_populates='stock_prices')
    dates = relationship('Date', back_populates='stock_prices')

    def __repr__(self):
        return f"StockPrice(StockPriceId={self.StockPriceId!r}, StockSymbolId={self.StockSymbolId!r}), StockPrice={self.StockPrice!r}"


class Date(Base):
    __table_args__ = {'schema': 'Dim'}
    __tablename__ = 'Dates'

    DateId = mapped_column(Integer, primary_key=True, autoincrement=True)
    Date = mapped_column(DateTime, nullable=False)
    Year = mapped_column(Integer, nullable=False)
    Month = mapped_column(Integer, nullable=False)
    Day = mapped_column(Integer, nullable=False)
    Month = mapped_column(String(9), nullable=False)
    WeekDay = mapped_column(String(9), nullable=False)

    # Class name to be related, name of matching SQLAlchemy column in other table, back_populates is the name of the relationship
    stock_prices = relationship('StockPrice', back_populates='dates')

    def __repr__(self):
        return f"Date(DateId={self.DateId!r}, Date={self.Date}, Year={self.Year}, Month={self.Month}, Day={self.Day}, MonthName={self.MonthName}, WeekDay={self.WeekDay})"