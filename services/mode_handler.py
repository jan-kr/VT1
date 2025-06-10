from services import helpers
from services.recommendation_generator_service import render_scenario
import pprint


def mode_backup(filename):
    job = helpers.read_json(filename)

    sources = job.get('source_servers', [])
    target = job.get('target_server', {})
    options = job.get('backup_options', {})

    if not sources:
        sources = [job.get('source_server', {})]

    content = ""
    for source in sources:
        context = gen_backup_recommendation(source, target, options)
        content += render_scenario(scenario=context['scenario'], context=context['context'])

    return content


def gen_backup_recommendation(source, target, options):
    scenario = f"backup_{source['os'].lower()}_to_{target['os'].lower()}"

    context = {
        "source_host": source['hostname'],
        "source_paths": source['data_to_backup'],
        "target_base": target['target_base_path'],
        "target_host": target['hostname'],
        "target_user": target['access']['username'],
        "target_share": target['access']['share'] if target['access']['method'] == "smb" else "",
        "target_folder": "$TARGET_FOLDER" if options.get('versioning', False) else
        f"{target['target_base_path']}/{source['hostname']}",
        "frequency": options.get('frequency', 0),
        "incremental": options.get('incremental', False),
        "versioning": options.get('versioning', False),
        "retention_days": options.get('retention_days', 0),
    }

    return {
        "scenario": scenario,
        "context": context
    }
