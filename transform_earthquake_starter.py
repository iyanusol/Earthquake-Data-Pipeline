import psycopg2
import os


def delete_old_records(conn, start_date, end_date):
    delete_query = """
    DELETE FROM raw.stage_earthquake
    WHERE dt BETWEEN %s AND %s;
    """
    cur = conn.cursor()
    cur.execute(delete_query, (start_date, end_date))
    conn.commit()
    cur.close()


def transform_earthquake(conn, start_date, end_date):
    cur = conn.cursor()
    sql = """
    INSERT INTO raw.stage_earthquake (
        ts, dt, place, magnitude, longitude, latitude, depth
    )
    SELECT
        to_timestamp(time / 1000) AS ts,
        cast(to_timestamp(time / 1000) AS date) AS dt,
        TRIM(SUBSTRING(place FROM POSITION('of ' IN place) + 3)) AS place,
        magnitude,
        longitude,
        latitude,
        depth
    FROM public.earthquake
    WHERE cast(to_timestamp(time / 1000) AS date)
          BETWEEN %s AND %s;
    """
    cur.execute(sql, (start_date, end_date))
    conn.commit()
    cur.close()




def main():
    db_params = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': 'iyanu1234',
    'host': 'localhost',
    'port': '5432'
}


    conn = psycopg2.connect(**db_params)

    start_date = "2025-12-31"
    end_date = "2026-01-15"

    try:
        delete_old_records(conn, start_date, end_date)
        transform_earthquake(conn, start_date, end_date)
        print("Data loaded successfully")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()




if __name__ == "__main__":
    main()
