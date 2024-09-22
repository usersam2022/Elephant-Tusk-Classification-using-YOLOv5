pipeline {
    agent any
    stages {
        stage('Build Docker Image') {
            steps {
                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: 'aws-ecr-credentials'
                ]]) {
                    sh 'aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin 820242905325.dkr.ecr.ap-south-1.amazonaws.com'
                    sh 'docker build -t 820242905325.dkr.ecr.ap-south-1.amazonaws.com/elephant-tusk-classification .'
                    sh 'docker push 820242905325.dkr.ecr.ap-south-1.amazonaws.com/elephant-tusk-classification:latest'
                }
            }
        }
        stage('Confirm Deployment') {
            steps {
                script {
                    def userInput = input(
                        id: 'UserInput',
                        message: 'Code change detected. Do you want to deploy it?',
                        parameters: [
                            [$class: 'BooleanParameterDefinition', name: 'Deploy', defaultValue: false, description: 'Check to deploy the changes']
                        ]
                    )
                    if (!userInput) {
                        currentBuild.result = 'ABORTED'
                        error('Deployment aborted by user.')
                    }
                }
            }
        }
        stage('Deploy to EC2') {
            steps {
                sh 'ssh -i /home/ubuntu/.ssh/tusk_ec2-deployment-key.pem ubuntu@3.109.121.137 "docker pull 820242905325.dkr.ecr.ap-south-1.amazonaws.com/elephant-tusk-classification:latest && docker run -d -p 8080:8080 elephant-tusk-classification:latest"'
            }
        }
    }
}
