# SKILLS AND TASK INTELLIGENCE PLATFORM 

The Skills & Task Intelligence Platform is a **data‑driven prototype** designed to help organisations understand the real work happening inside quality roles, identify opportunities for efficiency, and support employee development.

It combines task‑level analysis, AI‑enabled classification, and skills intelligence to reveal where automation, augmentation, and upskilling can create the biggest impact.

The platform is built for:

    Stakeholders who need visibility into workforce capability

    Managers who want to design efficient, resilient roles

    Employees in quality roles who want to understand their strengths and development opportunities 
    
## THE PROBLEM 
Enterprise quality roles are under pressure from:
- Talent shortages
- Rising operational costs
- Increasing digital demands
- Limited visibility into task‑level work
- Difficulty identifying upskilling and mobility opportunities

Teams spend significant time on repetitive or manual tasks that prevent them from focusing on strategic, creative, and people‑centred work.

Organisations need a smarter, data‑driven way to understand roles and design a future‑ready workforce.

## THE SOLUTION 
This platform provides:
- Task‑level analysis of real work
- **AI‑enabled task classification (Automatable / Augmentable / Human‑Critical)**
- Skill gap analysis for individuals and roles
- Career progression insights
- Interactive dashboards
- PDF report generation for stakeholders
- Job and person profile management

It helps organisations:
- Identify efficiency opportunities
- Support employee development
- Enable functional mobility
- Build a resilient, future‑ready quality workforce

## Features 
- Task Classification (AI - Powered)
- Skill Gap Analysis 
- Career Progression Insights 
- Radar Chart Visualisation
- PDF Report Generation
- Job & Person Profile Management 

## How the Classifier works
The classifier is implemented in `models/classifier.py`.

It uses:
- TF‑IDF vectorisation (unigrams + bigrams)
- Logistic Regression with class balancing
- Pickled model + vectorizer for fast inference

Training
```bash
python -c "from models.classifier import TaskClassifier; TaskClassifier().train()"
```
Evaluation
```bash
python -c "from models.classifier import TaskClassifier; TaskClassifier().evaluate()"
```
Prediction
The model:
- Recognises patterns in task wording
- Matches them to the most similar category
- Returns a confidence score


## Installtion and Running 
Install Dependencies 
```python
    pip install -r requirements.txt
```

Create and Activate Virtual Environment 
```python
    python3 -m venv .venv 
    source .venv/bin/activate 
```

Run the App 
```python
python app.py
```

Error Example: 

    Address already in use
    Port 8050 is in use by another program. Either identify and stop that program, or start the server with a different port.

    need to kill current port and run again 
        lsof -i :8050 
        kill -9 <PID> 


## PDF Report Structure
The generated PDF includes:

    Cover page
    Task radar
    Skill gap analysis
    Task classification table
    Career progression section (optional)

All styling uses inline CSS for maximum PDF compatibility.


## Roadmap 
    Add authentication
    Add admin dashboard
    Improve ML model with domain‑specific embeddings
    Add task extraction from free‑text role descriptions
    Add team‑level analytics
    Add export to Excel / CSV
    Add role similarity engine