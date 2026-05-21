import csv
# open() opens the file
# newline="" prevents extra blank lines on Windows
# encoding="utf-8" handles special characters

def read_csv(filename):
    data = []
    with open(filename, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(dict(row))
    return data

def test_read_csv():
    records = read_csv("./test_data/login_data.csv")
    print(records)
    for row in records:
        print(row)
    assert len(records) > 0
