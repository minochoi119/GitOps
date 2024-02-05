pipeline {
  agent any
  stages {
    stage('git pull') {
      steps {
<<<<<<< HEAD
        // https://github.com/minochoi119/GitOps will replace by sed command before RUN
        git url: 'https://github.com/minochoi119/GitOps', branch: 'main'
=======
        // https://github.com/minochoi119/GitOps.git will replace by sed command before RUN
        git url: 'https://github.com/minochoi119/GitOps.git', branch: 'main'
>>>>>>> 868231b5aec306d9161ec4532235ab7ca829d5be
      }
    }
    stage('k8s deploy'){
      steps {
        kubernetesDeploy(kubeconfigId: 'kubeconfig',
                         configs: '*.yaml')
      }
    }    
  }
}