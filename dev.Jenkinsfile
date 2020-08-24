node {
    def env_vars = [
            "SERVICE_GRAYLOG_IP": "xxx.xxx.xxx.xxx",
            "SERVICE_GRAYLOG_PORT": 12201,
            "SERVICE_KNIGHTMARE_IP": "http://{IP}:{port}",
            "MONGO_COLLECTION": "material",
            "MONGO_URI": "mongodb://{username}:{password}@{IP}:{port}/{db}",
        ]
    env_vars_list = []
    docker_env_content = ''
    for (var in env_vars) {
        line = "${var.key}=${var.value}"
        env_vars_list.add(line)
        docker_env_content += line + '\n'
    }

    stage('Create docker_env'){
        writeFile file: 'docker_env', text: docker_env_content
    }
   stage('Get Source') {
      // copy source code from local file system and test
      // for a Dockerfile to build the Docker image
        git(
           url: 'https://github.com/Sheldelraze/xxxx.git',
           credentialsId: 'github_authen',
           branch: "dev"
        )
      if (!fileExists("Dockerfile")) {
         error('Dockerfile missing.')
      }
   }
   stage('check code quality'){
       sh "python3.6 -m pip install pytest-repeat black isort flake8 pytest --user"
       sh "python3.6 -m pip install -r requirements.txt --user"
       sh "python3.6 -m black -l 120 --check ."
   }
  stage('run unittest'){
        withEnv(env_vars_list) {
            sh "python3.6 -m pytest -rA -vv"
        }
       
   }
   stage('Build Docker') {
         sh "docker build -t xxxxx-dev ."
   }
   stage('Stop old container') {
         sh "docker rm -f xxxxx-dev || true"
   }
   stage("run new container"){
        sh "docker run -p 3412:3412 -e TZ=Asia/Ho_Chi_Minh --env-file docker_env --name xxxxx-dev -d brahm-dev"
   }
}