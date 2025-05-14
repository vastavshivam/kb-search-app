import pandas as pd
import numpy as np
# import spacy
# import gensim
# from gensim.models import Word2Vec
from fastapi import FastAPI, Depends
from pydantic import BaseModel
import mysql.connector
import re


from numpy.linalg import norm


import logging

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "chatbot_db",
    "charset": "utf8mb4",
    "collation": "utf8mb4_unicode_ci"
}

def get_db():    
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    return conn, cursor