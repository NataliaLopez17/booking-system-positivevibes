from config.dbconfig import pg_config
import psycopg2

class RoomsUnavailDao():
    def __init__(self) -> None:
        connection_url = "dbname=%s user=%s password=%s port=%s host=%s" %(pg_config['dbname'], pg_config['user'], pg_config['password'],
                                                                            pg_config['port'], pg_config['host'])
        self.conn = psycopg2.connect(connection_url)

    def getAllRoomsUnavail(self):
        cursor = self.conn.cursor()
        query = "select room_unavail_id, room_id, room_unavail_date, room_start_time, room_end_time from room_unavailability"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getRoomUnavailById(self, room_unavail_id):
        cursor = self.conn.cursor()
        query = "select room_unavail_id, room_id, room_unavail_date, room_start_time, room_end_time from room_unavailability where room_unavail_id=%s"
        cursor.execute(query, (room_unavail_id,))
        result = cursor.fetchone()
        return result

    def updateRoomUnavail(self, room_unavail_id, room_id, room_unavail_date, room_start_time, room_end_time):
        cursor = self.conn.cursor()
        query = "update room_unavailability set room_id=%s, room_unavail_date=%s, room_start_time=%s, room_end_time=%s where room_unavail_id=%s;"
        cursor.execute(query, (room_id, room_unavail_date, room_start_time, room_end_time, room_unavail_id))
        self.conn.commit()
        return True

    def insertRoomUnavail(self, room_id, room_unavail_date, room_start_time, room_end_time):
        cursor = self.conn.cursor()
        query = "insert into room_unavailability (room_id, room_unavail_date, room_start_time, room_end_time) values (%s, %s, %s, %s) returning room_unavail_id;"
        cursor.execute(query, (room_id, room_unavail_date, room_start_time, room_end_time,))
        room_unavail_id = cursor.fetchone()[0]
        self.conn.commit()
        return room_unavail_id

    def deleteRoomUnavail(self, room_unavail_id):
        cursor = self.conn.cursor()
        query = "delete from room_unavailability where room_unavail_id=%s"  
        cursor.execute(query, (room_unavail_id,))
        affected_rows = cursor.rowcount
        self.conn.commit()
        return affected_rows != 0