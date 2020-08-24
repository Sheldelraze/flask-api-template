node {
    stage('Get Source') {
      // copy source code from local file system and test
      // for a Dockerfile to build the Docker image
        git(
           url: 'https://github.com/Sheldelraze/xxxxx.git',
           credentialsId: 'github_authen',
           branch: "master"
        )
      if (!fileExists("Dockerfile")) {
         error('Dockerfile missing.')
      }
   }
    stage('push to aws') {
        env.GIT_COMMIT_MSG = sh (script: 'git log -1 --pretty=%B ${GIT_COMMIT}', returnStdout: true).trim()
        env.GIT_TAG = sh (script: "git tag --sort version:refname | tail -1", returnStdout: true).trim()
        println("Git message: " + env.GIT_COMMIT_MSG )
        println("Latest tag: " + env.GIT_TAG )
        if (env.GIT_COMMIT_MSG.contains("push aws")){
            println("Building and pushing to AWS ECR....")
            docker.withRegistry('https://922969856207.dkr.ecr.ap-southeast-1.amazonaws.com', 'ecr:ap-southeast-1:aws_ecr_new') {
     
                //build image
                def customImage = docker.build("xxxxx:${GIT_TAG}")
    
                //push image
                customImage.push()
            }
        }
        

   }
}