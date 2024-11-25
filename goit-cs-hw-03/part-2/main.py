from pymongo import MongoClient

# Підключення до MongoDB
client = MongoClient(
    # Connection string here
    "mongodb+srv://<username>:<password>@krabaton.5mlpr.gcp.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
)
db = client.book

# Функції CRUD

# 1. Створення запису (Create)
def create_cat(name, age, features):
    result = db.cats.insert_one({"name": name, "age": age, "features": features})
    print(f"Додано кота з ID: {result.inserted_id}")

# 2. Читання всіх записів (Read all)
def read_all_cats():
    cats = db.cats.find({})
    for cat in cats:
        print(cat)

# 3. Читання запису за ім'ям (Read by name)
def read_cat_by_name(name):
    cat = db.cats.find_one({"name": name})
    if cat:
        print(cat)
    else:
        print(f"Кота з ім'ям '{name}' не знайдено.")

# 4. Оновлення віку кота за ім'ям (Update age)
def update_cat_age(name, new_age):
    result = db.cats.update_one({"name": name}, {"$set": {"age": new_age}})
    if result.modified_count > 0:
        print(f"Вік кота '{name}' оновлено до {new_age} років.")
    else:
        print(f"Кота з ім'ям '{name}' не знайдено.")

# 5. Додавання нової характеристики до кота (Update features)
def add_cat_feature(name, feature):
    result = db.cats.update_one({"name": name}, {"$addToSet": {"features": feature}})
    if result.modified_count > 0:
        print(f"Характеристика '{feature}' додана коту '{name}'.")
    else:
        print(f"Кота з ім'ям '{name}' не знайдено.")

# 6. Видалення запису за ім'ям (Delete by name)
def delete_cat_by_name(name):
    result = db.cats.delete_one({"name": name})
    if result.deleted_count > 0:
        print(f"Кіт з ім'ям '{name}' видалений.")
    else:
        print(f"Кота з ім'ям '{name}' не знайдено.")

# 7. Видалення всіх записів (Delete all)
def delete_all_cats():
    result = db.cats.delete_many({})
    print(f"Видалено {result.deleted_count} записів.")

# Тестові виклики функцій
if __name__ == "__main__":
    # Створення нових записів
    create_cat("barsik", 3, ["ходить в капці", "дає себе гладити", "рудий"])
    create_cat("Lama", 2, ["ходить в лоток", "не дає себе гладити", "сірий"])

    # Читання записів
    print("\nВсі коти:")
    read_all_cats()

    print("\nПошук кота по імені 'barsik':")
    read_cat_by_name("barsik")

    # Оновлення записів
    print("\nОновлення віку 'barsik':")
    update_cat_age("barsik", 4)

    print("\nДодавання характеристики 'любить молоко' для 'barsik':")
    add_cat_feature("barsik", "любить молоко")

    # Видалення записів
    print("\nВидалення кота з ім'ям 'Lama':")
    delete_cat_by_name("Lama")

    print("\nВидалення всіх котів:")
    delete_all_cats()