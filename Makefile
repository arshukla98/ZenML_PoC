# Before Running init, first run -> source .venv/bin/activate

# make init -> make run -> make deploy -> make predict -> make start -> make cleanup

init:
	zenml --version
	zenml down && zenml up

run:
	python run_pipeline.py 

deploy:
	python run_deployment.py --config deploy

predict:
	python run_deployment.py --config predict

start:
	streamlit run streamlit_app.py 

cleanup:
	zenml down && zenml up