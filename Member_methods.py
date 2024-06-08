
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


