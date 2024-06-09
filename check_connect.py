from pymilvus import connections, utility, Collection, FieldSchema, CollectionSchema, DataType

"""Создание коллекции: Пользователь создает коллекцию в Milvus. 
Информация о коллекции сохраняется в etcd. 
Вставка данных: Пользователь вставляет данные в коллекцию. 
Данные сегментов сохраняются в MinIO, а информация о сегментах и их местоположении - в etcd. 
Создание индекса: Пользователь создает индекс для коллекции. Информация об индексе сохраняется в etcd. 
Поиск: Пользователь выполняет поиск по коллекции. Milvus использует данные из MinIO и метаданные из etcd для выполнения запроса. """

# Подключение к Milvus
connections.connect(
    alias="default",
    host="127.0.0.1",  # Адрес хоста
    port="19530"  # Порт Milvus
)

# Проверка подключения: получение информации о версии
if utility.has_collection("example_collection"):
    utility.drop_collection("example_collection")

version = utility.get_server_version()
print(f"Connected to Milvus. Server version: {version}")
#
# # Создание схемы коллекции
# fields = [
#     FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
#     FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=128)
# ]
# schema = CollectionSchema(fields, "example collection schema")
#
# # Создание коллекции
# collection = Collection(name="example_collection", schema=schema)
#
# # Вставка данных
# import random
#
# vectors = [[random.random() for _ in range(128)] for _ in range(10)]
# collection.insert([vectors])
#
# # Создание индекса
# index_params = {
#     "metric_type": "L2",
#     "index_type": "IVF_FLAT",
#     "params": {"nlist": 128}
# }
# collection.create_index(field_name="vector", index_params=index_params)
#
# # Загрузка коллекции в память
# collection.load()
#
# # Выполнение поиска
# search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
# results = collection.search(vectors[:1], "vector", search_params, limit=3)
# print(f"Search results: {results}")
#
# # Очистка
# # utility.drop_collection("example_collection")
