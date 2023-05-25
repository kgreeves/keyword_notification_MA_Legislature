import psycopg2

hostname = 'localhost'
username = 'postgres'
port = 5433
password = 'Duckbox2!'
database = 'keyword_notification_MA_legislature'

def queryQuotes( conn ) :
    cur = conn.cursor()

    cur.execute(""" insert into bill_table 
    
    (bill_no,
    leg_body,
    bill_no_int,
    filed_by,
    filed_by_last,
    filed_by_first,
    filed_by_middle,
    title,
    description,
    url,
    session_no)
    
    values( %s,%s,%s,%s,%s,%s,
            %s,%s,%s,%s,%s )
    
    """,

    ('H.123',
    'H',
    123,
    'Candy Mann',
    'Mann',
    'Candy',
    None,
    'Title',
    'And the description',
    'http://www.google.com',
    198)

    )

    conn.commit()

    cur.execute("""select * from bill_table""")
    rows = cur.fetchall()

    for row in rows:
        print(row)

conn = psycopg2.connect( host=hostname, user=username, password=password, dbname=database, port=port )
queryQuotes( conn )
conn.close()