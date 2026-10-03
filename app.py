from flask import Flask, render_template, jsonify, request
import sqlite3

from modules.trust import calculate_trust
from modules.fusion import calculate_fusion
from modules.simulator import generate_sensor_data


app = Flask(__name__)

DATABASE = "database.db"


# ==================== DATABASE CONNECTION ====================

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn



@app.route("/")
def home():
    return render_template("dashboard.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/sensors")
def sensors():
    return render_template("sensors.html")


@app.route("/fusion")
def fusion():
    return render_template("fusion.html")


@app.route("/failure")
def failure():
    return render_template("failure.html")


@app.route("/results")
def results():
    return render_template("results.html")


# Compatibility routes for existing HTML links
@app.route("/dashboard.html")
def dashboard_html():
    return render_template("dashboard.html")


@app.route("/sensors.html")
def sensors_html():
    return render_template("sensors.html")


@app.route("/fusion.html")
def fusion_html():
    return render_template("fusion.html")


@app.route("/failure.html")
def failure_html():
    return render_template("failure.html")


@app.route("/results.html")
def results_html():
    return render_template("results.html")
# ==================== CREATE TABLES ====================

def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sensors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            status TEXT NOT NULL,
            trust_score REAL,
            signal_quality REAL,
            availability REAL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS detections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uav_id TEXT NOT NULL,
            sensor TEXT NOT NULL,
            confidence REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sensor_readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sensor TEXT NOT NULL,
            signal_quality REAL,
            availability REAL,
            reliability REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fusion_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            method TEXT NOT NULL,
            confidence REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS failure_tests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sensor TEXT NOT NULL,
            condition TEXT NOT NULL,
            trust_before REAL,
            trust_after REAL,
            confidence_before REAL,
            confidence_after REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


# ==================== SAMPLE SENSORS ====================

def insert_sample_sensors():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM sensors")
    count = cursor.fetchone()[0]

    if count == 0:
        sensors = [
            ("Radar", "Active", 0.94, 0.92, 0.98),
            ("RF", "Active", 0.89, 0.87, 0.95),
            ("EO/IR", "Active", 0.91, 0.90, 0.97)
        ]

        cursor.executemany("""
            INSERT INTO sensors
            (name, status, trust_score, signal_quality, availability)
            VALUES (?, ?, ?, ?, ?)
        """, sensors)

        conn.commit()

    conn.close()


# ==================== SENSOR API ====================

@app.route("/api/sensors")
def api_sensors():

    sensors = [
        {
            "name": "Radar",
            "status": "Active",
            "signal_quality": 0.92,
            "availability": 0.98,
            "reliability": 0.95,
            "trust": 0.94
        },
        {
            "name": "RF",
            "status": "Active",
            "signal_quality": 0.87,
            "availability": 0.95,
            "reliability": 0.90,
            "trust": 0.89
        },
        {
            "name": "EO/IR",
            "status": "Active",
            "signal_quality": 0.90,
            "availability": 0.97,
            "reliability": 0.92,
            "trust": 0.91
        }
    ]

    return jsonify(sensors)


# ==================== DETECTION API ====================

@app.route("/api/detections", methods=["GET"])
def get_detections():
    conn = get_db_connection()

    detections = conn.execute(
        "SELECT * FROM detections ORDER BY timestamp DESC"
    ).fetchall()

    conn.close()

    return [dict(detection) for detection in detections]


@app.route("/api/detections", methods=["POST"])
def add_detection():
    data = request.get_json()

    uav_id = data.get("uav_id")
    sensor = data.get("sensor")
    confidence = data.get("confidence")

    if not uav_id or not sensor or confidence is None:
        return {
            "error": "uav_id, sensor and confidence are required"
        }, 400

    conn = get_db_connection()

    conn.execute("""
        INSERT INTO detections
        (uav_id, sensor, confidence)
        VALUES (?, ?, ?)
    """, (uav_id, sensor, confidence))

    conn.commit()
    conn.close()

    return {
        "message": "Detection added successfully"
    }, 201


# ==================== SENSOR READINGS API ====================

@app.route("/api/readings", methods=["GET"])
def get_sensor_readings():
    conn = get_db_connection()

    readings = conn.execute(
        "SELECT * FROM sensor_readings ORDER BY timestamp DESC"
    ).fetchall()

    conn.close()

    return [dict(reading) for reading in readings]


@app.route("/api/readings", methods=["POST"])
def add_sensor_reading():
    data = request.get_json()

    sensor = data.get("sensor")
    signal_quality = data.get("signal_quality")
    availability = data.get("availability")
    reliability = data.get("reliability")

    if (
        not sensor
        or signal_quality is None
        or availability is None
        or reliability is None
    ):
        return {
            "error": "sensor, signal_quality, availability and reliability are required"
        }, 400

    trust_score = calculate_trust(
        signal_quality,
        availability,
        reliability
    )

    conn = get_db_connection()

    conn.execute("""
        INSERT INTO sensor_readings
        (sensor, signal_quality, availability, reliability)
        VALUES (?, ?, ?, ?)
    """, (
        sensor,
        signal_quality,
        availability,
        reliability
    ))

    conn.execute("""
        UPDATE sensors
        SET trust_score = ?,
            signal_quality = ?,
            availability = ?
        WHERE name = ?
    """, (
        trust_score,
        signal_quality,
        availability,
        sensor
    ))

    conn.commit()
    conn.close()

    return {
        "message": "Sensor reading added successfully",
        "sensor": sensor,
        "trust_score": trust_score
    }, 201


# ==================== FUSION API ====================

@app.route("/api/fusion", methods=["GET"])
def get_fusion_results():
    conn = get_db_connection()

    results = conn.execute(
        "SELECT * FROM fusion_results ORDER BY timestamp DESC"
    ).fetchall()

    conn.close()

    return [dict(result) for result in results]


@app.route("/api/fusion", methods=["POST"])
def add_fusion_result():
    data = request.get_json()

    sensor_data = data.get("sensor_data")

    if not sensor_data:
        return {
            "error": "sensor_data is required"
        }, 400

    try:
        final_confidence = calculate_fusion(sensor_data)
    except Exception as e:
        return {
            "error": str(e)
        }, 400

    conn = get_db_connection()

    conn.execute("""
        INSERT INTO fusion_results
        (method, confidence)
        VALUES (?, ?)
    """, (
        "Trust-Weighted Fusion",
        final_confidence
    ))

    conn.commit()
    conn.close()

    return {
        "message": "Fusion result calculated successfully",
        "method": "Trust-Weighted Fusion",
        "final_confidence": final_confidence
    }, 201


# ==================== SIMULATION API ====================

@app.route("/api/simulate", methods=["GET"])
def simulate_sensors():

    simulated_data = generate_sensor_data()

    results = []

    for sensor in simulated_data:

        trust_score = calculate_trust(
            sensor["signal_quality"],
            sensor["availability"],
            sensor["reliability"]
        )

        results.append({
            "sensor": sensor["sensor"],
            "signal_quality": sensor["signal_quality"],
            "availability": sensor["availability"],
            "reliability": sensor["reliability"],
            "confidence": sensor["confidence"],
            "trust": trust_score
        })

    # Calculate final fusion confidence
    final_confidence = calculate_fusion(results)

    return {
        "type": "simulated_data",
        "sensors": results,
        "fusion": {
            "method": "Trust-Weighted Fusion",
            "final_confidence": final_confidence
        }
    }

# ==================== FAILURE TEST API ====================

@app.route("/api/failure-test", methods=["GET"])
def get_failure_tests():
    conn = get_db_connection()

    tests = conn.execute(
        "SELECT * FROM failure_tests ORDER BY timestamp DESC"
    ).fetchall()

    conn.close()

    return [dict(test) for test in tests]


@app.route("/api/failure-test", methods=["POST"])
def add_failure_test():
    data = request.get_json()

    sensor = data.get("sensor")
    condition = data.get("condition")
    trust_before = data.get("trust_before")
    trust_after = data.get("trust_after")
    confidence_before = data.get("confidence_before")
    confidence_after = data.get("confidence_after")

    if (
        not sensor
        or not condition
        or trust_before is None
        or trust_after is None
        or confidence_before is None
        or confidence_after is None
    ):
        return {
            "error": "sensor, condition, trust_before, trust_after, confidence_before and confidence_after are required"
        }, 400

    conn = get_db_connection()

    conn.execute("""
        INSERT INTO failure_tests
        (
            sensor,
            condition,
            trust_before,
            trust_after,
            confidence_before,
            confidence_after
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        sensor,
        condition,
        trust_before,
        trust_after,
        confidence_before,
        confidence_after
    ))

    conn.commit()
    conn.close()

    return {
        "message": "Failure test added successfully"
    }, 201


# ==================== START SERVER ====================

if __name__ == "__main__":
    create_tables()
    insert_sample_sensors()
    app.run(debug=True)