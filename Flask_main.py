from flask import Flask, jsonify, request
from databaseActions import DatabaseActions

app = Flask(__name__)

@app.route("/")
def home():
    name = request.args.get("name")

    if not name:
        return jsonify(Message="Please provide a name parameter in the query string."), 400
    
    personYears = DatabaseActions.list_years_by_person_name(name)

    if not personYears:
        return jsonify(Message=f"No records found for name '{name}'."), 404
    
    mostPopularYear = None
    tenMostPopularYears = None
    if personYears:
        sortedYears = sorted(personYears, key=lambda p: p.NumberOfOccurrences, reverse=True)
        mostPopularYear = sortedYears[0] if sortedYears else None
        tenMostPopularYears = sortedYears[:10]

    firstOccurenceYear = personYears[0] if personYears else None

    message = f'"name": "{name}", "first_year": {firstOccurenceYear.Year if firstOccurenceYear else "N/A"}, "most_popular_year": {mostPopularYear.Year if mostPopularYear else "N/A"}, "ten_most_popular_years": ['
    if tenMostPopularYears:
        message += ", ".join([f'"{year.Year}"' for year in tenMostPopularYears])
    message += "]"
    message += f', "estimated_age": "{2026 - sum(int(year.Year) for year in tenMostPopularYears) // len(tenMostPopularYears) if tenMostPopularYears else "N/A"}"'

    return jsonify(Message=message)
if __name__ == "__main__":
    app.run()