import services.init
from db import Session
from models import *
from services import company_service, recommendation_generator_service, helpers
import argparse
import pprint


def gen(session, safeguard, company):
    templates = session.query(RecommendationTemplate).filter_by(safeguard_id=safeguard.id).all()

    for template in templates:
        presets = recommendation_generator_service.get_matching_presets(session, template)
        presets = [preset for preset in presets if criteria_in_list(preset.match_criteria, company.all_attributes())]
        for preset in presets:
            print('-', recommendation_generator_service.generate_recommendations(session, safeguard, preset))

def mode_backup(filename):
    job = helpers.read_json(filename)
    scenario = f"backup_{job['source_server']['os'].lower()}_to_{job['target_server']['os'].lower()}"


    context = {
        "source_host": job['source_server']['hostname'],
        "source_paths": job['source_server']['data_to_backup'],
        "target_base": job['target_server']['target_base_path'],
        "target_host": job['target_server']['hostname'],
        "target_user": job['target_server']['access']['username'],
        "target_share": job['target_server']['access']['share'] if job['target_server']['access']['method'] == "smb" else "",
        "rsync_options": "-avz --delete" if job.get('backup_options', {}).get('incremental', False) else "-avz",
        "target_folder": "$TARGET_FOLDER" if job.get('backup_options', {}).get('versioning', False) else
        f"{job['target_server']['target_base_path']}/{job['source_server']['hostname']}",
        "incremental": job.get('backup_options', {}).get('incremental', False),
        "versioning": job.get('backup_options', {}).get('versioning', False),
        "retention_days": job.get('backup_options', {}).get('retention_days', 0),
    }

    return {
        "scenario": scenario,
        "context": context,
    }


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
        # print(company.all_attributes())
        #gen(session, safeguard, company)

        parser = argparse.ArgumentParser(prog="CLI Implementation Guideline Generator",)
        parser.add_argument("-m", "--mode")
        parser.add_argument("-f", "--file")
        args = parser.parse_args()

        match args.mode:
            case "backup":
                context = mode_backup(args.file)
                pprint.pprint(context)
                print(recommendation_generator_service.render_scenario(context['scenario'], context["context"]))
            case _:
                print("No mode")
