pipeline {
    agent any
    options { timestamps(); timeout(time: 30, unit: 'MINUTES') }
    stages {
        stage('Checkout') {
            steps { checkout scm }
        }
        stage('Create Python environment') {
            steps {
                sh 'python3 --version'
                sh 'python3 -m venv .venv'
                sh '.venv/bin/python -m pip install --upgrade pip'
                sh '.venv/bin/pip install -r requirements.txt'
            }
        }
        stage('API smoke tests') {
            steps {
                sh '.venv/bin/pytest -v tests/api --junitxml=api-results.xml'
            }
        }
        stage('UI tests') {
            steps {
                sh 'mkdir -p reports'
                sh 'HEADLESS=true .venv/bin/pytest -v tests/ui --alluredir=allure-results --html=reports/pytest-report.html --self-contained-html'
            }
        }
    }
    post {
        always {
            junit allowEmptyResults: true, testResults: '**/*results.xml'
            archiveArtifacts artifacts: 'reports/**,allure-results/**,api-results.xml', allowEmptyArchive: true
        }
    }
}
