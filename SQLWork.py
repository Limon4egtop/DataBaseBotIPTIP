import pymysql

def getAllDataAboutUser(userId):
    """
    {'id': 132434, 'username': 'gsfdhgfhcgjhv',
    'first_name': 'qwe', 'last_name': 'eret',
    'phone_number': '+789', 'group_code': 'dsdv',
    'group_number': 12, 'group_year': 22,
    'status': 'Active'}
    :return: userDataRow
    """
    connection = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='Limon',
        database='IPTIPUserDataTgBot',
        cursorclass=pymysql.cursors.DictCursor
    )
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM UsersData WHERE id={userId}")
    # for row in cursor.fetchall():
    #     print(row)
    # print("#" * 20)
    # print("Connected - Yes")
    return cursor.fetchall()[0]
    connection.close()

def putIdAndUsername(userId, username):
    connection = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='Limon',
        database='IPTIPUserDataTgBot',
        cursorclass=pymysql.cursors.DictCursor
    )
    cursor = connection.cursor()
    cursor.execute("SELECT EXISTS(SELECT * FROM UsersData WHERE id = '%s')" % (userId))
    SQLSay = cursor.fetchone()
    if list(SQLSay.values())[0] == 0:
        cursor.execute("INSERT INTO UsersData(id, username) VALUES('%s', '%s')" % (userId, username))
    else:
        cursor.execute("UPDATE UsersData SET username = '%s' WHERE id = '%s'" % (username, userId))
    connection.commit()
    connection.close()

def updateFirstAndLastName(userId, firstName, lastName):
    connection = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='Limon',
        database='IPTIPUserDataTgBot',
        cursorclass=pymysql.cursors.DictCursor
    )
    cursor = connection.cursor()
    cursor.execute("UPDATE UsersData SET first_name = '%s', last_name = '%s' WHERE id = '%s'" %
                   (firstName, lastName, userId))
    connection.commit()
    connection.close()

def updatePhoneNumber(userId, phoneNumber):
    connection = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='Limon',
        database='IPTIPUserDataTgBot',
        cursorclass=pymysql.cursors.DictCursor
    )
    cursor = connection.cursor()
    cursor.execute("UPDATE UsersData SET phone_number = '%s'WHERE id = '%s'" %
                   (phoneNumber, userId))
    connection.commit()
    connection.close()

def updateGroupeNumber(userId, groupCode, groupNumber, groupYear):
    connection = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='Limon',
        database='IPTIPUserDataTgBot',
        cursorclass=pymysql.cursors.DictCursor
    )
    cursor = connection.cursor()
    cursor.execute("UPDATE UsersData SET group_code = '%s', group_number = '%s', group_year = '%s' WHERE id = '%s'" %
                   (groupCode, groupNumber, groupYear, userId))
    connection.commit()
    connection.close()