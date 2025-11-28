import os
from pymongo import MongoClient
import streamlit as st
from dotenv import load_dotenv

load_dotenv()  # carrega .env se existir

def get_db():
    uri = os.getenv("MONGO_URI")
    db_name = os.getenv("MONGO_DB")

    client = MongoClient(uri)
    return client[db_name]


def get_collection(nome_colecao):
    db = get_db()
    return db[nome_colecao]
