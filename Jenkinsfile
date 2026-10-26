pipeline {
    agent any

    options {
        timestamps()
        timeout(time: 30, unit: 'MINUTES')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Check Python Environment') {
            steps {
                bat '"C:\\Users\\soura\\AppData\\Local\\Programs\\Python\\Python312\\python.exe" --version'
            }
        }

        stage('Create Python Environment') {
            steps {
                bat '"C:\\Users\\soura\\AppData\\Local\\Programs\\Python\\Python312\\python.exe" -m venv .venv'

                bat '.venv\\Scripts\\python.exe -m pip install --upgrade pip'

                bat '.venv\\Scripts\\python.exe -m pip install -r requirements.txt'
            }
        }

        stage('API Smoke Tests') {
            steps {
                bat '''
                    .venv\\Scripts\\python.exe -m pytest -v tests/api ^
                        --junitxml=api-results.xml
                '''
            }
        }

        stage('UI Tests') {
            steps {
                bat 'if not exist reports mkdir reports'

                withEnv(['CI=true', 'HEADLESS=true']) {
                    bat '''
                        .venv\\Scripts\\python.exe -m pytest -v tests/ui ^
                            --junitxml=ui-results.xml ^
                            --alluredir=allure-results ^
                            --html=reports/pytest-report.html ^
                            --self-contained-html
                    '''
                }
            }
        }
    }

    post {
        always {
            junit(
                allowEmptyResults: true,
                testResults: '**/*results.xml'
            )

            archiveArtifacts(
                artifacts: 'reports/**,allure-results/**,*results.xml',
                allowEmptyArchive: true
            )
        }
    }
}