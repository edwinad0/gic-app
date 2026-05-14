from src.connection import init_db
from src.profiles import insert_profile

# Simple task extractor for test data
def extract_tasks_from_description(desc):
    tasks = []
    for line in desc.split("."):
        line = line.strip()
        if len(line) > 5:
            tasks.append(line)
    return tasks


# ------------------------------
# TEST DATA
# ------------------------------
extra_profiles = [
    {
        "lead": "Peter Smith",
        "title": "Quality Programme Lead Engineer",
        "grade": "D",
        "description": (
            "Interrogate & summarise customer data. "
            "Assure programme deliverables. "
            "Fresh Eyes Audit."
        ),
        "skills": [
            "Data Analysis",
            "Presentation Generation & Delivery",
            "Engineering Process Knowledge",
            "Manufacturing Process Knowledge"
        ]
    },
    {
        "lead": "John White",
        "title": "Quality Issue Prevention Engineer",
        "grade": "D",
        "description": (
            "Interrogate & summarise customer data. "
            "FMEA generation. "
            "DRBFM facilitation."
        ),
        "skills": [
            "Data Analysis",
            "Presentation Generation & Delivery",
            "Engineering Process Knowledge",
            "Manufacturing Process Knowledge"
        ]
    },
    {
        "lead": "James Heaton",
        "title": "Quality WCPA Auditor",
        "grade": "B",
        "description": (
            "Inspect product to audit guidelines. "
            "Prepare audit reports. "
            "Support supplier audit."
        ),
        "skills": [
            "Cosmetic Audit",
            "Functional Audit",
            "Presenting Feedback",
            "Data Entry"
        ]
    },
    {
        "lead": "Philip Stock",
        "title": "Quality Emissions Test Team Leader",
        "grade": "C",
        "description": (
            "Manage emissions test schedule. "
            "Physical vehicle emissions test. "
            "Ensure coverage for testing requirement."
        ),
        "skills": [
            "Workload Planning",
            "People Management",
            "Engineering Process Knowledge",
            "Manufacturing Process Knowledge"
        ]
    },
    {
        "lead": "Peter Critchlow",
        "title": "Quality Digital Project Lead",
        "grade": "D",
        "description": (
            "Deliver digital solutions. "
            "Maintain website. "
            "Manage digital requests."
        ),
        "skills": [
            "Programming",
            "Data Analysis",
            "Presentation Generation & Delivery",
            "Reporting and Feedback"
        ]
    },
    {
        "lead": "Laura Hart",
        "title": "Quality Diagnosis Operations Leader",
        "grade": "D",
        "description": (
            "Issue diagnosis. "
            "Prepare diagnosis reports. "
            "Component test management."
        ),
        "skills": [
            "Problem Solving",
            "Presentation Generation & Delivery",
            "Engineering Process Knowledge",
            "Manufacturing Process Knowledge"
        ]
    },
    {
        "lead": "Geoff Taylor",
        "title": "Quality Management System Auditor",
        "grade": "C",
        "description": (
            "Audit core process. "
            "Author processes. "
            "Report audit findings."
        ),
        "skills": [
            "Auditing",
            "Workload Planning",
            "Business Process Knowledge",
            "Reporting and Feedback"
        ]
    },
    {
        "lead": "Sean McDonald",
        "title": "Quality Certification Engineer",
        "grade": "D",
        "description": (
            "Documentation of conformance. "
            "Witness testing. "
            "Government liaison."
        ),
        "skills": [
            "Presentation Generation & Delivery",
            "Data Analysis",
            "Engineering Process Knowledge",
            "Programme Delivery Awareness"
        ]
    },
    {
        "lead": "Bruce Ball",
        "title": "Quality Digital & Data Infrastructure Lead",
        "grade": "D",
        "description": (
            "Maintenance of quality data. "
            "Quality data reporting. "
            "Data process governance."
        ),
        "skills": [
            "Programming",
            "Data Analysis",
            "Process Authoring",
            "Reporting and Feedback"
        ]
    },
    {
        "lead": "Harriet Blythe",
        "title": "Quality Senior PVT Engineer",
        "grade": "D",
        "description": (
            "Vehicle plant quality improvement. "
            "Engineering releasing. "
            "Supplier delivery."
        ),
        "skills": [
            "Problem Solving",
            "Data Analysis",
            "Reporting and Feedback",
            "Change Management"
        ]
    }
]

more_profiles = ([
    # ------------------------------
    # Quality Programme Lead Engineer (D)
    # ------------------------------
    {
        "lead": "Sophie Turner",
        "title": "Quality Programme Lead Engineer",
        "grade": "D",
        "description": (
            "Review customer quality trends to identify emerging issues. "
            "Coordinate programme-level quality actions with engineering teams. "
            "Prepare quality status updates for senior stakeholders."
        ),
        "skills": [
            "Data Analysis",
            "Programme Delivery Awareness",
            "Presentation Generation & Delivery",
            "Engineering Process Knowledge",
            "Manufacturing Process Knowledge"
        ]
    },
    {
        "lead": "Marcus Doyle",
        "title": "Quality Programme Lead Engineer",
        "grade": "D",
        "description": (
            "Analyse customer feedback to drive programme improvements. "
            "Support cross-functional reviews to assure deliverables. "
            "Conduct Fresh Eyes assessments on key programme milestones."
        ),
        "skills": [
            "Data Analysis",
            "Fresh Eyes Audit",
            "Engineering Process Knowledge",
            "Manufacturing Process Knowledge",
            "Reporting and Feedback"
        ]
    },

    # ------------------------------
    # Quality Issue Prevention Engineer (D)
    # ------------------------------
    {
        "lead": "Emily Carter",
        "title": "Quality Issue Prevention Engineer",
        "grade": "D",
        "description": (
            "Perform early issue detection through customer data interrogation. "
            "Lead FMEA workshops with engineering teams. "
            "Facilitate DRBFM sessions to prevent recurrence of issues."
        ),
        "skills": [
            "FMEA",
            "DRBFM",
            "Data Analysis",
            "Engineering Process Knowledge",
            "Manufacturing Process Knowledge"
        ]
    },
    {
        "lead": "Nathan Hughes",
        "title": "Quality Issue Prevention Engineer",
        "grade": "D",
        "description": (
            "Analyse warranty trends to identify potential failure modes. "
            "Support engineering teams in generating robust FMEAs. "
            "Deliver DRBFM reviews for high-risk components."
        ),
        "skills": [
            "FMEA",
            "DRBFM",
            "Data Analysis",
            "Presentation Generation & Delivery",
            "Manufacturing Process Knowledge"
        ]
    },

    # ------------------------------
    # Quality WCPA Auditor (B)
    # ------------------------------
    {
        "lead": "Holly Bennett",
        "title": "Quality WCPA Auditor",
        "grade": "B",
        "description": (
            "Conduct cosmetic and functional audits on finished vehicles. "
            "Document audit findings and prepare summary reports. "
            "Support supplier audit activities when required."
        ),
        "skills": [
            "Cosmetic Audit",
            "Functional Audit",
            "Data Entry",
            "Presenting Feedback",
            "Reporting and Feedback"
        ]
    },
    {
        "lead": "Ryan Mitchell",
        "title": "Quality WCPA Auditor",
        "grade": "B",
        "description": (
            "Inspect vehicles against WCPA standards. "
            "Record defects and escalate critical issues. "
            "Assist in supplier quality assessments."
        ),
        "skills": [
            "Cosmetic Audit",
            "Functional Audit",
            "Data Entry",
            "Auditing",
            "Communication"
        ]
    },

    # ------------------------------
    # Quality Emissions Test Team Leader (C)
    # ------------------------------
    {
        "lead": "Chloe Ward",
        "title": "Quality Emissions Test Team Leader",
        "grade": "C",
        "description": (
            "Plan and allocate emissions test activities. "
            "Oversee physical emissions testing on vehicles. "
            "Ensure test coverage meets programme requirements."
        ),
        "skills": [
            "Workload Planning",
            "People Management",
            "Engineering Process Knowledge",
            "Manufacturing Process Knowledge",
            "Reporting and Feedback"
        ]
    },
    {
        "lead": "Adam Farrell",
        "title": "Quality Emissions Test Team Leader",
        "grade": "C",
        "description": (
            "Manage daily emissions test operations. "
            "Coordinate test resources to meet deadlines. "
            "Review test results and escalate anomalies."
        ),
        "skills": [
            "Workload Planning",
            "Engineering Process Knowledge",
            "Manufacturing Process Knowledge",
            "Data Analysis",
            "Team Leadership"
        ]
    },

    # ------------------------------
    # Quality Digital Project Lead (D)
    # ------------------------------
    {
        "lead": "Zara Collins",
        "title": "Quality Digital Project Lead",
        "grade": "D",
        "description": (
            "Develop digital tools to support quality operations. "
            "Manage enhancement requests for existing platforms. "
            "Provide reporting dashboards for quality leadership."
        ),
        "skills": [
            "Programming",
            "Data Analysis",
            "Reporting and Feedback",
            "Presentation Generation & Delivery",
            "Digital Systems Knowledge"
        ]
    },
    {
        "lead": "Ethan Walsh",
        "title": "Quality Digital Project Lead",
        "grade": "D",
        "description": (
            "Deliver digital improvements for quality workflows. "
            "Maintain internal quality websites and portals. "
            "Analyse user requirements to shape digital solutions."
        ),
        "skills": [
            "Programming",
            "Data Analysis",
            "Process Authoring",
            "Reporting and Feedback",
            "Stakeholder Management"
        ]
    },

    # ------------------------------
    # Quality Diagnosis Operations Leader (D)
    # ------------------------------
    {
        "lead": "Grace O’Connor",
        "title": "Quality Diagnosis Operations Leader",
        "grade": "D",
        "description": (
            "Lead diagnosis activities for complex quality issues. "
            "Prepare detailed diagnosis reports for engineering teams. "
            "Coordinate component testing to validate root causes."
        ),
        "skills": [
            "Problem Solving",
            "Engineering Process Knowledge",
            "Manufacturing Process Knowledge",
            "Presentation Generation & Delivery",
            "Data Analysis"
        ]
    },
    {
        "lead": "Callum Reeves",
        "title": "Quality Diagnosis Operations Leader",
        "grade": "D",
        "description": (
            "Oversee issue diagnosis for high-impact concerns. "
            "Manage component test scheduling. "
            "Support engineering teams with structured problem-solving."
        ),
        "skills": [
            "Problem Solving",
            "Data Analysis",
            "Engineering Process Knowledge",
            "Manufacturing Process Knowledge",
            "Reporting and Feedback"
        ]
    }
])



# ------------------------------
# INITIALISE DB + LOAD DATA
# ------------------------------

print("Initialising database...")
init_db()

print("Loading dummy profiles...")

for person in more_profiles:
    tasks = extract_tasks_from_description(person["description"])
    insert_profile(
        person["lead"],
        person["title"],
        person["grade"],
        person["description"],
        tasks,
        person["skills"]
    )

print("Dummy data loaded successfully.")
