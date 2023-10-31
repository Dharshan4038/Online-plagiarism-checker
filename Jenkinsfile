pipeline {
   agent any
   environment {
     PATH = "C:\Users\kumar\Downloads\apache-maven-3.9.5-bin\apache-maven-3.9.5\bin$PATH"
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
