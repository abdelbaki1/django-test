pipeline{
    agent{
        label "linux"
    }
    stages{
        stage("build the containers from docker-compose file"){
            steps{
 
                sh 'docker-compose build -d sql_containner '
            }
            post{
               
                failure{
                    echo "there been somthing wrong with docker compose build"
                }
            }
        }
        stage("run the containers"){
            steps{
                sh "docker-compose start -d sql_containner"
            }

        }
        stage("COPY DATA FROM THE CONTAINER TO JENKINS CONTAINER") {
        steps {
            script {
            def containerId = sh(script: "docker-compose ps -q sql_container", returnStdout: true).trim()
            sh "docker exec ${containerId} tar -cvzf /var/lib/mysql/backup.tar.gz /var/lib/mysql"
            sh "docker cp ${containerId}:/var/lib/mysql/data/backup.tar.gz /var/jenkins_home/backups/\$(date+%Y/%m/%d)"
        }
    }
}

    }
}