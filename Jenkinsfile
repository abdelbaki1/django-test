pipeline {
    agent none

    environment {
        AGENT_CONTAINER_ID = ''
    }

    stages {
        stage('Run Agent Container') {
            agent {
                docker {
                    image 'mysql:5.7.22'
                    args "--name backup_container -v .sqlbackups:/var/sqlbackup:rw"
                }
            }
            steps {
                script {
                    try {
                        sh'docker ps'
                        // Capture the container ID for later use
                        AGENT_CONTAINER_ID = sh(script: 'docker ps -aqf name=backup_container', returnStdout: true).trim()
                        echo "Agent container ID: ${AGENT_CONTAINER_ID}"
                        sh """
                                #!/bin/bash
                               tar -czf /var/sqlbackup/\$(date +%Y/%m/%d) /var/lib/mysql/
                            """
                    } catch (Exception e) {
                        currentBuild.result = 'FAILURE'
                        error("Failed to capture agent container ID: ${e.getMessage()}")
                    }
                }
            }
        }
        

        stage("move the dir away"){
            agent any
            steps {
                script {
                    try {
                      sh "mv -Tvp .sqlbackup/*  docic_backup/ "
                    } catch (Exception e) {
                        currentBuild.result = 'FAILURE'
                        error("Backup failed: ${e.getMessage()}")
                    }
                }


            }
        }
        

        // stage('Cleanup') {
        //     steps {
        //         script {
        //             try {
        //                 // Stop and remove the agent container
        //                 sh "docker stop ${AGENT_CONTAINER_ID}"
        //                 sh "docker rm ${AGENT_CONTAINER_ID}"
        //             } catch (Exception e) {
        //                 error("Failed to cleanup agent container: ${e.getMessage()}")
        //             }
        //         }
        //     }
        // }
    }

    // post {
    //     always {
    //         // Send notifications based on build result
    //         slackSend(color: currentBuild.result == 'SUCCESS' ? 'good' : 'danger', message: "Backup completed with status: ${currentBuild.result}")
    //         emailext body: "Backup completed with status: ${currentBuild.result}", subject: "Jenkins Backup Status", to: "your@email.com"
    //     }
    // }
}
