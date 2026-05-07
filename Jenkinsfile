pipeline {

    agent any

    environment {

        HEADLESS = 'true'

    }

    stages {


        stage('Checkout Code') {

            steps {

                checkout scm

                echo "Code downloaded successfully"
            }
        }


        stage('Install Dependencies') {

            steps {

                sh '''

                    python3 -m venv venv

                    . venv/bin/activate

                    pip install --upgrade pip

                    pip install -r requirements.txt

                '''
            }
        }


        stage('Run API Tests') {

            steps {

                sh '''

                    . venv/bin/activate

                    pytest tests/test_api_notes.py \
                    -v -m api \
                    --alluredir=reports/allure-results

                '''
            }
        }


        stage('Run UI Login Tests') {

            steps {

                sh '''

                    . venv/bin/activate

                    pytest tests/test_ui_login.py \
                    -v \
                    --alluredir=reports/allure-results

                '''
            }
        }


        stage('Run UI Notes Tests') {

            steps {

                sh '''

                    . venv/bin/activate

                    pytest tests/test_ui_notes.py \
                    -v \
                    --alluredir=reports/allure-results

                '''
            }
        }


        stage('Run E2E Tests') {

            steps {

                sh '''

                    . venv/bin/activate

                    pytest tests/test_e2e_hybrid.py \
                    -v \
                    --alluredir=reports/allure-results

                '''
            }
        }


        stage('Generate Allure Report') {

            steps {

                allure([

                    includeProperties: false,

                    reportBuildPolicy: 'ALWAYS',

                    results: [[path: 'reports/allure-results']]

                ])
            }
        }


        stage('Archive Reports') {

            steps {

                archiveArtifacts(
                    artifacts: 'reports/**/*',
                    fingerprint: true
                )

                echo "Reports archived successfully"
            }
        }
    }


    post {

        success {

            echo "All tests passed"
        }

        failure {

            echo "Build failed"
        }

        always {

            echo "Pipeline execution completed"
        }
    }
}
