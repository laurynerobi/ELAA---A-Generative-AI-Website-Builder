from flask import Blueprint, render_template, request
from models import db, WebsiteTemplate, Page
import logging
import uuid

template_blueprint = Blueprint('template_blueprint', __name__)


@template_blueprint.route('/template/<template_name>')
def template(template_name):
    # Template retrieval logic
    return render_template(f'{template_name}.html')


@template_blueprint.route('/template_content/<int:template_id>/<page_name>')
def template_page_content(template_id, page_name):
    template = WebsiteTemplate.query.get(template_id)
    if template:
        page = Page.query.filter_by(template_id=template_id, page_name=page_name).first()
        if page:
            return page.html_content
        return "Page not found", 404
    return "Template not found", 404