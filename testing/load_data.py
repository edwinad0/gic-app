from src import insert_profile, init_db

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
        "lead": "Hannah O’Neill",
        "title": "Manufacturing Quality Engineer",
        "grade": "A",
        "description": (
            "Supports daily production quality checks. Analyses scrap trends. "
            "Updates PFMEAs. Collaborates with maintenance teams to reduce downtime."
        ),
        "skills": ["Root Cause Analysis", "PFMEA", "SPC", "Lean", "Process Auditing"]
    },
    {
        "lead": "Daniel Murphy",
        "title": "Manufacturing Quality Engineer",
        "grade": "A",
        "description": (
            "Manages supplier non‑conformances. Performs incoming inspection analysis. "
            "Leads supplier corrective action reviews."
        ),
        "skills": ["Supplier Quality", "8D Problem Solving", "APQP", "Quality Auditing", "Root Cause Analysis"]
    },
    {
        "lead": "Oliver Hayes",
        "title": "Manufacturing Quality Engineer",
        "grade": "A",
        "description": (
            "Conducts root cause investigations. Updates control plans. "
            "Collaborates with operators to improve first‑time‑through performance."
        ),
        "skills": ["Root Cause Analysis", "Control Plans", "SPC", "Lean", "Quality Auditing"]
    },
    {
        "lead": "Aidan McCarthy",
        "title": "Data Analyst",
        "grade": "B",
        "description": (
            "Builds dashboards for reporting. Cleanses large datasets. "
            "Performs exploratory data analysis. Defines KPIs with stakeholders."
        ),
        "skills": ["SQL", "Python", "Power BI", "Data Cleaning", "Statistics"]
    },
    {
        "lead": "Saoirse Dunne",
        "title": "Business Analyst",
        "grade": "B",
        "description": (
            "Gathers business requirements. Maps current processes. "
            "Identifies workflow inefficiencies. Supports project documentation."
        ),
        "skills": ["Process Mapping", "Documentation", "Stakeholder Management", "UML", "Data Analysis"]
    },
    {
        "lead": "Declan Byrne",
        "title": "Project Manager",
        "grade": "A",
        "description": (
            "Oversees project timelines. Manages risks. Coordinates cross‑functional teams. "
            "Ensures successful delivery of milestones."
        ),
        "skills": ["Project Planning", "Risk Management", "Agile", "Communication", "Leadership"]
    },
    {
        "lead": "Niamh Kelleher",
        "title": "Software Developer",
        "grade": "B",
        "description": (
            "Develops backend APIs. Writes unit tests. Reviews pull requests. "
            "Collaborates with QA to resolve defects."
        ),
        "skills": ["Python", "Django", "REST APIs", "Unit Testing", "Git"]
    },
    {
        "lead": "Patrick O’Shea",
        "title": "Software Developer",
        "grade": "A",
        "description": (
            "Implements new features. Optimises database queries. "
            "Supports CI/CD pipelines. Participates in sprint planning."
        ),
        "skills": ["JavaScript", "React", "SQL", "CI/CD", "Agile"]
    },
    {
        "lead": "Ciara Nolan",
        "title": "Cybersecurity Analyst",
        "grade": "B",
        "description": (
            "Monitors SIEM alerts. Investigates security incidents. "
            "Performs vulnerability scans. Supports awareness training."
        ),
        "skills": ["SIEM", "Incident Response", "Networking", "Python", "Risk Assessment"]
    },
    {
        "lead": "Shane Gallagher",
        "title": "DevOps Engineer",
        "grade": "A",
        "description": (
            "Maintains CI/CD pipelines. Automates deployments. "
            "Manages cloud infrastructure. Monitors system performance."
        ),
        "skills": ["CI/CD", "Docker", "Kubernetes", "AWS", "Linux"]
    },
    {
        "lead": "Ava Donnelly",
        "title": "HR Business Partner",
        "grade": "B",
        "description": (
            "Supports employee relations. Coaches managers. "
            "Leads engagement initiatives. Manages performance processes."
        ),
        "skills": ["Employee Relations", "Coaching", "Communication", "Conflict Resolution", "Talent Development"]
    },
    {
        "lead": "Eoin Walsh",
        "title": "Manufacturing Technician",
        "grade": "C",
        "description": (
            "Operates production machinery. Performs routine equipment checks. "
            "Records process data. Supports maintenance activities."
        ),
        "skills": ["Machine Operation", "Safety Compliance", "Data Recording", "Lean", "Troubleshooting"]
    },
    {
        "lead": "Molly Keegan",
        "title": "Manufacturing Technician",
        "grade": "C",
        "description": (
            "Monitors production lines. Inspects components. "
            "Documents defects. Assists with equipment changeovers."
        ),
        "skills": ["Quality Inspection", "Documentation", "Lean", "SPC", "Teamwork"]
    },
    {
        "lead": "Ronan Doyle",
        "title": "Quality Auditor",
        "grade": "B",
        "description": (
            "Conducts internal audits. Reviews process compliance. "
            "Documents findings. Supports corrective actions."
        ),
        "skills": ["Auditing", "ISO Standards", "Documentation", "Root Cause Analysis", "Communication"]
    },
    {
        "lead": "Aoife Brennan",
        "title": "Supply Chain Planner",
        "grade": "B",
        "description": (
            "Analyses demand trends. Manages inventory levels. "
            "Coordinates with suppliers. Prepares weekly reports."
        ),
        "skills": ["Forecasting", "Inventory Management", "Excel", "Supplier Management", "Data Analysis"]
    },
    {
        "lead": "Liam O’Rourke",
        "title": "Logistics Coordinator",
        "grade": "C",
        "description": (
            "Schedules shipments. Tracks deliveries. "
            "Communicates with carriers. Resolves logistics issues."
        ),
        "skills": ["Scheduling", "SAP", "Communication", "Problem Solving", "Data Entry"]
    },
    {
        "lead": "Erin McGrath",
        "title": "Finance Analyst",
        "grade": "B",
        "description": (
            "Prepares financial reports. Analyses cost trends. "
            "Supports budgeting cycles. Reconciles accounts."
        ),
        "skills": ["Excel", "Financial Modelling", "Reporting", "SQL", "Attention to Detail"]
    },
    {
        "lead": "Conor Higgins",
        "title": "Data Engineer",
        "grade": "A",
        "description": (
            "Builds ETL pipelines. Manages cloud storage. "
            "Optimises SQL queries. Ensures data quality."
        ),
        "skills": ["Python", "SQL", "Airflow", "AWS", "ETL"]
    },
    {
        "lead": "Maeve O’Donnell",
        "title": "Product Owner",
        "grade": "A",
        "description": (
            "Defines product backlog. Prioritises features. "
            "Works with developers. Gathers stakeholder feedback."
        ),
        "skills": ["Agile", "Backlog Management", "Communication", "User Stories", "Leadership"]
    },
    {
        "lead": "Sean Kavanagh",
        "title": "Test Automation Engineer",
        "grade": "B",
        "description": (
            "Develops automated test scripts. Maintains test frameworks. "
            "Executes regression suites. Reports defects."
        ),
        "skills": ["Selenium", "Python", "Automation", "CI/CD", "JIRA"]
    },
    {
        "lead": "Katie Byrne",
        "title": "UX Designer",
        "grade": "B",
        "description": (
            "Creates wireframes. Designs user flows. "
            "Conducts usability testing. Collaborates with developers."
        ),
        "skills": ["Figma", "User Research", "Prototyping", "Accessibility", "Communication"]
    },
    {
        "lead": "Owen Fitzpatrick",
        "title": "IT Support Engineer",
        "grade": "C",
        "description": (
            "Resolves helpdesk tickets. Installs software. "
            "Troubleshoots hardware issues. Supports end users."
        ),
        "skills": ["Troubleshooting", "Windows", "Networking", "Customer Service", "Documentation"]
    },
    {
        "lead": "Isla McKenna",
        "title": "Operations Coordinator",
        "grade": "B",
        "description": (
            "Tracks operational KPIs. Prepares daily reports. "
            "Coordinates team schedules. Supports process improvements."
        ),
        "skills": ["Excel", "Reporting", "Scheduling", "Communication", "Organisation"]
    },
    {
        "lead": "Cillian Reilly",
        "title": "Maintenance Technician",
        "grade": "C",
        "description": (
            "Performs equipment repairs. Conducts preventive maintenance. "
            "Troubleshoots faults. Documents maintenance activities."
        ),
        "skills": ["Mechanical Repair", "Diagnostics", "Safety", "Tools", "Documentation"]
    }
]


# ------------------------------
# INITIALISE DB + LOAD DATA
# ------------------------------

print("Initialising database...")
init_db()

print("Loading dummy profiles...")

for person in extra_profiles:
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
