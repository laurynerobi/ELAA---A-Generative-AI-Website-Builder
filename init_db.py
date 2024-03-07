from main import app
from models import db, WebsiteTemplate, Page


def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


def init_db():
    with app.app_context():
        db.create_all()

        # Check if the database is empty
        if WebsiteTemplate.query.count() == 0:
            # Create the base template
            ecommerce_template = WebsiteTemplate(name='ecommerce', is_base_template=True)
            db.session.add(ecommerce_template)

            # Add pages to the ecommerce template
            ecommerce_pages_info = [
                ('Home', 'templates/preview_templates/ecommerce/homepage.html', 'static/preview_static/ecommerce/styles.css', 'static/preview_static/ecommerce/script.js'),
                ('About', 'templates/preview_templates/ecommerce/about.html', 'static/preview_static/ecommerce/styles.css', 'static/preview_static/ecommerce/script.js'),
                ('Products', 'templates/preview_templates/ecommerce/products.html', 'static/preview_static/ecommerce/styles.css', 'static/preview_static/ecommerce/script.js'),
                ('Contact', 'templates/preview_templates/ecommerce/contact.html', 'static/preview_static/ecommerce/styles.css', 'static/preview_static/ecommerce/script.js'),
            ]

            for page_name, html_path, css_path, js_path in ecommerce_pages_info:
                html_content = read_file(html_path)
                css_content = read_file(css_path)
                js_content = read_file(js_path)

                new_page = Page(template=ecommerce_template, page_name=page_name, html_content=html_content, css_content=css_content, js_content=js_content)
                db.session.add(new_page)

            # Create the portfolio base template
            portfolio_template = WebsiteTemplate(name='portfolio', is_base_template=True)
            db.session.add(portfolio_template)

            # Add pages to the portfolio template
            portfolio_pages_info = [
                ('Home', 'templates/preview_templates/portfolio/homepage.html', 'static/preview_static/portfolio/portfolioStyle.css', 'static/preview_static/portfolio/portfolioScript.js'),
                ('About', 'templates/preview_templates/portfolio/about.html', 'static/preview_static/portfolio/portfolioStyle.css', 'static/preview_static/portfolio/portfolioScript.js'),
                ('Contact', 'templates/preview_templates/portfolio/contact.html', 'static/preview_static/portfolio/portfolioStyle.css', 'static/preview_static/portfolio/portfolioScript.js'),
            ]

            for page_name, html_path, css_path, js_path in portfolio_pages_info:
                html_content = read_file(html_path)
                css_content = read_file(css_path)
                js_content = read_file(js_path)

                new_page = Page(template=portfolio_template, page_name=page_name, html_content=html_content, css_content=css_content, js_content=js_content)
                db.session.add(new_page)

            db.session.commit()


if __name__ == '__main__':
    init_db()
