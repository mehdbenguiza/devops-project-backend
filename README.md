# DevOps Project - Small Backend REST API

Petit service backend Flask (< 150 lignes de code) avec observability basique, containerisation Docker, CI/CD GitHub Actions, scans de sécurité et déploiement Kubernetes (Minikube).

**Objectifs remplis** :
- API REST simple
- GitHub workflow (issues, PRs, reviews)
- CI/CD (build, test, SAST, Docker push)
- Observability (metrics, logs, tracing)
- Sécurité (SAST + DAST)
- Containerisation + Kubernetes
- Documentation complète

## Technologies utilisées

- Backend : Python 3.12 + Flask
- Observability : prometheus-flask-exporter, OpenTelemetry (console exporter)
- Container : Docker
- CI/CD : GitHub Actions
- Kubernetes : Minikube + kubectl
- Sécurité : Bandit (SAST), OWASP ZAP (DAST)

## Prérequis

- Ubuntu / Linux
- Python 3.12+
- Docker installé et utilisateur dans le groupe docker
- Minikube + kubectl
- Compte Docker Hub
- Compte GitHub

## Installation et exécution locale

1. Cloner le dépôt :
   ```bash
   git clone https://github.com/mehdibenguiza/devops-project-backend.git
   cd devops-project-backend
2.Créer l'environnement virtuel :
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
3.Lancer l'API :
python app.py
4.Tester les endpoints :
# Health check
curl http://localhost:5000/health
# → {"status":"healthy"}

# Incrémenter le compteur
curl -X POST http://localhost:5000/counter -H "Content-Type: application/json" -d '{"increment": 5}'
# → {"counter":5} (ou valeur précédente +5)

# Métriques Prometheus
curl http://localhost:5000/metrics
# → retourne les métriques (flask_http_request_duration_seconds, etc.)
5.Docker – Containerisation:
Build de l'image :Bashdocker build -t my-backend-api:latest .
Lancer le container :Bashdocker run -d -p 5000:5000 --name backend-container my-backend-api:latest
Tester depuis l'hôte :Bashcurl http://localhost:5000/health
curl -X POST http://localhost:5000/counter -H "Content-Type: application/json" -d '{"increment": 10}'
curl http://localhost:5000/metrics | head -n 30
Arrêt et nettoyage :Bashdocker stop backend-container
docker rm backend-container
6.Kubernetes – Déploiement sur Minikube:
Lancer Minikube :Bashminikube start --driver=docker
Déployer les manifests :Bashkubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
Vérifier le statut :Bashkubectl get pods
# → backend-api-...   1/1     Running

kubectl get svc
# → backend-api-service   LoadBalancer   ...   80:xxxxx/TCP
Obtenir l'URL d'accès :Bashminikube service backend-api-service --url
# Exemple : http://192.168.49.2:32620
Tester l'API déployée :Bashcurl http://192.168.49.2:32620/health
# → {"status":"healthy"}

curl -X POST http://192.168.49.2:32620/counter -H "Content-Type: application/json" -d '{"increment": 5}'
# → {"counter":X}

curl http://192.168.49.2:32620/metrics
