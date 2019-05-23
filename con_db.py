#!/usr/bin/env python

import psycopg2

def mkcodb():
    conn = psycopg2.connect(database="fusionpbx", user="fusionpbx", password="9MsCmsOetx7mqyTOg8ModB8ak", host="localhost", port="5432")
    return conn