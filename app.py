import pandas as pd
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

sheets = {
    "hour": pd.read_excel("data/hourly.xlsx"),
    "daily": pd.read_excel("data/daily.xlsx"),
    "week": pd.read_excel("data/week.xlsx"),
    "month": pd.read_excel("data/month.xlsx")
}  # keep your file in /data/
# Convert 'datum' column to datetime for all sheets
for key in sheets:
    sheets[key]['datum'] = pd.to_datetime(sheets[key]['datum'], errors='coerce')

@app.route('/')
def index():
    return render_template('index.html')



# Endpoint to get column names (drug list)
@app.route('/get_drugs')
def get_drugs():
    # skip first column 'datum'
    #drugs = df.columns[1:].tolist()
    drugs = sheets['month'].columns[1:].tolist()
    return jsonify(drugs)

# Endpoint to get time series for selected drug
@app.route('/get_data/<drug>')
def get_data(drug):
    if drug not in df.columns:
        return jsonify({"error": "Drug not found"}), 404
    data = {
        "dates": df["datum"].tolist(),
        "values": df[drug].tolist()
    }
    return jsonify(data)

# Endpoint to upload new Excel/CSV data
# @app.route('/upload', methods=["POST"])
# def upload():
#     file = request.files['file']
#     if file.filename.endswith(".csv"):
#         new_df = pd.read_csv(file)
#     else:
#         new_df = pd.read_excel(file)
    
#     global df
#     df = pd.concat([df, new_df], ignore_index=True)
#     return jsonify({"message": "File uploaded and data appended successfully."})

@app.route('/analysis')
def analysis():
    # Get query params (optional: from submit button)
    drug = request.args.get("drug")
    time_range = request.args.get("time_range") # hour month week month

    # If no drug selected yet → just load page
    if not drug or not time_range:
        return render_template("Analysis.html", drug=None)

    df=sheets[time_range]  # Get the DataFrame for the selected time range
    # Otherwise send the drug + data to template
    if drug not in df.columns:
        data = {
            "dates": [],
            "values": []
        }
        return render_template("Analysis.html", drug=None, error="Drug not found")
    dates = df['datum'].dt.strftime('%Y-%m-%d').tolist()
    values = df[drug].tolist()
    data = {
    "dates": dates,
    "values": values
}
    return render_template("Analysis.html", drug=drug, data=data, timerange=time_range)




@app.route('/forecasting')
def forecasting():
    return render_template('Forcasting.html')

@app.route('/strategy')
def strategy():
    return render_template('Stratergy.html')

if __name__ == '__main__':
    app.run(debug=True)