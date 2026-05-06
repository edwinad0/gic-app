import csv
import random

# 350 task-like sentences
task_sentences = [
    "Act as single point of contact for clients",
    "Provide coordinated access to products and services",
    "Manage and develop relationships with key clients",
    "Review client financial statements regularly",
    "Meet senior executives to understand long-term strategies",
    "Build rapport with client contacts",
    "Serve as a trusted advisor to clients",
    "Execute client instructions accurately and on time",
    "Proactively suggest solutions to client needs",
    "Develop specialised product knowledge for the covered sector",
    "Prepare client briefing materials",
    "Document client interactions in CRM systems",
    "Coordinate internal teams to deliver client solutions",
    "Monitor client satisfaction metrics",
    "Escalate client issues to senior management when required",
    "Support onboarding of new client accounts",
    "Analyse client portfolio performance",
    "Identify cross-selling opportunities",
    "Prepare proposals for client meetings",
    "Track follow-up actions from client discussions",
    "Participate in internal product training sessions",
    "Review regulatory requirements relevant to client activities",
    "Ensure compliance with internal policies",
    "Assist with audit requests",
    "Maintain accurate client documentation",
    "Prepare internal reports for management",
    "Collaborate with risk teams on client assessments",
    "Support junior team members with task execution",
    "Delegate routine tasks to analysts",
    "Manage complex client-related projects",
    "Resolve client issues efficiently",
    "Communicate updates to stakeholders",
    "Prepare financial summaries for client reviews",
    "Coordinate meeting logistics",
    "Track deadlines for deliverables",
    "Update internal knowledge bases",
    "Draft client communication templates",
    "Review client onboarding documents",
    "Assist with KYC updates",
    "Monitor industry trends relevant to clients",
    "Prepare competitive analysis summaries",
    "Attend client events and networking sessions",
    "Support development of new service offerings",
    "Assist with internal process improvements",
    "Participate in team planning sessions",
    "Review internal workflow documentation",
    "Provide feedback on operational bottlenecks",
    "Support implementation of new tools",
    "Test new internal systems",
    "Document process changes",
    "Prepare training materials for new hires",
] 

# 350 non-task sentences
non_task_sentences = [
    "The company operates in over 40 countries",
    "This role requires strong communication skills",
    "The department supports a wide range of business functions",
    "Employees are encouraged to participate in learning programs",
    "The organisation values innovation and collaboration",
    "This position reports to the regional head of operations",
    "The team works closely with other business units",
    "The company has a long history of client service excellence",
    "This role is part of a broader transformation initiative",
    "The position may require occasional travel",
    "The company provides a comprehensive benefits package",
    "The role sits within the client coverage division",
    "The organisation is committed to diversity and inclusion",
    "The team structure may evolve over time",
    "The company invests heavily in technology",
    "This role contributes to strategic objectives",
    "The department is undergoing process improvements",
    "The organisation encourages cross-functional collaboration",
    "The role requires familiarity with industry trends",
    "The company supports flexible working arrangements",
] 

rows = []

# Build dataset
for sentence in task_sentences:
    rows.append([sentence, 1])

for sentence in non_task_sentences:
    rows.append([sentence, 0])

# Shuffle
random.shuffle(rows)

# Write CSV
with open("task_training_data.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["sentence", "is_task"])
    writer.writerows(rows)

print(f"Generated task_training_data.csv with {len(rows)} samples.")
