import os
from flask import Flask, render_template, request, session, jsonify
from models import db, WebsiteTemplate, Page
from TestFlow import conversation_flow
from OpenCAI import CAIFlow, Node

# Create a Flask web application instance
app = Flask(__name__)
app.secret_key = os.urandom(24)

# Configure the SQLAlchemy part of the app instance
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # Initialize the database with the Flask app

# Global variable to track if the init code has run
has_initialized = False


@app.before_request
def before_request():
    global has_initialized
    if not has_initialized:
        # Initialize the database schema (create tables) only once
        db.create_all()
        has_initialized = True


# Import Blueprints after db and models is created
from template_routes import template_blueprint

# Register Blueprints
app.register_blueprint(template_blueprint)

''''''''''''''''''''''''''''''''''''''''''''' ROUTES '''''''''''''''''''''''''''''''''''''''''''''''''''


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/builder', methods=['GET'])
def builder():
    return render_template("builder.html")


@app.route('/main', methods=['GET'])
def main():
    template_type = request.args.get('type', 'default')  # 'default' is a fallback

    session['website_type'] = template_type

    # Load the original template based on type
    template = WebsiteTemplate.query.filter_by(name=template_type, is_base_template=True).first()

    if template:
        initial_page = fetch_initial_page_content(template.id)
        return render_template("main.html", template_id=template.id, initial_page_content=initial_page)
    else:
        return render_template("main.html", error="Template not found")


def fetch_initial_page_content(template_id):
    # Example: Fetch the 'home' page of the template
    page = Page.query.filter_by(template_id=template_id, page_name='Home').first()
    if page:
        return page.html_content
    return None


def update_template_with_name():
    website_name = session.get('website_name')
    template = WebsiteTemplate.query.filter_by(name=session.get('website_type'), is_base_template=True).first()
    updated_html_content = template.html_content.replace('{{ Business_name }}', website_name)
    template.html_content = updated_html_content
    db.session.commit()


@app.route('/conversation', methods=['POST'])
def manage_conversation():
    # Initialize or retrieve the conversation flow from the session
    if 'current_node_name' not in session:
        testFlow = conversation_flow()
        session['current_node_name'] = testFlow.flowStart.nodeName
        testFlow.currentNode = testFlow.flowStart  # Ensure currentNode is initialized
        # Now you can safely generate the initial response
        response = {
            "GeneratedText": testFlow.generateText(),
            "UserInputOptions": testFlow.getUserInputOptions()
        }


    else:
        testFlow = conversation_flow()
        testFlow.set_current_node_by_name(session['current_node_name'])
        user_input = request.json.get('message', '')
        response = testFlow.processNode(user_input)
        session['current_node_name'] = testFlow.currentNode.nodeName

        # Storing the website name from the user, this happens in node3
        if session['current_node_name'] == 'TestNode3':
            session['website_name'] = user_input
            print('Business name:', session['website_name'])
            print('Session data:', session)  # Print all session data

            update_template_with_name()  # Update the template with the new business name
        session['current_node_name'] = testFlow.currentNode.nodeName

    return jsonify(response)  # Send the response back to the client


# Start the Flask application if this script is executed directly
if __name__ == '__main__':
    app.run(debug=True)
