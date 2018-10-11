import sqlite3


def main():
    db = sqlite3.connect('test.dp')
    db.execute('DROP TABLE IF EXISTS test')
    db.execute('CREATE TABLE test(t1 text, i1 int)')

    db.execute('INSERT INTO test (t1, i1) VALUES (?, ?)', ('one', 1))
    db.execute('INSERT INTO test (t1, i1) VALUES (?, ?)', ('two', 2))
    db.execute('INSERT INTO test (t1, i1) VALUES (?, ?)', ('three', 3))
    db.execute('INSERT INTO test (t1, i1) VALUES (?, ?)', ('four', 4))
    db.execute('INSERT INTO test (t1, i1) VALUES (?, ?)', ('five', 5))

    db.commit()
    cursor = db.execute('SELECT * FROM test ORDER BY i1')
    for row in cursor: print(row)


if __name__ == "__main__": main()