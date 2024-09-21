pipeline {
  agent any
  stages {
    stage('Build Docker Image') {
      steps {
        sh 'docker build -t 820242905325.dkr.ecr.ap-south-1.amazonaws.com/elephant-tusk-classification .'
        sh 'docker push 820242905325.dkr.ecr.ap-south-1.amazonaws.com/elephant-tusk-classification:latest'
      }
    }
    stage('Deploy to EC2') {
      steps {
        sh 'ssh -i your-key.pem ubuntu@3.6.126.251 "docker pull 820242905325.dkr.ecr.ap-south-1.amazonaws.com/elephant-tusk-classification:latest && docker run -d -p 8080:8080 elephant-tusk-classification:latest"'
      }
    }
  }
}
