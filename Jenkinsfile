pipeline {
   agent any
   environment {
     PATH = "D:/DevTools/apache-maven-3.9.4/bin$PATH"
   }
   stages {
     stage('Checkout') {
       steps {
         checkout scm
       }
   }
   stage('Build') {
      steps {
       bat "C:\\Windows\\System32\\cmd.exe /c mvn clean test"
       }
     }
   }
}
