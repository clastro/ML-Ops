import mlflow
import mlflow.sklearn

with mlflow.start_run():
    # Train model on dataset
    model.fit_generator(generator=training_generator,
                    validation_data=validation_generator,
                    epochs = 20,
                    use_multiprocessing=True,
                    workers=2)
    test = model.predict(validation_generator)
    loss_and_metrics = model.evaluate_generator(validation_generator)
    
    mlflow.log_metric("loss", loss_and_metrics[0])  
    mlflow.log_metric("auccuracy", loss_and_metrics[1])  
    mlflow.log_metric("auc", loss_and_metrics[2])

    tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

    # Model registry does not work with file store
    if tracking_url_type_store != "file":

        mlflow.sklearn.log_model(model, "model", registered_model_name="keras_CNN")
    else:
        mlflow.sklearn.log_model(model, "model")
