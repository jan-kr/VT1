from jinja2 import Template
from db import Session
from models import *


def generate_recommendations(session, safeguard_id: int, match_criteria: dict):
    template = session.query(RecommendationTemplate).filter_by(safeguard_id=safeguard_id).first()
    preset = session.query(ParameterPreset).filter_by(
        template_id=template.id,
        match_criteria=match_criteria
    ).first()

    if not template or not preset:
        raise Exception("No template or preset found for safeguard with matching criteria")

    jinja_template = Template(template.description_template)
    rendered_text = jinja_template.render(**preset.parameters)

    return rendered_text
