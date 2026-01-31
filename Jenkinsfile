pipeline {
    agent any

    environment {
        TRAIN_IMAGE = "airbnb-train"
        API_IMAGE   = "air_bnb_price_prediction-api"
        TAG         = "${BUILD_NUMBER}"

        // MinIO (Jenkins Credentials'tan gelecek)
        MINIO_ENDPOINT   = "http://airbnb.local:9000"
        MINIO_ACCESS_KEY = credentials('minio-access-key')
        MINIO_SECRET_KEY = credentials('minio-secret-key')
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

        stage("Run Model Training & Upload to MinIO") {
            steps {
                sh """
                docker run --rm \
                  -e MINIO_ENDPOINT \
                  -e MINIO_ACCESS_KEY \
                  -e MINIO_SECRET_KEY \
                  -e BUILD_NUMBER=${TAG} \
                  ${TRAIN_IMAGE}:${TAG} \
                  sh -c "
                    mc alias set minio \$MINIO_ENDPOINT \
                      \$MINIO_ACCESS_KEY \$MINIO_SECRET_KEY &&
                    python -m backend.src.train
                  "
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
            echo "✅ TRAINING + MODEL UPLOAD + API IMAGE BUILD SUCCESSFUL"
        }
        failure {
            echo "❌ PIPELINE FAILED"
        }
    }
}
