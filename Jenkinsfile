pipeline {
    agent any

    environment {
        APP_NAME     = "airbnb-mlops"
        NAMESPACE    = "airbnb-mlops"
        DOCKER_IMAGE = "air_bnb_price_prediction-api"
        DOCKER_TAG   = "${BUILD_NUMBER}"
    }

    stages {

        /*
        =========================
        MODEL TRAINING (PYTHON)
        =========================
        */
        stage("Model Training") {
            steps {
                echo "🧠 Training ML model (Docker run)"

                sh '''
                    echo "=== JENKINS WORKSPACE ==="
                    pwd
                    ls -la

                    docker run --rm \
                      -v "$WORKSPACE:/app" \
                      -w /app \
                      python:3.12-slim \
                      bash -c "
                        set -e
                        echo '=== INSIDE CONTAINER ==='
                        pwd
                        ls -la
                        echo '=== BACKEND DIR ==='
                        ls -la backend
                        echo '=== REQUIREMENTS FILE ==='
                        ls -la backend/requirements.txt
                        python --version
                        pip install --upgrade pip
                        pip install -r backend/requirements.txt
                        python -m backend.src.train
                      "
                '''
            }
        }

        /*
        =========================
        BUILD DOCKER IMAGE
        =========================
        */
        stage("Build API Docker Image") {
            steps {
                echo "🐳 Building API Docker image"
                sh """
                    docker build \
                      -t ${DOCKER_IMAGE}:${DOCKER_TAG} \
                      -f backend/Dockerfile .
                """
            }
        }

        stage("Tag Image as latest") {
            steps {
                echo "🏷️ Tagging image as latest"
                sh """
                    docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:latest
                """
            }
        }

        /*
        =========================
        DEPLOY TO KUBERNETES
        =========================
        */
        stage("Deploy to Kubernetes") {
            steps {
                echo "🚀 Deploying to Kubernetes"
                sh """
                    chmod +x deploy.sh
                    ./deploy.sh
                """
            }
        }

        stage("Verify Deployment") {
            steps {
                echo "🔍 Verifying deployment"
                sh """
                    kubectl get pods -n ${NAMESPACE}
                """
            }
        }
    }

    post {
        success {
            echo "✅ FULL MLOPS PIPELINE SUCCESSFUL"
        }
        failure {
            echo "❌ PIPELINE FAILED"
        }
    }
}
