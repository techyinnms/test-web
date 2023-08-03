from flask import Flask, render_template, request, Response
import pandas as pd

app = Flask(__name__)

# Load data from the Excel file
data = pd.read_csv("Data1.csv")

@app.route("/", methods=['GET', 'POST'])
def index():
    filtered_data = data.copy()
    filters_col1 = data['Col1'].unique()  # Unique categories in Col1
    filters_col3 = data['Col3'].unique()  # Unique categories in Col3

    if request.method == 'POST':
        selected_col1 = request.form.get('col1_filter')
        selected_col3 = request.form.get('col3_filter')

        if selected_col1:
            filtered_data = filtered_data[filtered_data['Col1'] == selected_col1]

        if selected_col3:
            filtered_data = filtered_data[filtered_data['Col3'] == selected_col3]

    return render_template("index.html", data=filtered_data.to_html(index=False, escape=False), filters_col1=filters_col1, filters_col3=filters_col3)

@app.route("/export", methods=['POST'])
def export_csv():
    filtered_data = data.copy()
    selected_col1 = request.form.get('col1_filter')
    selected_col3 = request.form.get('col3_filter')

    if selected_col1:
        filtered_data = filtered_data[filtered_data['Col1'] == selected_col1]

    if selected_col3:
        filtered_data = filtered_data[filtered_data['Col3'] == selected_col3]

    response = Response(filtered_data.to_csv(index=False), content_type='text/csv')
    response.headers['Content-Disposition'] = 'attachment; filename=filtered_data.csv'
    return response

if __name__ == "__main__":
    app.run(debug=True)
