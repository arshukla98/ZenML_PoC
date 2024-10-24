import json
import numpy as np
import pandas as pd
from .utils import get_data_for_test

from zenml.config import DockerSettings

from zenml.integrations.mlflow.model_deployers.mlflow_model_deployer import(MLFlowModelDeployer,)
from zenml.integrations.mlflow.services import MLFlowDeploymentService
from zenml.integrations.mlflow.steps import mlflow_model_deployer_step

from zenml.steps import BaseParameters
from zenml import pipeline, step
from steps.clean_data import clean_df
from steps.evaluation import evaluate_model
from steps.ingest_data import ingest_df
from steps.model_train import train_model

docker_settings=DockerSettings(required_integrations=['mlflow'])

##################################
# Continuous Deployment Pipeline #
##################################

class DeploymentTriggerConfig(BaseParameters):
  """Class for configuring deployment trigger"""
  min_accuracy: float=0.5


@step 
def deployment_trigger(
  accuracy:float,
  config: DeploymentTriggerConfig,
)->bool:
  return accuracy > config.min_accuracy


@pipeline(enable_cache=False, settings={"docker":docker_settings})
def continuous_deployment_pipeline(
   data_path: str,
   min_accuracy:float=0.5,
   workers: int=1,
   timeout: int=60,
):
   df=ingest_df(data_path=data_path)

   X_train,X_test,Y_train,Y_test=clean_df(df)

   model=train_model(X_train,Y_train)
   
   evaluation_metrics=evaluate_model(model,X_test,Y_test)
   
   deployment_decision=deployment_trigger(evaluation_metrics)    
   
   mlflow_model_deployer_step(
      model=model,
      deploy_decision=deployment_decision,
      workers=workers,
      timeout=timeout,
    )

##################################
#     Inference Pipeline         #
##################################
    
class MLFlowDeploymentLoaderStepParameters(BaseParameters):
   pipeline_name:str
   step_name:str
   running:bool=True


@step(enable_cache=False)
def dynamic_importer()->str:
   data=get_data_for_test()
   return data  

@step(enable_cache=False)
def prediction_service_loader(
   pipeline_name: str,
   pipeline_step_name: str,
   running: bool=True,
   model_name: str="model", 
)->MLFlowDeploymentService:

   mlflow_model_deployer_component=MLFlowModelDeployer.get_active_model_deployer()

   existing_services=mlflow_model_deployer_component.find_model_server(
                        pipeline_name=pipeline_name,
                        pipeline_step_name=pipeline_step_name,
                        model_name=model_name,
                        running=running)   
   
   if not existing_services:
      raise RuntimeError(
         f"No MLFlow deployment service found for pipeline "
         f"{pipeline_name},step {pipeline_step_name} and "
         f"model{model_name} and pipeline for the model "
         f"{model_name} is currently running" 
      )
   print("Existing Services:", existing_services)
   print(type(existing_services))
   return existing_services[0]


@step(enable_cache=False)
def predictor(
    service: MLFlowDeploymentService,
    data: str,
) -> np.ndarray:
    """Run an inference request against a prediction service"""

    service.start(timeout=21)  # should be a NOP if already started
    data = json.loads(data)
    data.pop("columns")
    data.pop("index")
    columns_for_df = ['Age','DistanceFromHome', 'Education', 'EnvironmentSatisfaction',
       'JobInvolvement', 'JobLevel', 'JobSatisfaction',
       'MonthlyIncome', 'NumCompaniesWorked',
       'OverTime', 'PercentSalaryHike', 'PerformanceRating',
       'StockOptionLevel', 'TotalWorkingYears',
       'TrainingTimesLastYear', 'WorkLifeBalance', 'YearsAtCompany',
       'YearsInCurrentRole', 'YearsSinceLastPromotion',
       'YearsWithCurrManager']
    try:
      df = pd.DataFrame(data["data"], columns=columns_for_df)
      json_list = json.loads(json.dumps(list(df.T.to_dict().values())))
      data = np.array(json_list)
      #print("Input Data Shape:", data.shape)
      #print("Input Data Sample:", data[:5])
      prediction = service.predict(data)
      print(prediction[prediction == 0].shape, prediction[prediction == 1].shape)
      return prediction
    except Exception as e:
        print(f"Prediction error: {str(e)}")

   
@pipeline(enable_cache=False,settings={"docker":docker_settings})
def inference_pipeline(pipeline_name: str, pipeline_step_name:str):
   data=dynamic_importer()
   service=prediction_service_loader(
      pipeline_name=pipeline_name,
      pipeline_step_name=pipeline_step_name,
      running=False,
      )
   prediction=predictor(service=service,data=data)
   return prediction