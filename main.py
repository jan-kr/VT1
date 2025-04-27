from db import Session
from models import *
from services import company_service, recommendation_generator_service

def main(session):
    safeguard = session.query(Safeguard).filter_by(safeguard_id="11.2").first()
    company = session.query(Company).filter_by(name="WirVerkaufenIhrZeug AG").first()

    templates = session.query(RecommendationTemplate).filter_by(safeguard_id=safeguard.id).all()
    for template in templates:
        presets = session.query(ParameterPreset).filter_by(template_id=template.id).all()
        for preset in presets:
            for key in preset.matchKeys():
                companyAttributes = session.query(CompanyAttribute).filter_by(
                    company_id=company.id,
                    key=key
                ).all()
                for companyAttribute in companyAttributes:
                    print(recommendation_generator_service.generate_recommendations(session, safeguard.id, companyAttribute.dict()))

def attrgroups(session):
    safeguard = session.query(Safeguard).filter_by(safeguard_id="11.2").first()
    control = session.get(SecurityControl, safeguard.control_id)
    print(control.framework, 'Control', control.control_id, '-', control.title)
    print(control.description)
    print('')
    print('Safeguard', safeguard.safeguard_id, '-', safeguard.title)
    print(safeguard.description)
    print('')
    #company = session.query(Company).filter_by(name="BauMitUns GmbH").first()
    company = session.query(Company).filter_by(name="WirVerkaufenIhrZeug AG").first()

    templates = session.query(RecommendationTemplate).filter_by(safeguard_id=safeguard.id).all()

    for template in templates:
        for group in company.linked_attribute_groups:
            presets = session.query(ParameterPreset).filter_by(template_id=template.id).all()
            for preset in presets:
                if(preset.match_criteria == group.group.dict()):
                    print('-', recommendation_generator_service.generate_recommendations(session, safeguard.id, group.group.dict()))



if __name__ == "__main__":
    with Session() as session:
        #main(session)
        attrgroups(session)