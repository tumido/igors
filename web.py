from flask import Flask, render_template, request, jsonify

from utils.sensors import DHT_HUM, DHT_TEMP, DS_TEMP, HEATER_POWER

app = Flask(
    __name__,
    static_url_path="",
    static_folder="frontend/out",
    template_folder="frontend/out",
)


@app.route("/")
def hello():
    return render_template("index.html")


@app.route("/api/igors", methods=["GET", "POST"])
def igors():
    if request.method == "GET":
        return jsonify(
            {
                "above": DHT_TEMP.read(),
                "below": DS_TEMP.read(),
                "humidity": DHT_HUM.read(),
                "heater": HEATER_POWER.read(),
            }
        )

    HEATER_POWER.set(request.json.get("heater"))
    return jsonify(message="Success")


if __name__ == "__main__":
    app.run()
