from jinja2 import Template, Environment, FileSystemLoader
from db import Session
from models import *
from sqlalchemy.orm import selectinload


def generate_recommendations(session, safeguard: Safeguard, preset: ParameterPreset):
    template = session.query(RecommendationTemplate).filter_by(safeguard_id=safeguard.id).first()

    if not template or not preset:
        #raise Exception("No template or preset found for safeguard with matching criteria")
        return False

    jinja_template = Template(template.description_template)
    rendered_text = jinja_template.render(**preset.parameters)

    return rendered_text


def get_matching_presets(session, template):
    required_set = set(template.parameters_required)

    presets = session.query(ParameterPreset).all() #TODO: fetch only presets for given template
    return [
        preset for preset in presets
        if required_set.issubset(preset.parameters.keys())
    ]

def get_matching_attribute_groups(session, preset: ParameterPreset, company = None):
    match_dict = preset.match_criteria

    if company is not None:
        groups = [group.group for group in company.linked_attribute_groups]
    else:
        groups = session.query(AttributeGroup).options(
            selectinload(AttributeGroup.attributes)
        ).all()

    matching_groups = []

    for group in groups:
        if all(group.dict().get(k) == v for k, v in match_dict.items()):
            matching_groups.append(group)

    return matching_groups


def render_scenario(scenario, context):
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template(f"{scenario}.html.j2")

    manual = template.render(context)

    return manual

def render_full(context, title):
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template("base.html.j2")

    manual = template.render({
        "content": context,
        "title": title,
    })

    return manual

def save_html(content):
    with open('output.html', 'w', encoding='utf-8') as f:
        f.write(content)