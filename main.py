import connect_options as opt
from sqlalchemy.orm import sessionmaker
from models import *
import json


DSN = f'postgresql://{opt.user}:{opt.password}@{opt.ip}:{opt.port}/{opt.database}'

# Задание №2
def Task2LoadData(engine):

    create_tables(engine)
    session = sessionmaker(bind=engine)()
    publisher1 = Publisher(name="Пушкин")
    publisher2 = Publisher(name="Лермонтов")
    publisher3 = Publisher(name="Гоголь")

    book1 = Book(title="Евгений Онегин", publisher_fk2=publisher1)
    book2 = Book(title="Руслан и Людмила", publisher_fk2=publisher1)
    book3 = Book(title="Герой нашего времени", publisher_fk2=publisher2)
    book4 = Book(title="Бородино", publisher_fk2=publisher2)
    book5 = Book(title="Мертвые души", publisher_fk2=publisher3)
    book6 = Book(title="Вий", publisher_fk2=publisher3)

    shop1 = Shop(name="Мир книги")
    shop2 = Shop(name="Дом книги")
    shop3 = Shop(name="Книжный мир")

    stock1 = Stock(shop_fk=shop1, book_fk=book1, count=1)
    stock2 = Stock(shop_fk=shop1, book_fk=book4, count=1)
    stock3 = Stock(shop_fk=shop2, book_fk=book2, count=1)
    stock4 = Stock(shop_fk=shop2, book_fk=book5, count=1)
    stock5 = Stock(shop_fk=shop3, book_fk=book3, count=1)
    stock6 = Stock(shop_fk=shop3, book_fk=book6, count=1)

    sale1 = Sale(price=100, date_sale='01.10.2023', stock_fk=stock1, count=1)
    sale2 = Sale(price=150, date_sale='02.10.2023', stock_fk=stock2, count=1)
    sale3 = Sale(price=200, date_sale='03.10.2023', stock_fk=stock3, count=1)
    sale4 = Sale(price=250, date_sale='04.10.2023', stock_fk=stock4, count=1)
    sale5 = Sale(price=300, date_sale='05.10.2023', stock_fk=stock5, count=1)
    sale6 = Sale(price=350, date_sale='06.10.2023', stock_fk=stock6, count=1)

    session.add_all([publisher1, publisher2, publisher3])
    session.add_all([book1, book2, book3, book4, book5, book6])
    session.add_all([shop1, shop2, shop3])
    session.add_all([stock1, stock2, stock3, stock4, stock5, stock6])
    session.add_all([sale1, sale2, sale3, sale4, sale5, sale6])
    session.commit()
    session.close()


# Задание №3
def Task3LoadData(engine):
    create_tables(engine)
    session = sessionmaker(bind=engine)()
    with open('fixtures/tests_data.json', 'r') as fd:  # у меня windows
        data = json.load(fd)

    for record in data:
        model_dict = {
            'publisher': Publisher,
            'shop': Shop,
            'book': Book,
            'stock': Stock,
            'sale': Sale,
        }
        model_class = model_dict.get(record.get('model'))
        model_object = model_class(**record.get('fields'))
        session.add(model_object)
    session.commit()
    session.close()


def search_query(engine, search_publisher):
    # Запрос выборки магазинов, продающих целевого издателя
    session = sessionmaker(bind=engine)()
    q = session.query(Sale).join(Sale.stock_fk).join(Stock.shop_fk).join(Stock.book_fk).join(Book.publisher_fk2)
    if search_publisher.isdigit():
        q = q.filter(Publisher.id == search_publisher)
    else:
        q = q.filter(Publisher.name == search_publisher)
    for s in q.all():
        print(s.stock_fk.book_fk.title, s.stock_fk.shop_fk.name, s.price, s.date_sale.strftime("%d-%m-%Y"), sep='|')
    session.close()

engine = sq.create_engine(DSN)

print('Задание №2')
Task2LoadData(engine)
print('Поиск по имени: ')
search_query(engine, 'Лермонтов')
print('Поиск по ID: ')
search_query(engine, '3')
print('')
print('Задание №3')
Task3LoadData(engine)
search_query(engine, 'No starch press')
print('')
print('Задание №2 ручной ввод')
Task2LoadData(engine)
search_query(engine, input('Введите имя писателя: '))