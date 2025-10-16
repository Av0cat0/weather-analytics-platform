pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'weather-monitor'
        DOCKER_TAG = "${BUILD_NUMBER}"
    }
    
    stages {
        stage('Clone') {
            steps {
                echo 'Cloning repository...'
                checkout scm
                script {
                    def gitCommit = sh(returnStdout: true, script: 'git rev-parse HEAD').trim()
                    def gitBranch = sh(returnStdout: true, script: 'git rev-parse --abbrev-ref HEAD').trim()
                    echo "Git commit: ${gitCommit}"
                    echo "Git branch: ${gitBranch}"
                }
            }
        }
        
        stage('Build') {
            steps {
                echo 'Building Docker image...'
                script {
                    def image = docker.build("${DOCKER_IMAGE}:${DOCKER_TAG}")
                    echo "Built image: ${image.id}"
                }
            }
        }
        
        stage('Deploy') {
            steps {
                echo 'Deploying application...'
                script {
                    // Stop existing containers
                    sh 'docker-compose down weather_monitor || true'
                    
                    // Update the image tag in docker-compose
                    sh "sed -i 's|image: weather-monitor:.*|image: weather-monitor:${DOCKER_TAG}|g' docker-compose.yml || true"
                    
                    // Start the updated service
                    sh 'docker-compose up -d weather_monitor'
                    
                    // Wait for service to be healthy
                    sh '''
                        timeout 60 bash -c 'until docker-compose ps weather_monitor | grep -q "Up"; do sleep 2; done'
                    '''
                }
            }
        }
        
        stage('Notify Success') {
            steps {
                echo 'Deployment completed successfully!'
                echo 'Weather monitoring service is now running'
            }
        }
    }
    
    post {
        always {
            echo 'Pipeline completed'
            // Clean up workspace
            cleanWs()
        }
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            echo 'Pipeline failed!'
            echo 'Please check the logs for more details'
        }
    }
}
