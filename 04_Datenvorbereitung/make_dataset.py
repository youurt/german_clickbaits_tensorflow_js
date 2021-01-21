import pandas as pd
import sqlite3
import re
import string


def remove_punc(text):
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub('\w*\d\w*', '', text)
    return text


def connect_to_db(tablename, db_path):
    return pd.read_sql_query(
        f"SELECT * FROM {tablename}", sqlite3.connect(db_path))


def strip_new_lines(df, column_name_df):
    return df[column_name_df].apply(
        lambda x: " ".join(x.replace("\n", "").split()))


def label_data(df, col_name, **kwargs):
    return df[col_name].apply(
        lambda x: '1' if '?' in x or kwargs["word_1"] in x or kwargs["word_2"] in x else '0')


def remove_suffix(df, column_name_df, what):
    return df[column_name_df].apply(
        lambda x: x.replace(what, ""))


def contains_string(word, col):
    for s in col:
        if s in word:
            return "1"


def label_data_with_arg(df, col_name, arg_):
    return df[col_name].apply(
        lambda x: contains_string(arg_, re.findall(r"[\w']+|[.,!?;]", x.lower())))


def set_human(row):
    if row["origin"] == "wiki":
        return "none_bait"
    if row["is_question"] == "1":
        return "bait"
    elif row["has_keyword"] == "1":
        return "bait"
    elif row["has_number"] == "1":
        return "bait"
    else:
        return "none_bait"


def get_avg_length(string):
    words = remove_punc(string).split()
    try:
        count = int(sum(len(word) for word in words) / len(words))
    except ZeroDivisionError:
        count = 1
    return count


def count_words(string):
    words = remove_punc(string).split()
    return len([word for word in words])


def get_sum(row):
    is_question = int(row["is_question"])
    is_slang = int(row["has_keyword"])
    has_number = int(row["has_number"])
    avg_w_length = int(row["avg_word_length"])

    if int(round(is_question*-2 + is_slang*-3 + has_number*-2 + avg_w_length*3)) <= 0:
        return 1
    else:
        return int(round(is_question*-2 + is_slang*-3 + has_number*-2 + avg_w_length*3))


# def contains_pos(sentence):
#     list_ = ["PDAT", "ADJD", "ADJA", "PIS",
#              "PWAV", "PTKA", "VAFIN", "PROAV", "ADV"]
#     doc = nlp(sentence)
#     for token in doc:
#         if str(token.tag_) in list_:
#             return "1"


# def label_data_with_pos(df, col_name):
#     return df[col_name].apply(
#         lambda x: contains_pos(x.lower()))

    # connect to db
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


# origin of data
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


# special operations
# 1
heftig_df = heftig_df.rename(columns={"headline": "title"})

# 2
wiki_df = wiki_df.rename(columns={"extract": "text"})
wiki_df = wiki_df.sample(frac=1).reset_index(drop=True)
wiki_df = wiki_df[:10000]
wiki_df["label"] = "1"
wiki_df["text"] = strip_new_lines(wiki_df, "text")


# 4
bravo_df["title"] = remove_suffix(bravo_df, "title", "| BRAVO")
webde_df["title"] = remove_suffix(webde_df, "title", "| WEB.DE")

# generate end df
all_df = pd.concat([buzz_df, heftig_df, frau_df,
                    quiz_df, tasty_df, movie_df, bravo_df, webde_df, promi_df, wiki_df])

just_clickbait_all_df = pd.concat([buzz_df, heftig_df, frau_df,
                                   quiz_df, tasty_df, movie_df, bravo_df, webde_df, promi_df])


del wiki_df["page_id"]
del wiki_df["text"]
del wiki_df["category"]

del just_clickbait_all_df["id"]
del just_clickbait_all_df["page_id"]
del just_clickbait_all_df["scraped_at"]
del just_clickbait_all_df["url"]
del just_clickbait_all_df["text"]


# has question
wiki_df["is_question"] = label_data_with_arg(
    wiki_df, "title", "?")

just_clickbait_all_df["is_question"] = label_data_with_arg(
    just_clickbait_all_df, "title", "?")

# has slang
wiki_df["has_keyword"] = label_data_with_arg(
    wiki_df, "title", ["diese", "besten", "krassen", "neue", "darum", "dinge", "mehr", "alle", "so", "quiz"])


just_clickbait_all_df["has_keyword"] = label_data_with_arg(
    just_clickbait_all_df, "title", ["diese", "besten", "krassen", "neue", "darum", "dinge", "mehr", "alle", "so", "quiz"])


# has number
wiki_df["has_number"] = label_data_with_arg(
    wiki_df, "title", [str(i) for i in range(1, 11)])

just_clickbait_all_df["has_number"] = label_data_with_arg(
    just_clickbait_all_df, "title", [str(i) for i in range(1, 11)])


# set human
wiki_df = wiki_df.assign(human=wiki_df.apply(set_human, axis=1))


just_clickbait_all_df = just_clickbait_all_df.assign(
    human=just_clickbait_all_df.apply(set_human, axis=1))

just_clickbait_all_df = just_clickbait_all_df[just_clickbait_all_df.human == "bait"]

just_clickbait_all_df = just_clickbait_all_df[~just_clickbait_all_df["title"].str.contains(
    "köln|berlin|staffel|gzsz|sturm", case=False, regex=True)]


# all_df.to_csv("clickbaits.csv", index=False)

just_clickbait_all_df = just_clickbait_all_df.reset_index()
del just_clickbait_all_df["index"]
just_clickbait_all_df = just_clickbait_all_df.fillna(0)
just_clickbait_all_df = just_clickbait_all_df.sample(
    frac=1).reset_index(drop=True)
# just_clickbait_all_df.to_csv("just_clickbaits.csv", index=False)

just_clickbait_all_df["avg_word_length"] = just_clickbait_all_df["title"].apply(
    get_avg_length)
just_clickbait_all_df["count_words"] = just_clickbait_all_df["title"].apply(
    count_words)

just_clickbait_all_df = just_clickbait_all_df.assign(
    class_name=just_clickbait_all_df.apply(get_sum, axis=1))


wiki_df["avg_word_length"] = wiki_df["title"].apply(
    get_avg_length)
wiki_df["count_words"] = wiki_df["title"].apply(
    count_words)
wiki_df["class_name"] = 0


# bring all together

just_clickbait_all_df = just_clickbait_all_df[:10000]
result = pd.concat([just_clickbait_all_df, wiki_df])
# result = just_clickbait_all_df

# change class_name values to strings


result = result.reset_index()
del result["index"]
del result["human"]
del result["class_name"]
result = result.fillna(0)
result = result.sample(frac=1).reset_index(drop=True)

result.to_csv("result.csv", index=False)
