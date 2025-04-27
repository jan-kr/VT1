from db import Session
from models import *

session = Session()

baumituns = Company(
    name="BauMitUns GmbH",
    description="KMU mit OneDrive Datenverwaltung und Bauverwaltungssoftware auf Tower-PC",
    industry="Bau",
    employee_count=1,
)

# session.add(baumituns)
session.commit()

attributes = [
    CompanyAttribute(company_id=baumituns.id, key="cloud_storage", value="OneDrive"),
    CompanyAttribute(company_id=baumituns.id, key="has_backups", value="no"),
    CompanyAttribute(company_id=baumituns.id, key="os_type", value="Windows 11"),
]

# session.add_all(attributes)
session.commit()

control = SecurityControl(
    control_id="11",
    title="Data Recovery",
    description="Establish and maintain data recovery practices sufficient to restore in-scope enterprise assets to a pre-incident and trusted state",
    category="Data",
    framework="CIS"
)

# session.add(control)
session.commit()
control = session.query(SecurityControl).filter_by(control_id="11").first()

safeguards = [
    Safeguard(
        safeguard_id="11.1",
        title="Establish and Maintain a Data Recovery Process",
        description="Establish and maintain a documented data recovery process. In the process, address the scope of data recovery activities, recovery prioritization, and the security of backup data. Review and update documentation annually, or when significant enterprise changes occur that could impact this Safeguard.",
        control_id=control.id,
    ),
Safeguard(
        safeguard_id="11.2",
        title="Perform Automated Backups",
        description="Perform automated backups of in-scope enterprise assets. Run backups weekly, or more frequently, based on the sensitivity of the data.",
        control_id=control.id,
    ),
Safeguard(
        safeguard_id="11.3",
        title="Protect Recovery Data",
        description="Protect recovery data with equivalent controls to the original data. Reference encryption or data separation, based on requirements.",
        control_id=control.id,
    ),
Safeguard(
        safeguard_id="11.4",
        title="Establish and Maintain an Isolated Instance of Recovery Data",
        description="Establish and maintain an isolated instance of recovery data. Example implementations include, version controlling backup destinations through offline, cloud, or off-site systems or services.",
        control_id=control.id,
    ),
]

# session.add_all(safeguards)
session.commit()

safeguard = session.query(Safeguard).filter_by(safeguard_id="11.2").first()
template = RecommendationTemplate(
    safeguard_id=safeguard.id,
    title="Template Recommendation for Safeguard " + str(safeguard.safeguard_id),
    description_template="Create an automated Backuptask for your {{ system_type }} Systems {{ frequency }} to the Backuptarget {{ target }}.",
    parameters_required=["system_type", "frequency", "target"]
)
# session.add(template)
session.commit()

presets = [
    ParameterPreset(
        template_id=template.id,
        match_criteria={"os_type": "Windows"},
        parameters={
            "os_type": "Windows Server 2022",
            "frequency": "daily",
            "target": "USB-Disk",
        }
    ),
    ParameterPreset(
        template_id=template.id,
        match_criteria={"os_type": "Linux"},
        parameters={
            "os_type": "Debian Server",
            "frequency": "daily",
            "target": "NAS with rsync",
        }
    ),
    ParameterPreset(
        template_id=template.id,
        match_criteria={"os_type": "macOS"},
        parameters={
            "os_type": "macOS",
            "frequency": "weekly",
            "target": "Time machine Backup to external Disk"
        }
    )
]

# session.add_all(presets)
session.commit()

from services.company_service import create_company, delete_company
# wviz = create_company(
#     session=session,
#     name="Wir verkaufen ihr Zeug AG",
#     description="Online Handelsplattform zum Verkauf von gebrauchten Waren",
#     industry="Commerce",
#     employee_count=25,
# )

ag = AttributeGroup(
    group_type="operating_system",
    label="Windows 10"
)
#session.add(ag)
session.commit()

agv1 = AttributeGroupValue(
    key="os_type",
    value="Windows",
    group_id=ag.id,
)
#session.add(agv1)
session.commit()

agv2 = AttributeGroupValue(
    key="os_version",
    value="10",
    group_id=ag.id,
)
#session.add(agv2)
session.commit()

ag = AttributeGroup(
    group_type="operating_system",
    label="Windows 11"
)
#session.add(ag)
session.commit()

agv1 = AttributeGroupValue(
    key="os_type",
    value="Windows",
    group_id=ag.id,
)
#session.add(agv1)
session.commit()

agv2 = AttributeGroupValue(
    key="os_version",
    value="11",
    group_id=2,
)

#session.add(agv2)
session.commit()


company = session.query(Company).filter_by(name="BauMitUns GmbH").first()
cag = CompanyAttributeGroup(
    company_id=company.id,
    group_id=2,
)
#session.add(cag)
session.commit()

for group in company.linked_attribute_groups:
    print(group.group.dict())

session.close()