from flask import Flask, request, jsonify, render_template
import csv
from datetime import datetime

import mysql.connector

cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password="tiger",
    database="Datasets"
)
cursor = cnx.cursor()


'''
statement = "TRUNCATE TABLE Data"

# execute the statement
cursor.execute(statement)

# commit the changes to the database
cnx.commit()


'''

# query = "SELECT * FROM Data"
# cursor.execute(query)
# results = cursor.fetchall()
# print(results)
#cursor.close()
#cnx.close()


# create_table_query = """
#         CREATE TABLE Data (
#             Temp FLOAT NOT NULL,
#             Humid FLOAT NOT NULL,
#             Timestamp DATETIME NOT NULL
#         )
#     """
# create_table_query="drop table Data"
# cursor.execute(create_table_query)



app = Flask(__name__)

# Create an empty list to store the data entries
data_list = []

@app.route("/")
@app.route("/home")
def home_page():
    results = []
    statement = "SELECT * FROM Data ORDER BY Timestamp DESC LIMIT 1"
    cursor.execute(statement)
    result = cursor.fetchall()
    for row in result:
        data_entry = {'temp': row[0], 'humidity': row[1], 'timestamp': row[2]}
        print(data_entry)
        results.append(data_entry)
    return render_template('home.html', results=results)







@app.route('/data', methods=['POST'])
def receive_data():
    temp = request.form.get('temp')
    humidity = request.form.get('humidity')
    timestamp = request.form.get('timestamp')
    datetime_obj = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')

    data = []
    data.append(temp)
    data.append(humidity)
    data.append(datetime_obj)


    #csv_file = open(filename, 'a')
    #writer = csv.writer(csv_file)
    #writer.writerow(data)
    #data = []
    values = (temp, humidity, timestamp)
    statement = "INSERT INTO Data (temp, humid, timestamp) VALUES (%s, %s, %s)"    
    cursor.execute(statement, values)
    cnx.commit()

    # Create a dictionary to store the data
    data_entry = {'temp': temp, 'humidity': humidity, 'timestamp': timestamp}
    
    # Add the data entry to the list
    data_list.append(data_entry)
    
    # Return a success message
    return 'Data received'



@app.route('/data', methods=['GET'])
def get_data():
    # Return the contents of the list as JSON
    results = []

    query = "SELECT * FROM Data"
    cursor.execute(query)
    result = cursor.fetchall()
    #print(results)
    count = 1
    for row in result:
        data_entry = {'temp': row[0], 'humidity': row[1], 'timestamp': row[2]}
        print(data_entry)
        results.append(data_entry)
        # count = count + 1
    return render_template('alldata.html', results=results)









@app.route("/more",  methods=['GET', 'POST'])
def more_details():
    if request.method == 'POST':
        start_datetime = request.form.get('start') #start_time = datetime.strptime(request.form.get('start'), "%Y-%m-%dT%H:%M")
        end_datetime = request.form.get('end') #end_time = datetime.strptime(request.form.get('end'), "%Y-%m-%dT%H:%M")


        # Execute the SELECT statement to retrieve the data within the given date time range
        statement = "SELECT * FROM Data WHERE Timestamp BETWEEN %s AND %s"
        cursor.execute(statement, (start_datetime, end_datetime))
        print(statement,start_datetime, end_datetime)
        result = cursor.fetchall()

        # Create a list of data entries
        data_entries = []
        for row in result:
            data_entry = {'temp': row[0], 'humidity': row[1], 'timestamp': row[2]}
            data_entries.append(data_entry)

        # Return the list of data entries as a JSON response
        return render_template('more_details.html', results=data_entries)
    return render_template('more_details.html')







@app.route('/humidity', methods=['GET'])
def get_humidity():
    humidity_list = []
    statement = "SELECT Humid FROM Data"
    cursor.execute(statement)
    result = cursor.fetchall()
    # print(result)
    for x in result:
        humidity_list.append(x)
    print(humidity_list)
    # Return the list as a JSON response
    return jsonify(humidity_list)


@app.route('/temperature', methods=['GET'])
def get_temperature():
    humidity_list = []
    statement = "SELECT Temp FROM Data"
    cursor.execute(statement)
    result = cursor.fetchall()
    # print(result)
    for x in result:
        humidity_list.append(x)
    print(humidity_list)
    # Return the list as a JSON response
    return jsonify(humidity_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9002, debug=True)

