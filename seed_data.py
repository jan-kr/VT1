from db import Session
from models import *


def init():
    session = Session()

    company = Company(
        name="BauMitUns GmbH",
        description="KMU mit OneDrive Datenverwaltung und Bauverwaltungssoftware auf Tower-PC",
        industry="Bau",
        employee_count=1,
    )

    session.add(company)
    session.commit()

    attributes = [
        CompanyAttribute(company_id=company.id, key="cloud_storage", value="OneDrive"),
        CompanyAttribute(company_id=company.id, key="has_backups", value="no"),
        CompanyAttribute(company_id=company.id, key="os_type", value="Windows 11"),
    ]

    session.add_all(attributes)
    session.commit()

    controls = [
        SecurityControl(
            control_id="1",
            title="Inventory of Enterprise Assets",
            description="Actively manage (inventory, track, and correct) all enterprise assets (end-user devices, including \
portable and mobile; network devices; non-computing/Internet of Things (IoT) devices; and servers) \
connected to the infrastructure physically, virtually, remotely, and those within cloud environments, to \
accurately know the totality of assets that need to be monitored and protected within the enterprise. \
This will also support identifying unauthorized and unmanaged assets to remove or remediate.",
            category="Inventory",
            framework="CIS"
        ),
        SecurityControl(
            control_id="2",
            title="Inventory of Software Assets",
            description="Actively manage (inventory, track, and correct) all software (operating systems and applications) on \
the network so that only authorized software is installed and can execute, and that unauthorized and \
unmanaged software is found and prevented from installation or execution.",
            category="Inventory",
            framework="CIS"
        ),
        SecurityControl(
            control_id="3",
            title="Data Protection",
            description="Develop processes and technical controls to identify, classify, securely handle, retain, and \
dispose of data.",
            category="Data",
            framework="CIS"
        ),
        SecurityControl(
            control_id="4",
            title="Secure Configuration of Enterprise Assets and Software",
            description="Establish and maintain the secure configuration of enterprise assets (end-user devices, including \
portable and mobile; network devices; non-computing/IoT devices; and servers) and software \
(operating systems and applications).",
            category="Configuration",
            framework="CIS"
        ),
        SecurityControl(
            control_id="5",
            title="Account Management",
            description="Use processes and tools to assign and manage authorization to credentials for user accounts, \
including administrator accounts, as well as service accounts, to enterprise assets and software.",
            category="Access Control",
            framework="CIS"
        ),
        SecurityControl(
            control_id="6",
            title="Access Control Management",
            description="Use processes and tools to create, assign, manage, and revoke access credentials and privileges for \
user, administrator, and service accounts for enterprise assets and software.",
            category="Access Control",
            framework="CIS"
        ),
        SecurityControl(
            control_id="7",
            title="Continuous Vulnerability Management",
            description="Develop a plan to continuously assess and track vulnerabilities on all enterprise assets within \
    the enterprise’s infrastructure, in order to remediate, and minimize, the window of opportunity for \
    attackers. Monitor public and private industry sources for new threat and vulnerability information.",
            category="Vulnerability Management",
            framework="CIS"
        ),
        SecurityControl(
            control_id="8",
            title="Audit Log Management",
            description="Collect, alert, review, and retain audit logs of events that could help detect, understand, or recover \
from an attack.",
            category="Logging",
            framework="CIS"
        ),
        SecurityControl(
            control_id="9",
            title="Email and Web Browser Protections",
            description="Improve protections and detections of threats from email and web vectors, as these are opportunities \
for attackers to manipulate human behavior through direct engagement.",
            category="Security Awareness",
            framework="CIS"
        ),
        SecurityControl(
            control_id="10",
            title="Malware Defenses",
            description="Prevent or control the installation, spread, and execution of malicious applications, code, or scripts on \
enterprise assets.",
            category="Malware",
            framework="CIS"
        ),
        SecurityControl(
            control_id="11",
            title="Data Recovery",
            description="Establish and maintain data recovery practices sufficient to restore in-scope enterprise assets to a \
pre-incident and trusted state.",
            category="Data",
            framework="CIS"
        ),
        SecurityControl(
            control_id="12",
            title="Network Infrastructure Management",
            description="Establish, implement, and actively manage (track, report, correct) network devices, in order to \
prevent attackers from exploiting vulnerable network services and access points.",
            category="Network",
            framework="CIS"
        ),
        SecurityControl(
            control_id="13",
            title="Security Awareness and Skills Training",
            description="Operate processes and tooling to establish and maintain comprehensive network monitoring and \
defense against security threats across the enterprise’s network infrastructure and user base.",
            category="Training",
            framework="CIS"
        ),
        SecurityControl(
            control_id="14",
            title="Security Function Testing",
            description="Establish and maintain a security awareness program to influence behavior among the workforce to \
be security conscious and properly skilled to reduce cybersecurity risks to the enterprise.",
            category="Testing",
            framework="CIS"
        ),
        SecurityControl(
            control_id="15",
            title="Service Provider Management",
            description="Develop a process to evaluate service providers who hold sensitive data, or are responsible for \
an enterprise’s critical IT platforms or processes, to ensure these providers are protecting those \
platforms and data appropriately.",
            category="Supply Chain",
            framework="CIS"
        ),
        SecurityControl(
            control_id="16",
            title="Application Software Security",
            description="Manage the security life cycle of in-house developed, hosted, or acquired software to prevent, detect, \
and remediate security weaknesses before they can impact the enterprise.",
            category="Application Security",
            framework="CIS"
        ),
        SecurityControl(
            control_id="17",
            title="Incident Response Management",
            description="Establish a program to develop and maintain an incident response capability (e.g., policies, plans, \
procedures, defined roles, training, and communications) to prepare, detect, and quickly respond to an attack.",
            category="Response",
            framework="CIS"
        ),
        SecurityControl(
            control_id="18",
            title="Penetration Testing",
            description="Test the effectiveness and resiliency of enterprise assets through identifying and exploiting \
weaknesses in controls (people, processes, and technology), and simulating the objectives and actions of an attacker.",
            category="Testing",
            framework="CIS"
        )
    ]
    session.add_all(controls)
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

    session.add_all(safeguards)
    session.commit()

    safeguard = session.query(Safeguard).filter_by(safeguard_id="11.2").first()
    template = RecommendationTemplate(
        safeguard_id=safeguard.id,
        title="Template Recommendation for Safeguard " + str(safeguard.safeguard_id),
        description_template="Create an automated Backuptask for your {{ os_type }} Systems {{ frequency }} to the Backuptarget {{ target }}.",
        parameters_required=["os_type", "frequency", "target"]
    )
    session.add(template)
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

    session.add_all(presets)
    session.commit()

    ag = AttributeGroup(
        group_type="operating_system",
        label="Windows 10"
    )
    # session.add(ag)
    session.commit()

    agv1 = AttributeGroupValue(
        key="os_type",
        value="Windows",
        group_id=ag.id,
    )
    # session.add(agv1)
    session.commit()

    agv2 = AttributeGroupValue(
        key="os_version",
        value="10",
        group_id=ag.id,
    )
    # session.add(agv2)
    session.commit()

    ag = AttributeGroup(
        group_type="operating_system",
        label="Windows 11"
    )
    session.add(ag)
    session.commit()

    agv1 = AttributeGroupValue(
        key="os_type",
        value="Windows",
        group_id=ag.id,
    )
    session.add(agv1)
    session.commit()

    agv2 = AttributeGroupValue(
        key="os_version",
        value="11",
        group_id=2,
    )

    session.add(agv2)
    session.commit()

    session.close()
