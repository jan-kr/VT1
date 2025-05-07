from sqlalchemy.orm import selectinload

import services.init
from db import Session
from models import *
from services import company_service, recommendation_generator_service


def gen(session, safeguard, company):
    templates = session.query(RecommendationTemplate).filter_by(safeguard_id=safeguard.id).all()

    for template in templates:
        presets = recommendation_generator_service.get_matching_presets(session, template)

        presets = [preset for preset in presets if criteria_in_list(preset.match_criteria, company.all_attributes())]
        for preset in presets:
            print('-', recommendation_generator_service.generate_recommendations(session, safeguard, preset))


# def preset_matcher(session):
#     company = session.query(Company).filter_by(name="BauMitUns GmbH").first()
#     safeguard = session.query(Safeguard).filter_by(safeguard_id="11.2").first()
#     templates = session.query(RecommendationTemplate).filter_by(safeguard_id=safeguard.id).all()
#
#     for template in templates:
#         presets = recommendation_generator_service.get_matching_presets(session, template)
#
#         for preset in presets:
#             ags = recommendation_generator_service.get_matching_attribute_groups(session, preset, company)
#
#             for ag in ags:
#                 print(recommendation_generator_service.generate_recommendations(session, safeguard, preset))
#

def criteria_in_list(criteria: dict, attribute_list: list[dict]) -> bool:
    return all(any(d.get(k) == v for d in attribute_list) for k, v in criteria.items())


if __name__ == "__main__":
    services.init.init_db()
    with Session() as session:
        safeguard = session.query(Safeguard).filter_by(safeguard_id="11.2").first()
        company = session.query(Company).filter_by(name="BauMitUns GmbH").first()

        gen(session, safeguard, company)
        # preset_matcher(session)
