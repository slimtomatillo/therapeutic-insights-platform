from flask import Flask, request, jsonify, render_template
from openai import OpenAI
import requests
import os

app = Flask(__name__)

# Set your API keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PUBMED_API_URL = "https://pubmed.ncbi.nlm.nih.gov/api/v1/articles"
SEMANTIC_SCHOLAR_API_URL = "https://api.semanticscholar.org/v1/paper"

client = OpenAI(api_key=OPENAI_API_KEY)

# Route: Homepage
@app.route("/")
def home():
    return render_template("index.html")

# Route: Generate Case Conceptualization and Advice
@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        if not data or "user_input" not in data:
            return jsonify({"error": "Invalid input. Please provide 'user_input' in JSON format."}), 400

        user_input = data["user_input"]

        # OpenAI Prompt for Case Conceptualization
        conceptualization_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a mental health counselor."},
                {"role": "user", "content": f"""Based on the following description, generate a structured case conceptualization including:
                - Presenting Problem
                - Relevant History
                - Strengths and Resources
                - Case Formulation
                - Treatment Plan

                Input: {user_input}"""}
            ]
        )

        # Extract the response content
        conceptualization = conceptualization_response.choices[0].message.content

        # Generate actionable advice
        advice_prompt = f"""
        Based on the following conceptualization, generate 3 pieces of actionable advice for the counselor to help the client, with links to supporting research:
        {conceptualization}.
        """

        # OpenAI Prompt for actionable advice based on conceptualization
        advice_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a mental health counselor."},
                {"role": "user", "content": f"""{advice_prompt}"""}
            ]
        )

        # Extract the response content
        advice = advice_response.choices[0].message.content

        return jsonify({"conceptualization": conceptualization, "advice": advice})

    except Exception as e:
        # Log the error for debugging
        print(f"Error in /generate route: {e}")
        return jsonify({"error": str(e)}), 500  # Return the actual error message

# Route: Fetch and Summarize Research
@app.route("/research", methods=["POST"])
def research():
    try:
        data = request.get_json()
        topic = data.get("topic")
        
        # Query Semantic Scholar API
        url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={topic}&fields=title,abstract,url&limit=3"
        response = requests.get(url, headers={"Accept": "application/json"})
        
        if response.status_code != 200:
            return jsonify([{
                "title": "API Error",
                "url": "#",
                "summary": "Unable to fetch research at this time."
            }])

        papers = response.json().get("data", [])
        
        # If no papers found, return specific message
        if not papers:
            return jsonify([{
                "title": "No Results",
                "url": "#",
                "summary": f"No research papers found for '{topic}'. Try modifying your search terms."
            }])
        
        research_results = []
        for paper in papers:
            # Handle missing data gracefully
            title = paper.get("title", "No title available")
            url = paper.get("url", "#")
            abstract = paper.get("abstract")
            
            # Only add papers with meaningful content
            if title and title != "No title available":
                research_results.append({
                    "title": title,
                    "url": url,
                    "summary": abstract[:200] + "..." if abstract else "No abstract available"
                })
        
        # If no valid results after filtering
        if not research_results:
            return jsonify([{
                "title": "No Results",
                "url": "#",
                "summary": f"No valid research results found for '{topic}'. Please try different search terms."
            }])
        
        return jsonify(research_results)

    except Exception as e:
        print(f"Error in research route: {str(e)}")  # Log the error
        return jsonify([{
            "title": "Search Error",
            "url": "#",
            "summary": "We encountered an error while searching. Please try different search terms or try again later."
        }])

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
