# Therapeutic Insights Platform

A web application that helps mental health professionals generate case conceptualizations and treatment recommendations using AI assistance.

## Features
- Case conceptualization generation (including missing information identification)
- Treatment advice
- Research paper suggestions
- Privacy-focused design
- Copy and download functionality

## Prerequisites
- Python 3.8+
- Flask
- OpenAI API key

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/therapeutic-insights-platform.git
cd therapeutic-insights-platform
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install required packages:

```bash
pip install flask openai python-dotenv
```

4. Create a `.env` file in the root directory and add your OpenAI API key:

```
OPENAI_API_KEY=your_api_key_here
```

## Running the Application

1. Ensure your virtual environment is activated

2. Start the Flask server:

```bash
python app.py
```

3. Open your web browser and navigate to:

```
http://localhost:5000
```

## Usage

1. Enter an anonymized client description in the text area
2. Click "Get Advice & Case Conceptualization"
3. View the generated:
   - Case conceptualization
   - Treatment advice
4. Generate research suggestions as needed
5. Use the copy/download buttons to save the information

## Privacy Considerations
- No client information is stored by the application
- All data is processed through OpenAI's API
- Users should ensure all information is properly anonymized
- Review OpenAI's privacy policy and terms of use for API data handling

## Development

The application uses:
- Flask for the backend
- Bootstrap 5 for styling
- Alpine.js for reactive components
- HTMX for dynamic loading
- Marked.js for markdown rendering

## File Structure

```
therapeutic-insights-platform/
├── app.py                 # Flask application
├── templates/
│   └── index.html        # Main HTML template, includes all the frontend code
└── README.md             # Documentation
```

## Author

Developed by Alex Smith

## Acknowledgments
- OpenAI for API services
- Bootstrap for UI components
- PAIR dataset from University of Michigan (https://lit.eecs.umich.edu/downloads.html#PAIR)
- Other libraries and frameworks used

## Additional Setup
Create a `.gitignore` file in your root directory and add:

```
.env
__pycache__/
venv/
*.pyc
```
