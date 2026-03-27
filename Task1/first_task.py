#Import all the necessary libraries
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId
#Create a connection using MongoClient
client = MongoClient(
    "mongodb+srv://straitrzr:password321@cluster0.6udzmea.mongodb.net/",
    server_api = ServerApi('1')
)
#Choose a database
db = client.Test


# Fill out the database
first_record = db.dogs.insert_one(
    {
            "name":"Bruce",
        "age":4,
        "breed":"Rottweieler",
        "features":["приносить палицю","любить коли чешуть за вухом", "ласкавий"],
    }
)
print(first_record.inserted_id)

#insert many documents at once
multiple_records = db.dogs.insert_many(
    [
        {
        "name":"Rocky",
        "age":6,
        "breed":"Belgian Malinois",
        "features":["гавкає","кусається", "аггресивний"],
    },
    {
        "name":"Roger",
        "age":3,
        "breed":"German Shepherd",
        "features":["добрий","бадьорий","любить дітей"]
    }
    ]
)
print(multiple_records.inserted_ids)
#Read funcs
def read_all():
    all_records = db.dogs.find({})

    return f"List of all the records from the database: {list(all_records)}"

def read_record(name:str) -> dict:
    if not name.isalpha():
        raise ValueError("Invalid name entered, please re-enter")
    return f"{name}'s document: {db.dogs.find_one({"name": name})}"

#Update funcs
def update_age(name:str,new_age:int) -> dict:
    updated_age = db.dogs.update_one({"name":name}, {"$set":{"age":new_age}})

    if not name.isalpha():
        raise ValueError("Invalid name entered, please re-enter")
    if not str(new_age).isdigit():
        raise ValueError("Invalid age entered, please re-enter")

    return f"Set a new age for {name}, {new_age}"


def update_name(name:str,new_name:str) -> dict:
    if not name.isalpha():
        raise ValueError("What kind of name is that?")
    if not new_name.isalpha():
        raise ValueError("What kind of name is that?")
    updated_name = db.dogs.update_one({"name":name}, {"$set":{"name":new_name}})

    return f"Updated {name}'s name to {new_name}"
#Delete funcs
def delete_document(name:str):
    if not name.isalpha():
        raise ValueError("Invalid name entered, please re-enter")
    deleted_record = db.dogs.delete_one({"name":name})
    
    return f"Deleted {name}'s document form database"

def clear_database() -> None:
    deleted = db.dogs.delete_many({})

    return f"Database cleared, deleted {deleted.deleted_count} documents"

#Test the functions
print(read_all())
print(read_record("Bruce"))
print(update_age("Bruce", 5))
print(update_name("Rocky", "Johny"))
print(delete_document("Roger"))
print(clear_database())