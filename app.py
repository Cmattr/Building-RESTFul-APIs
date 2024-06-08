from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from marshmallow import fields, ValidationError
import mysql.connector
from mysql.connector import Error


def get_db_connection():
    db_name = "gym_db"
    user = "root"
    password = "Richardson!629"
    host = "localhost"
    try:
        conn = mysql.connector.connect(
            database=db_name,
            user=user,
            password=password,
            host=host,
            auth_plugin='mysql_native_password'
        )
        
        print("connected to gym_db")
        return conn

    except Error as e:
        print(f"Error: {e}")

app = Flask(__name__)
ma = Marshmallow(app)

class MemberSchema(ma.Schema):
    name = fields.String(required=True)
    age = fields.Integer(required=True)
    id = fields.Integer(required=True)


    class Meta:
        fields = ("name","age", "id")

member_schema = MemberSchema()
members_schema = MemberSchema(many=True)


class WorkoutSessionSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    member_id = fields.Integer(required=True)
    session_date = fields.String(required=True)
    session_time = fields.String(required=True)
    activity = fields.String(required=True)

    class Meta:
        fields = ("id", "member_id", "session_date", "session_time", "activity")

workout_session_schema = WorkoutSessionSchema()
workoutsessions_schema = WorkoutSessionSchema(many=True)

class TrainerSchema(ma.Schema):
    trainer_id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    specialty = fields.String(required=True)

    class Meta:
        fields = ("trainer_id", "name", "specialty")

trainer_schema = TrainerSchema()
trainers_schema = TrainerSchema(many=True)

@app.route('/')
def home():
    return 'Welcome to the Gym!'

@app.route("/members", methods=["GET"])
def get_members():
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify ({"error": "Database connection failed"}), 500
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM members"
        cursor.execute(query)
        members = cursor.fetchall()
        return members_schema.jsonify(members) 
    except Error as e:
        print(f"Error: {e}") 
        return jsonify({"error": "Internal Server Error"}), 500

@app.route("/members", methods=["POST"])
def add_member():
    try:
        member_data = member_schema.load(request.json)
    except ValidationError as e:
        print(F"Error: {e}")
        return jsonify(e.messages), 400
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify ({"error": "Database connection failed"}), 500
        cursor = conn.cursor()
        new_member = (member_data ['name'], member_data['age'], member_data['id'])
        query = "INSERT INTO members(name, age, id) VALUES (%s, %s, %s)"
        cursor.execute(query, new_member)
        conn.commit()
        return jsonify({"message": "new member added successfully"}), 201
    except Error as e:
        print(f"error: {e}")
        return jsonify ({"error": "Internal server error"}), 500 
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route("/members/<int:id>", methods=["PUT"])
def update_members(id):
    try:
        members_data = member_schema.load(request.json)
    except ValidationError as e:
        print(F"Error: {e}")
        return jsonify(e.messages), 400
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify ({"error": "Database connection failed"}), 500
        cursor = conn.cursor()
        updated_members = (members_data['name'], members_data['age'], id)
        query = 'UPDATE members SET name = %s, age = %s WHERE id = %s' 
        cursor.execute(query, updated_members)
        conn.commit()
        return jsonify({"message": "updated members information successfully"}), 201
    except Error as e:
        print(f"error: {e}")
        return jsonify ({"error": "Internal server error"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route("/members/<int:id>", methods=["DELETE"])
def delete_member(id):
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify ({"error": "Database connection failed"}), 500
        cursor = conn.cursor()
        member_to_remove = (id,)
        cursor.execute("SELECT * FROM members where ID = %s", member_to_remove)
        member = cursor.fetchone()
        if not member:
            return jsonify(["ERROR: member not found"]), 404
        query = "DELETE FROM members WHERE id = %s"
        cursor.execute(query, member_to_remove)
        conn.commit()        
        return jsonify({"message": "member removed successfully"}), 200
    except Error as e:
        print(f"error: {e}")
        return jsonify ({"error": "Internal server error"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


@app.route("/sessions", methods=["GET"])
def sessions():
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify ({"error": "Database connection failed"}), 500
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM Workoutsessions"
        cursor.execute(query)
        sessions = cursor.fetchall()
        return workoutsessions_schema.jsonify(sessions) 
    except Error as e:
        print(f"Error: {e}") 
        return jsonify({"error": "Internal Server Error"}), 500


@app.route("/Session", methods=["POST"])
def add_session():
    try:
        workoutsession_data = workout_session_schema.load(request.json)
    except ValidationError as e:
        print(F"Error: {e}")
        return jsonify(e.messages), 400
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify ({"error": "Database connection failed"}), 500
        cursor = conn.cursor()
        new_session = (workoutsession_data ['id'], workoutsession_data['member_id'], workoutsession_data['session_date'], workoutsession_data["session_time"], workoutsession_data["activity"])
        query = "INSERT INTO workoutsessions(id, member_id, session_date, session_time, activity) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, new_session)
        conn.commit()
        return jsonify({"message": "new member added successfully"}), 201
    except Error as e:
        print(f"error: {e}")
        return jsonify ({"error": "Internal server error"}), 500 
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


@app.route("/session/<int:id>", methods=["PUT"])
def update_sessions(id):
    try:
        workoutsession_data = workout_session_schema.load(request.json)
    except ValidationError as e:
        print(F"Error: {e}")
        return jsonify(e.messages), 400
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify ({"error": "Database connection failed"}), 500
        cursor = conn.cursor()
        updated_sessions = (workoutsession_data['member_id'], workoutsession_data['session_date'], workoutsession_data['session_time'], workoutsession_data['activity'], id)
        query = 'UPDATE workoutsessions SET member_id = %s, session_date = %s, session_time = %s, activity = %s WHERE id = %s' 
        cursor.execute(query, updated_sessions)
        conn.commit()
        return jsonify({"message": "updated members information successfully"}), 201
    except Error as e:
        print(f"error: {e}")
        return jsonify ({"error": "Internal server error"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route("/sessions/member/<int:member_id>", methods=["GET"])
def get_workoutsessions_for_member(member_id):
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM workoutsessions WHERE member_id = %s"
        cursor.execute(query, (member_id,))
        workoutsessions = cursor.fetchall()


        for session in workoutsessions:
            session['session_date'] = session['session_date'].format()
            
        return workoutsessions_schema.jsonify(workoutsessions)
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/trainers/distinct', methods=['GET'])
def list_distinct_trainers():
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT DISTINCT t.trainer_id, t.name, t.specialty
            FROM trainers t
            JOIN workoutsessions ws ON t.trainer_id = ws.trainer_id
        """
        cursor.execute(query)
        trainers = cursor.fetchall()
        return trainers_schema.jsonify(trainers)
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/trainers/count_members', methods=['GET'])
def count_members_per_trainer():
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT t.trainer_id, t.name, COUNT(m.id) as member_count
            FROM trainers t
            JOIN members m ON t.trainer_id = m.trainer_id
            GROUP BY t.trainer_id, t.name
        """
        cursor.execute(query)
        result = cursor.fetchall()
        return jsonify(result)
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/members/age_range', methods=['GET'])
def get_members_in_age_range():
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT name, age, id
            FROM members
            WHERE age BETWEEN 25 AND 30
        """
        cursor.execute(query)
        members = cursor.fetchall()
        return members_schema.jsonify(members)
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == '__main__':
    app.run(debug=True)

