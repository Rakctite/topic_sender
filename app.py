import psycopg2
import paho.mqtt.client as mqtt
import json
import os
import threading
import time
import sys

DEVICE_MAP = {}
map_lock = threading.Lock()

# DB 연결 정보 공통 사용
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "127.0.0.1"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "database": os.getenv("DB_NAME", "edge_hmi"),
    "user": os.getenv("DB_USER", "admin"),
    "password": os.getenv("DB_PASSWORD", "1q2w3e4r"),
    "connect_timeout": int(os.getenv("DB_CONNECT_TIMEOUT", "5"))
}

MQTT_HOST = os.getenv("MQTT_HOST", "127.0.0.1")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_KEEPALIVE = int(os.getenv("MQTT_KEEPALIVE", "60"))

def fetch_mapping():
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("SET search_path TO core, public")
        query = "SELECT mac_address, process_type, line_code, equip_name, plant_bd, plant_cd FROM v_topic_mapping;"
        cur.execute(query)

        new_mapping = {}
        for row in cur.fetchall():
            new_mapping[row[0]] = {
                "process_type": row[1],
                "line_code": row[2],
                "equip_name": row[3],
                "plant_bd": row[4],
                "plant_cd": row[5]
            }
        cur.close()
        return new_mapping
    except Exception as e:
        print(f"DB 로드 에러: {e}")
        return None
    finally:
        if conn: conn.close()

def fetch_sensor_data_by_mac(mac_address):
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("SET search_path TO core, public")

        # sensor_mst 테이블에서 해당 mac_address를 가진 모든 데이터를 조회
        query = "SELECT * FROM sensor_mst WHERE mac_address = %s;"
        cur.execute(query, (mac_address,))

        # 결과를 딕셔너리 리스트로 변환
        columns = [desc[0] for desc in cur.description]
        sensors = [dict(zip(columns, row)) for row in cur.fetchall()]

        cur.close()
        return sensors
    except Exception as e:
        print(f"센서 DB 직접 조회 에러: {e}")
        return []
    finally:
        if conn: conn.close()

def update_mapping_loop():
    global DEVICE_MAP
    while True:
        try:
            print("DB 매핑 데이터 동기화 중...")
            latest_map = fetch_mapping()
            if latest_map is not None:
                with map_lock:
                    DEVICE_MAP = latest_map
                print(f"동기화 완료: {len(DEVICE_MAP)}개 장치")
        except Exception as e:
            print(f"매핑 루프 치명적 에러: {e}")
        time.sleep(60)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("MQTT 브로커 연결 성공")

        client.subscribe("C-S/request-topic")
        client.subscribe("C-S/request-sensor_cd")
        print("구독 시작: request-topic, request-sensor_cd")
    else:
        print(f"연결 실패 (결과 코드: {rc})")

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print(f"MQTT 연결 끊김 (코드: {rc}). 재연결을 시도합니다...")

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        mac = payload.get("mac")
        if not mac: return

        if msg.topic == "C-S/request-topic":
            with map_lock:
                info = DEVICE_MAP.get(mac)

            response_topic = f"S-C/request-topic/{mac}"
            if info:
                response_payload = {
                    "topic": f'{info["plant_cd"]}/{info["plant_bd"]}/{info["process_type"]}/{info["line_code"]}/{info["equip_name"]}/-/'
                }
            else:
                response_payload = {"topic": "Unknown MAC"}

            client.publish(response_topic, json.dumps(response_payload))
            print(f"[Topic Response] MAC: {mac}")

        elif msg.topic == "C-S/request-sensor_cd":
            response_topic = f"S-C/request-sensor_cd/{mac}"
            sensor_data = fetch_sensor_data_by_mac(mac)

            # 조회된 데이터가 없으면 빈 리스트 [] 전송
            client.publish(response_topic, json.dumps(sensor_data))
            print(f"[Sensor Response] MAC: {mac}, Data Count: {len(sensor_data)}")

    except Exception as e:
        print(f"메시지 처리 에러: {e}")

def main():
    global DEVICE_MAP
    print(f"Topic Sender Ver 2.0.0")
    initial_map = fetch_mapping()
    if initial_map:
        DEVICE_MAP = initial_map
        print(f"초기 데이터 {len(DEVICE_MAP)}건 로드 성공")

    update_thread = threading.Thread(target=update_mapping_loop, daemon=True)
    update_thread.start()

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    while True:
        try:
            print("시스템 가동 시작...")
            client.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE)
            client.loop_forever()
        except Exception as e:
            print(f"MQTT 메인 루프 에러: {e}. 5초 후 재시작합니다.")
            time.sleep(5)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n사용자에 의해 종료되었습니다.")
