pipeline {
    agent any

    environment {
        TRAIN_IMAGE = "airbnb-train"
        API_IMAGE   = "air_bnb_price_prediction-api"
        TAG         = "${BUILD_NUMBER}"
    }

    stages {

        stage("Build Training Image") {
            steps {
                sh """
                    docker build \
                      -t ${TRAIN_IMAGE}:${TAG} \
                      -f backend/Dockerfile.train .
                """
            }
        }

        stage("Run Model Training") {
            steps {
                sh """
                    docker run --rm ${TRAIN_IMAGE}:${TAG}
                """
            }
        }

        stage("Build API Image") {
            steps {
                sh """
                    docker build \
                      -t ${API_IMAGE}:${TAG} \
                      -f backend/Dockerfile .
                """
            }
        }
    }

    post {
        success {
            echo "✅ TRAINING + API IMAGE BUILD SUCCESSFUL"
        }
        failure {
            echo "❌ PIPELINE FAILED"
        }
    }
}
