from Ingest_data import ingest_data
from Feature_engineering import preprocess_data, split_step
from Modeling import modeling,predict
from Model_evaluation import evaluate
from zenml import pipeline
from zenml.client import Client


@pipeline
def ev_range_prediction_pipeline(data_path: str) -> float:
    """Full ML pipeline."""
    print("Ingesting data...")  # Print statements for debugging
    data = ingest_data(data_path=data_path)
    print("Preprocessing data...")
    processed_data = preprocess_data(data)
    print('splitting data...')
    x_train, x_test, y_train, y_test = split_step(processed_data, test_size=0.2, target_column='Electric Range')
    print('modeling data...')
    model = modeling(x_train, y_train)
    print('predicting data...')
    predictions = predict(model, x_test)
    print('evaluating data...')
    accuracy = evaluate(y_test,predictions)
    return accuracy


if __name__ == '__main__':
    print(Client().active_stack.experiment_tracker.get_tracking_uri())
    print('Running pipeline...')
    ev_range_prediction_pipeline('Data\Electric_Vehicle_Population_Data.csv')
    print('Done!')