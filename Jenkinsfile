pipeline {
    agent any

    environment {
        TRAIN_IMAGE = "airbnb-train"
        TAG = "${BUILD_NUMBER}"

        MINIO_ACCESS_KEY = credentials('minio-access-key')
        MINIO_SECRET_KEY = credentials('minio-secret-key')
    }

    stages {

        stage("Build Training Image") {
            steps {
                sh '''
                docker build \
                  -t ${TRAIN_IMAGE}:${TAG} \
                  -f backend/Dockerfile.train .
                '''
            }
        }

        stage("Run Training Job") {
            options {
                timeout(time: 10, unit: 'MINUTES')
            }
            steps {
                sh '''
                docker run --rm \
                  --network air_bnb_price_prediction_default \
                  -e MINIO_ENDPOINT=minio:9000 \
                  -e MINIO_ACCESS_KEY \
                  -e MINIO_SECRET_KEY \
                  -e MINIO_BUCKET=ml-models \
                  -e BUILD_NUMBER=${TAG} \
                  ${TRAIN_IMAGE}:${TAG} \
                  python -m backend.src.train
                '''
            }
        }

        stage("Deploy Services with Docker Compose") {
            steps {
                sh '''
                docker compose up -d --build
                '''
            }
        }
    }

    post {
        success {
            echo "✅ TRAIN COMPLETED → SERVICES DEPLOYED (API + UI)"
        }
        failure {
            echo "❌ PIPELINE FAILED"
        }
    }
}
