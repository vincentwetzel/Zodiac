from collections.abc import Generator
from datetime import datetime

import pandas as pd

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


def main():
    cred = credentials.Certificate('./ServiceAccountKey.json')
    default_app = firebase_admin.initialize_app(cred)
    db: firebase_admin.firestore.client() = firestore.client(default_app)

    '''
    # Get a collection
    slcogop_officer_names_doc_ref: firestore.firestore.CollectionReference = db.collection(u'SLCOGOP_Officer_Names')
    doc_stream_generator = slcogop_officer_names_doc_ref.stream()  # Returns a generator
    print_collection(doc_stream_generator, 0)
    '''

    # add_sample_data_types(db)

    df = pd.read_excel("E:/Google Drive (vincentwetzel3@gmail.com)/Zodiac/zodiac_people.xlsx")
    d = df.set_index("Name").to_dict(orient="index")  # 'dict', 'list', 'series', 'split', 'records', 'index'
    # pp_nested_dict(d)
    for name in d:
        if '\"' in name or "(" in name:
            print(name)
    for name, data in d.items():
        add_zodiac_person(name, data, db)

def add_zodiac_person(name: str, data: dict, db: firebase_admin.firestore.client):
    upload_data = {
        "Name": name,
        "Month": data["Month"],
        "Day": data["Day"],
        "Year": data["Year"],
        "Sign": data["Sign"],
        "Element": data["Element"],
        "Quality": data["Quality"],
        "Political": data["Political"],
        "Hottie": data["Hottie"],
        "President": data["President"],
        "Notes": None if pd.isna(data["Notes"]) else data["Notes"]
    }
    db.collection('Zodiac').document(name.replace(" ", "_")).set(upload_data)

def add_sample_data_types(db: firebase_admin.firestore.client):
    data = {
        u'stringExample': u'Hello, World!',
        u'booleanExample': True,
        u'numberExample': 3.14159265,
        u'dateExample': datetime.now(),
        u'arrayExample': [5, True, u'hello'],
        u'nullExample': None,
        u'mapExample': {
            u'a': 5,
            u'b': True
        }
    }

    db.collection('SLCOGOP_Officer_Names').document(u'Scott_Miller').set(data)
    # [END add_sample_data_types]


def print_collection(doc_stream: Generator[firebase_admin.firestore.firestore.DocumentSnapshot], level: int) -> None:
    """
    Prints a collection.
    :type doc_stream: Generator
    :param level: The level of recursion of this function
    :return: None
    """
    for doc in doc_stream:
        print("DOCUMENT_ID: " + doc.id)
        pp_nested_dict(doc.to_dict())


def pp_nested_dict(d: dict, iteration_level: int = 1) -> None:
    for key, val in d.items():
        if type(val) is not dict:
            print("\t" * iteration_level + str(key) + ": " + str(val))
        else:
            print("\t" * iteration_level + ">" + str(key))
            pp_nested_dict(val, iteration_level + 1)


if __name__ == "__main__":
    main()
