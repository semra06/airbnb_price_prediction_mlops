pipeline {
    agent any

    environment {
        TRAIN_IMAGE = "airbnb-train"
        API_IMAGE   = "air_bnb_price_prediction-api"
        UI_IMAGE    = "airbnb-ui"

        TAG = "${BUILD_NUMBER}"

        // MinIO credentials
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

        stage("Run Training & Upload Model") {
            steps {
                sh """
                docker run --rm \
                  --network air_bnb_price_prediction_default \
                  -e MINIO_ENDPOINT=http://minio:9000 \
                  -e MINIO_ACCESS_KEY \
                  -e MINIO_SECRET_KEY \
                  -e BUILD_NUMBER=${TAG} \
                  ${TRAIN_IMAGE}:${TAG} \
                  python -m backend.src.train
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

        stage("Restart API (Load New Model)") {
            steps {
                sh """
                docker stop airbnb_api || true
                docker rm airbnb_api || true

                docker run -d \
                  --name airbnb_api \
                  --network air_bnb_price_prediction_default \
                  -e MINIO_ENDPOINT=http://minio:9000 \
                  -e MINIO_ACCESS_KEY \
                  -e MINIO_SECRET_KEY \
                  -p 8502:8502 \
                  ${API_IMAGE}:${TAG}
                """
            }
        }

        stage("Restart Streamlit UI") {
            steps {
                sh """
                docker stop airbnb_ui || true
                docker rm airbnb_ui || true

                docker run -d \
                  --name airbnb_ui \
                  --network air_bnb_price_prediction_default \
                  -p 8501:8501 \
                  ${UI_IMAGE}:latest
                """
            }
        }
    }

    post {
        success {
            echo "✅ MODEL UPDATED → API & STREAMLIT REFRESHED"
        }
        failure {
            echo "❌ PIPELINE FAILED"
        }
    }
}
