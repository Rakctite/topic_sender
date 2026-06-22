import importlib
import json
import sys
import types
import unittest


def import_app_with_stubs():
    sys.modules.setdefault("psycopg2", types.SimpleNamespace(connect=None))
    mqtt_module = types.SimpleNamespace(Client=lambda: None)
    sys.modules.setdefault("paho", types.ModuleType("paho"))
    sys.modules.setdefault("paho.mqtt", types.ModuleType("paho.mqtt"))
    sys.modules["paho.mqtt.client"] = mqtt_module
    return importlib.import_module("app")


class FakeMessage:
    topic = "C-S/request-topic"

    def __init__(self, mac):
        self.payload = json.dumps({"mac": mac}).encode()


class FakeClient:
    def __init__(self):
        self.published = []

    def publish(self, topic, payload):
        self.published.append((topic, json.loads(payload)))


class TopicResponseTest(unittest.TestCase):
    def test_fetch_mapping_includes_sensor_type_from_view(self):
        app = import_app_with_stubs()

        class FakeCursor:
            description = []

            def __init__(self):
                self.queries = []

            def execute(self, query):
                self.queries.append(query)

            def fetchall(self):
                return [("AA:BB", "PROC", "L1", "EQ1", "B1", "P1", "TEMP")]

            def close(self):
                pass

        class FakeConnection:
            def __init__(self):
                self.cursor_instance = FakeCursor()

            def cursor(self):
                return self.cursor_instance

            def close(self):
                pass

        fake_connection = FakeConnection()
        app.psycopg2.connect = lambda **kwargs: fake_connection

        mapping = app.fetch_mapping()

        self.assertEqual(mapping["AA:BB"]["sensor_type"], "TEMP")

    def test_request_topic_uses_sensor_type_as_eighth_topic_level(self):
        app = import_app_with_stubs()
        app.DEVICE_MAP = {
            "AA:BB": {
                "plant_cd": "P1",
                "plant_bd": "B1",
                "process_type": "PROC",
                "line_code": "L1",
                "equip_name": "EQ1",
                "sensor_type": "TEMP",
            }
        }

        client = FakeClient()
        app.on_message(client, None, FakeMessage("AA:BB"))

        self.assertEqual(
            client.published,
            [
                (
                    "S-C/request-topic/AA:BB",
                    {"topic": "P1/B1/PROC/L1/EQ1/-/TEMP"},
                )
            ],
        )


if __name__ == "__main__":
    unittest.main()
