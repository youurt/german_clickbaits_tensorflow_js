import pandas as pd
import sqlite3


def connect_to_db(tablename, db_path):
    return pd.read_sql_query(
        f"SELECT * FROM {tablename}", sqlite3.connect(db_path))


buzz_df = connect_to_db("buzz", "./data/buzz.db")
heftig_df = connect_to_db("heftig", "./data/heftig.db")
frau_df = connect_to_db("frau", "./data/frau.db")
quiz_df = connect_to_db("quiz", "./data/quiz.db")
tasty_df = connect_to_db("tasty", "./data/tasty.db")
movie_df = connect_to_db("movie", "./data/tvmovie.db")
wiki_df = connect_to_db("wiki", "./data/wiki_full_text.db")
bravo_df = connect_to_db("bravo", "./data/bravo.db")
webde_df = connect_to_db("webde", "./data/webde.db")
promi_df = connect_to_db("promipool", "./data/promi.db")

buzz_df["origin"] = "buzzfeed"
heftig_df["origin"] = "heftig"
frau_df["origin"] = "frau"
quiz_df["origin"] = "quiz"
tasty_df["origin"] = "tasty"
movie_df["origin"] = "movie"
wiki_df["origin"] = "wiki"
bravo_df["origin"] = "bravo"
webde_df["origin"] = "webde"
promi_df["origin"] = "promi"


raw_data = pd.concat([buzz_df, heftig_df, frau_df,
                      quiz_df, tasty_df, movie_df, wiki_df, bravo_df, webde_df, promi_df])

raw_data.to_csv("raw.csv", index=False)
