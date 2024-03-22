@Library('sharedlib') _

def triggeredBy = currentBuild.rawBuild.getCause(Cause.UserIdCause)?.getUserId() ?: 'Unknown User'


pipeline {
    agent {
        label 'vps-node'
    }
    stages {
        stage('Notify Start') {
            steps {
                script {
                    echo '${triggeredBy} started the build'
                    def notificationArgs = [
                            jobName: env.JOB_NAME,
                            buildNumber: env.BUILD_NUMBER.toInteger(),
                            notificationType: 'start',
                            recipient: triggeredBy
                    ]

                    sendNotification(notificationArgs)

                }
            }
        }
        stage('Checkout') {
            steps {
                script {
                    checkoutRepo()
                }
            }
        }
        stage('Build') {
            steps {
                script {

                    Map<String, String> additionalArgs = [
                            IMAGE_NAME: 'bank-api',
                            TAG: 'latest'
                    ]

                    buidlDockerImageNoCredentials(additionalArgs)
                }
            }
        }
        stage('Clean previous version') {
            steps {
                script {
                    String appName = 'bank-api-latest'
                    cleanWorkspace(appName)
                }
            }
        }
        stage('Deploy') {
            steps {
                script {
                    // The ID of your secretFile credential containing the build args
                    String imageId = 'bank-api'
                    String name = 'bank-api-latest'
                    String dockerPort = '8000'
                    String outputPort = '8000'
                    // Additional arguments not in the secret file

                    deploy(imageId, dockerPort,outputPort,name)



                }
            }
        }
    }
    post {
        always {
            script {
                def notificationArgs = [
                        jobName: env.JOB_NAME,
                        buildNumber: env.BUILD_NUMBER.toInteger(),
                        notificationType: currentBuild.result == 'SUCCESS' ? 'end' : 'error',
                        recipient: params.correo
                ]

                // Call the sendNotification function with the arguments map
                sendNotification(notificationArgs)
            }
        }
    }
}

