from fyi import app, auto

from flask import render_template, request
from datetime import datetime
from glob import glob

@app.route('/', methods=['GET'])
@auto.doc()
def indexPage():
    languages = glob('../languages/*/')
    projects = []
    for language in languages:
        projects += glob(language + '*/')
    names = list(set([project.split('/')[3] for project in projects]))
    descriptions = []
    for name in names:
        with open('../descriptions/' + name, 'r') as description_file:
            descriptions.append(description_file.readlines()[-1])
    return render_template(
        "index.html",
        projects=[
            {
                "name": name,
                "description": description
            } for name, description in zip(names, descriptions)
        ],
        languages=[language.split('/')[2] for language in languages]
    )

@app.route('/languages/<string:language>', methods=['GET'])
@auto.doc()
def languagePage(language):
    projects = glob('../languages/' + language + '/*/')
    return render_template(
        "language.html",
        language=language,
        projects=list(set([project.split('/')[3] for project in projects])),
    )

@app.route('/projects/<string:project>', methods=['GET'])
@auto.doc()
def projectPage(project):
    languages = glob('../languages/*/')
    languages_with_project = []
    for language in languages:
        if project in [project_folder.split('/')[-2] for project_folder in glob(language + '*/')]:
            languages_with_project.append(language.split('/')[-2])
    with open('../descriptions/' + project, 'r') as description_file:
        description = description_file.readlines()[-1]
    return render_template(
        "project.html",
        project=project,
        description=description,
        languages=[
            {
                "name": language,
                "code": lookup(language, project)
            } for language in languages_with_project
        ]
    )

def lookup(language, project):
    project_dir = '../languages/' + language + '/' + project + '/'
    if language == 'python':
        with open(project_dir + 'Solution.py', 'r') as solution_file:
            solution = solution_file.read()
        with open(project_dir + 'TestCase.py', 'r') as test_file:
            tests = test_file.read()
    elif language == 'bash':
        with open(project_dir + 'Solution.sh', 'r') as solution_file:
            solution = solution_file.read()
        with open(project_dir + 'TestCase.sh', 'r') as test_file:
            tests = test_file.read()
    elif language == 'groovy':
        with open(project_dir + 'src/main/groovy/Solution.groovy', 'r') as solution_file:
            solution = solution_file.read()
        with open(project_dir + 'src/test/groovy/TestCase.groovy', 'r') as test_file:
            tests = test_file.read()
    elif language == 'java':
        with open(project_dir + 'src/main/java/Solution.java', 'r') as solution_file:
            solution = solution_file.read()
        with open(project_dir + 'src/test/java/TestCase.java', 'r') as test_file:
            tests = test_file.read()
    return {
	"solution": solution, 
	"tests": tests
    }




