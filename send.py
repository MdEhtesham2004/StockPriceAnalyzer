from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv
import os 
load_dotenv()


STOCKS_ENDPOINT_HTML = os.getenv("STOCKS_ENDPOINT_HTML")




def extract_stocks_data():
    response = requests.get(STOCKS_ENDPOINT_HTML)
    data = response.text
    soup = BeautifulSoup(data, "html.parser")

    table = soup.find("table")  # You can use more specific selectors if needed
    rows = table.find_all("tr")

    # Step 1: Extract the data from the table
    table_data = []
    for row in rows:
        cells = row.find_all(["td", "th"])
        cell_data = [cell.get_text(strip=True) for cell in cells]
        table_data.append(cell_data)

    # Step 2: Create an HTML structure
    html_content = """
    {% extends "index.html" %}
    {% block content %}
    <html>
    <head>
        <link rel="stylesheet" type="text/css" href="{{ url_for('static',filename='output.css')}}">

    </head>
    <body>
    <table>
    """
    for row_data in table_data:
        html_content += "<tr>"
        for cell in row_data:
            html_content += f"<td>{cell}</td>"
        html_content += "</tr>"
    html_content += "</table></body></html>{% endblock %}"

    # Step 3: Write the HTML structure to a file
    with open("templates/output.html", "w",encoding="utf-8") as file:
        file.write(html_content)