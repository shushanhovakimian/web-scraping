DB_NAME = "postgres"
DB_PASSWORD = "admin"
DB_USER = "user"
DB_HOST = "local_pgdb"
DB_PORT = 5432

def get_and_transform_data(index):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}

    url_is = 'https://finance.yahoo.com/quote/' + index + '/financials?p=' + index
    page = requests.get(url_is, headers=headers)
    soup = BeautifulSoup(page.text, "html.parser")
    ls = []  # Creating an empty list
    for s in soup.find_all('button'):
        s.extract()
    for l in soup.find_all(['div']):
        # Finding all data structure that is ‘div’
        ls.append(l.string)  # Adding each element one by one to the list

    new_ls = list(filter(None, ls))
    new_ls = new_ls[14:]
    is_data = list(zip(*[iter(new_ls)] * 6))

    Income_st = pd.DataFrame(is_data[0:])
    Income_st.columns = Income_st.iloc[0]  # Name columns to first row of dataframe
    Income_st = Income_st.iloc[1:, ]  # start to read 1st row
    Income_st = Income_st.T  # transpose dataframe
    Income_st.columns = Income_st.iloc[0]  # Name columns to first row of dataframe
    Income_st.drop(Income_st.index[0], inplace=True)  # Drop first index row
    Income_st.index.name = ''  # Remove the index name
    Income_st = Income_st[Income_st.columns[:-5]]  # remove last 5 irrelevant columns

    return Income_st

def db_connect(host=None, port=None, database=None, user=None, password=None):
    """create database connection"""
    try:
        connection = psycopg2.connect(host=host, port=port, database=database,
                                      user=user, password=password)
        print("connected successfully")
        return connection
    except Exception as error:
        print(type(error))
        print(error)

def insert_values(dataframe, table):
    """import data to database"""

    conn = db_connect(host=DB_HOST, port=DB_PORT, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    tuples = [tuple(x) for x in dataframe.to_numpy()]

    cols = ','.join(list(dataframe.columns))
    # SQL query to execute
    query = "INSERT INTO %s(%s) VALUES %%s" % ("income_statement", cols)
    cursor = conn.cursor()
    try:
        extras.execute_values(cursor, query, tuples)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cursor.close()
        return 1
    print("the dataframe is inserted")
    cursor.close()

if __name__ == "__main__":

    output = get_and_transform_data("AAPL")
    if output is not None:
        insert_values(output, table="income_statement")