from config.dbconfig import pg_config
import psycopg2

class RoomsDAO():
    def __init__(self) -> None:
        connection_url = "dbname=%s user=%s password=%s port=%s host=%s" %(pg_config['dbname'], pg_config['user'], pg_config['password'],
                                                                            pg_config['port'], pg_config['host'])
        self.conn = psycopg2.connect(connection_url)

    def getAllRooms(self):
        cursor = self.conn.cursor()
        query = "select room_id, room_capacity, authorization_level, building_id from rooms;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getRoomById(self, room_id):
        cursor = self.conn.cursor()
        query = "select room_id, room_capacity, authorization_level, building_id from rooms where room_id=%s;"
        cursor.execute(query, (room_id,))
        result = cursor.fetchone()
        return result

    def updateRoom(self, room_id, room_capacity, authorization_level, building_id):
        cursor = self.conn.cursor()
        query = "update rooms set room_capacity=%s, authorization_level=%s, building_id=%s where room_id=%s;"
        cursor.execute(query, (room_capacity, authorization_level, building_id, room_id))
        self.conn.commit()
        return True

    def insertRoom(self, room_capacity, authorization_level, building_id):
        cursor = self.conn.cursor()
        query = "insert into rooms (room_capacity, authorization_level, building_id) values (%s, %s, %s) returning room_id;"
        cursor.execute(query, (room_capacity, authorization_level, building_id,))
        room_id = cursor.fetchone()[0]
        self.conn.commit()
        return room_id

    def deleteRoom(self, room_id):
        cursor = self.conn.cursor()
        query = "delete from rooms where room_id=%s"
        cursor.execute(query, (room_id,))
        affected_rows = cursor.rowcount
        self.conn.commit()
        return affected_rows != 0