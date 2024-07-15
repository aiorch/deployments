ssh -i "RAGinBox.pem" ubuntu@ec2-44-204-133-208.compute-1.amazonaws.com -N -L 8888:localhost:8888 -L 8000:localhost:8000 -L 6333:localhost:6333 -L 8501:localhost:8501
